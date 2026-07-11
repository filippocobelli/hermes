"""
Case 001 (Núñez de Balboa) — Clean Sampling Zone computation (ADR-004).

Given the two neighbouring solar plants found within 2 km of the Case 001
footprint (see check_case001_confounders_geom.py output and ADR-004), this
computes the "clean sampling zone": the sub-region of the treatment
footprint's own interior (after the standard one-pixel edge buffer) that
lies >= 2 km from every identified neighbouring transformation.

It then checks this zone against the >= 30 valid interior pixel requirement
from HYPOTHESES.md Section 4.1 (Landsat, 30 m pixels).

This script re-fetches the same OSM data as
check_case001_confounders_geom.py (kept independent/self-contained rather
than importing from it, since this is still exploratory case-selection
work, not part of the Layer 1-6 pipeline).

Usage:
    python examples/compute_case001_clean_zone.py
"""

from __future__ import annotations

import requests
from pyproj import Transformer
from shapely.geometry import Polygon
from shapely.ops import transform as shp_transform
from shapely.ops import unary_union

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

CASE_001_CENTROID = (38.4533, -6.2260)
SEARCH_RADIUS_M = 6000
CRITERION_4_BUFFER_M = 2000
CLUSTER_TOLERANCE_M = 150
EDGE_BUFFER_M = 30  # one Landsat pixel, per HYPOTHESES.md Section 4.1
LANDSAT_PIXEL_AREA_M2 = 30 * 30
MIN_REQUIRED_PIXELS = 30  # HYPOTHESES.md Section 4.1

CASE_001_NAME_HINTS = ("núñez de balboa", "nunez de balboa")


def build_query(lat: float, lon: float, radius_m: int) -> str:
    return f"""
    [out:json][timeout:90];
    (
      way["power"="plant"](around:{radius_m},{lat},{lon});
      way["power"="generator"]["generator:source"="solar"](around:{radius_m},{lat},{lon});
    );
    out geom;
    """


def fetch_ways(lat: float, lon: float, radius_m: int) -> list[dict]:
    query = build_query(lat, lon, radius_m)
    headers = {
        "User-Agent": "HERMES-research-framework/0.1 (https://github.com/filippocobelli/hermes)",
        "Accept": "application/json",
    }
    resp = requests.post(OVERPASS_URL, data={"data": query}, headers=headers, timeout=120)
    resp.raise_for_status()
    return resp.json().get("elements", [])


def way_to_polygon(way: dict) -> Polygon | None:
    geom = way.get("geometry")
    if not geom or len(geom) < 3:
        return None
    coords = [(pt["lon"], pt["lat"]) for pt in geom]
    if coords[0] != coords[-1]:
        coords.append(coords[0])
    try:
        poly = Polygon(coords)
        if not poly.is_valid:
            poly = poly.buffer(0)
        return poly if poly.area > 0 else None
    except Exception:
        return None


def cluster_polygons(records: list[dict], tolerance_m: float) -> dict[int, list[int]]:
    n = len(records)
    parent = list(range(n))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj

    buffered = [r["poly"].buffer(tolerance_m / 2) for r in records]
    for i in range(n):
        for j in range(i + 1, n):
            if buffered[i].intersects(buffered[j]):
                union(i, j)

    clusters: dict[int, list[int]] = {}
    for i in range(n):
        clusters.setdefault(find(i), []).append(i)
    return clusters


def main() -> None:
    lat, lon = CASE_001_CENTROID
    print(f"Fetching way geometries within {SEARCH_RADIUS_M} m of ({lat}, {lon})...")
    ways = fetch_ways(lat, lon, SEARCH_RADIUS_M)
    print(f"Retrieved {len(ways)} ways.\n")

    to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True).transform

    records = []
    for w in ways:
        poly = way_to_polygon(w)
        if poly is None:
            continue
        poly_m = shp_transform(to_utm, poly)
        name = w.get("tags", {}).get("name", "")
        records.append({"id": w["id"], "name": name, "poly": poly_m, "tags": w.get("tags", {})})

    clusters = cluster_polygons(records, CLUSTER_TOLERANCE_M)

    case001_cluster_id = None
    for cid, idxs in clusters.items():
        for i in idxs:
            if any(hint in records[i]["name"].lower() for hint in CASE_001_NAME_HINTS):
                case001_cluster_id = cid
                break
        if case001_cluster_id is not None:
            break

    if case001_cluster_id is None:
        print("Could not identify the Núñez de Balboa cluster. Aborting.")
        return

    case001_union = unary_union([records[i]["poly"] for i in clusters[case001_cluster_id]])

    neighbour_unions = []
    for cid, idxs in clusters.items():
        if cid == case001_cluster_id:
            continue
        cluster_union = unary_union([records[i]["poly"] for i in idxs])
        dist = cluster_union.distance(case001_union)
        if dist <= CRITERION_4_BUFFER_M:
            neighbour_unions.append(cluster_union)

    print(f"Identified {len(neighbour_unions)} neighbouring transformation(s) within "
          f"{CRITERION_4_BUFFER_M} m — subtracting their 2 km buffers from the treatment "
          "footprint's own interior.\n")

    # Step 1: erode the treatment footprint by one pixel (mixed-pixel edge exclusion,
    # per HYPOTHESES.md Section 4.1) — this is about the TRUE land-cover boundary.
    interior = case001_union.buffer(-EDGE_BUFFER_M)

    # Step 2: subtract the 2 km buffer of every identified neighbour (ADR-004).
    clean_zone = interior
    for neighbour in neighbour_unions:
        clean_zone = clean_zone.difference(neighbour.buffer(CRITERION_4_BUFFER_M))

    interior_area_ha = interior.area / 10_000
    clean_area_ha = clean_zone.area / 10_000
    clean_pixels = int(clean_zone.area // LANDSAT_PIXEL_AREA_M2)

    print(f"Treatment footprint interior (after {EDGE_BUFFER_M} m edge buffer): "
          f"{interior_area_ha:.1f} ha")
    print(f"Clean sampling zone (also >= {CRITERION_4_BUFFER_M} m from neighbours): "
          f"{clean_area_ha:.1f} ha")
    print(f"Estimated valid interior Landsat pixels (30 m) in clean zone: {clean_pixels}")
    print(f"Required minimum (HYPOTHESES.md Section 4.1): {MIN_REQUIRED_PIXELS}\n")

    if clean_pixels >= MIN_REQUIRED_PIXELS:
        print(f"RESULT: PASS — clean zone provides {clean_pixels} pixels, "
              f">= the required {MIN_REQUIRED_PIXELS}. Case 001 can be approved for "
              "Criterion 4 (ADR-004), sampling restricted to this clean sub-region.")
    else:
        print(f"RESULT: FAIL — clean zone provides only {clean_pixels} pixels, "
              f"< the required {MIN_REQUIRED_PIXELS}. Case 001 should be reconsidered "
              "or the neighbouring transformations investigated further "
              "(e.g. commissioning dates — if built AFTER the observation window "
              "of interest, they may not apply as of the relevant period).")


if __name__ == "__main__":
    main()
