"""
Case 001 — Export geometries (treatment clean zone + control area buffers) as GeoJSON.

v3: fixes a reintroduced bug. v2 (and this file before the fix) computed
"other_polys" as every solar-tagged way NOT carrying the treatment's name
tag, and subtracted a 2km buffer around each individually. Most of those
~76 unnamed ways are internal sub-components of Nunez de Balboa's own
footprint (individually-mapped panel-array blocks, per OSM convention for
large solar farms) — NOT external neighbours. Treating each as a separate
"neighbouring transformation" and subtracting 77 overlapping 2km buffers
centered on the plant's own location destroyed the entire clean zone.

This is the exact bug already found and fixed earlier in
check_case001_confounders_geom.py / compute_case001_clean_zone.py (the
"31 false alarms -> 2 real neighbours" correction). This version reuses
that validated clustering logic instead of re-deriving it: adjacent/
overlapping solar-tagged polygons are merged into clusters BEFORE distance
to the treatment cluster is measured. Only genuinely separate clusters
count as neighbours.

Usage:
    python examples/export_case001_geometries.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import requests
from pyproj import Transformer
from shapely.geometry import Point, Polygon, mapping
from shapely.ops import transform as shp_transform
from shapely.ops import unary_union

OVERPASS_MIRRORS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.openstreetmap.ru/api/interpreter",
]

TREATMENT_CENTROID = (38.4533, -6.2260)
TREATMENT_NAME_HINTS = ("núñez de balboa", "nunez de balboa")

SEARCH_RADIUS_M = 6000
TRANSFORM_BUFFER_M = 2000
TREATMENT_EDGE_BUFFER_M = 30  # one Landsat pixel, per HYPOTHESES.md 4.1
CLUSTER_TOLERANCE_M = 150  # merge polygons separated by up to this gap (internal roads)

CONTROL_POINTS = {
    "control_1_C5": (38.43507, -6.16257),
    "control_2_C1": (38.43534, -6.17401),
}
CONTROL_RADIUS_M = 300

OUTPUT_DIR = Path("../research_programs/RP001-surface-transformation-energy-balance/cases/geometries")

MAX_RETRIES_PER_MIRROR = 2
BACKOFF_BASE_S = 3

HEADERS = {
    "User-Agent": "HERMES-research-framework/0.1 (https://github.com/filippocobelli/hermes)",
    "Accept": "application/json",
}


def overpass(query: str) -> list[dict]:
    for mirror in OVERPASS_MIRRORS:
        for attempt in range(1, MAX_RETRIES_PER_MIRROR + 1):
            try:
                resp = requests.post(mirror, data={"data": query}, headers=HEADERS, timeout=120)
                resp.raise_for_status()
                data = resp.json()
                elements = data.get("elements", [])
                if elements:
                    return elements
                print(f"    [{mirror}] returned 0 elements (attempt {attempt}) — retrying")
            except requests.exceptions.RequestException as exc:
                print(f"    [{mirror}] attempt {attempt}/{MAX_RETRIES_PER_MIRROR} failed: {exc}")
            if attempt < MAX_RETRIES_PER_MIRROR:
                time.sleep(BACKOFF_BASE_S * attempt)
        print(f"    Giving up on {mirror}, trying next mirror...")
    raise RuntimeError(
        "All Overpass mirrors failed or returned empty results after retries. "
        "This is a network/service issue, not a code issue — re-run later."
    )


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
    """Union-find clustering of polygons that touch/overlap within tolerance_m."""
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


def save_geojson(geom_wgs84, path: Path, properties: dict) -> None:
    feature = {"type": "Feature", "geometry": mapping(geom_wgs84), "properties": properties}
    path.write_text(json.dumps(feature, indent=2))
    print(f"  Saved: {path}")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    lat, lon = TREATMENT_CENTROID
    to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True).transform
    to_wgs84 = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True).transform

    print("Fetching transformations for treatment clean-zone computation...")
    ways = overpass(f"""
    [out:json][timeout:120];
    (
      way["power"="plant"](around:{SEARCH_RADIUS_M},{lat},{lon});
      way["power"="generator"]["generator:source"="solar"](around:{SEARCH_RADIUS_M},{lat},{lon});
    );
    out geom;
    """)
    print(f"  Retrieved {len(ways)} ways.")

    records = []
    for w in ways:
        poly = way_to_polygon(w)
        if poly is None:
            continue
        poly_m = shp_transform(to_utm, poly)
        name = w.get("tags", {}).get("name", "")
        records.append({"id": w["id"], "name": name, "poly": poly_m, "tags": w.get("tags", {})})

    if not records:
        raise RuntimeError("No valid polygons retrieved from Overpass. Aborting.")

    # --- Cluster BEFORE measuring distance (the validated fix) ---
    clusters = cluster_polygons(records, CLUSTER_TOLERANCE_M)

    treatment_cluster_id = None
    for cid, idxs in clusters.items():
        for i in idxs:
            if any(h in records[i]["name"].lower() for h in TREATMENT_NAME_HINTS):
                treatment_cluster_id = cid
                break
        if treatment_cluster_id is not None:
            break

    if treatment_cluster_id is None:
        raise RuntimeError(
            f"Could not identify the treatment cluster (name hints: {TREATMENT_NAME_HINTS}) "
            f"among {len(records)} polygons in {len(clusters)} cluster(s). Aborting — NOT "
            "writing geometry files."
        )

    treatment_union = unary_union([records[i]["poly"] for i in clusters[treatment_cluster_id]])
    if treatment_union.is_empty or treatment_union.area <= 0:
        raise RuntimeError("Treatment cluster union is empty/zero-area. Aborting.")

    n_merged = len(clusters[treatment_cluster_id])
    print(f"  Treatment cluster identified: {treatment_union.area / 10_000:.1f} ha "
          f"({n_merged} way(s) merged — includes internal sub-components)")

    interior = treatment_union.buffer(-TREATMENT_EDGE_BUFFER_M)

    # --- Only genuinely separate clusters count as neighbours ---
    clean_zone = interior
    n_neighbours = 0
    for cid, idxs in clusters.items():
        if cid == treatment_cluster_id:
            continue
        cluster_union = unary_union([records[i]["poly"] for i in idxs])
        dist = cluster_union.distance(treatment_union)
        if dist <= TRANSFORM_BUFFER_M:
            clean_zone = clean_zone.difference(cluster_union.buffer(TRANSFORM_BUFFER_M))
            n_neighbours += 1
            print(f"    Neighbour cluster: {cluster_union.area / 10_000:.1f} ha at {dist:.0f} m")

    print(f"  {n_neighbours} genuinely separate neighbouring cluster(s) found and subtracted "
          f"(out of {len(clusters) - 1} other cluster(s) total — most are internal sub-components).")

    if clean_zone.is_empty or clean_zone.area <= 0:
        raise RuntimeError(
            "Clean zone is empty after subtracting real neighbours. Review ADR-004 / Case 001 "
            "assumptions — this would be a genuine finding, not expected given prior validated "
            "runs (786.2 ha expected)."
        )

    clean_zone_wgs84 = shp_transform(to_wgs84, clean_zone)
    print(f"Treatment clean zone: {clean_zone.area / 10_000:.1f} ha "
          f"(expected ~786.2 ha from prior validated run)")
    save_geojson(
        clean_zone_wgs84,
        OUTPUT_DIR / "treatment_clean_zone.geojson",
        {
            "site_id": "case001_treatment",
            "name": "Nunez de Balboa - clean sampling zone",
            "area_ha": round(clean_zone.area / 10_000, 1),
            "method": "ADR-004 clean-zone (clustered footprint interior minus real "
                      "neighbouring-cluster 2km buffers)",
        },
    )

    for site_id, (clat, clon) in CONTROL_POINTS.items():
        pt_utm = Point(*to_utm(clon, clat))
        buffer_utm = pt_utm.buffer(CONTROL_RADIUS_M)
        buffer_wgs84 = shp_transform(to_wgs84, buffer_utm)
        print(f"{site_id}: {buffer_utm.area / 10_000:.1f} ha (radius {CONTROL_RADIUS_M} m)")
        save_geojson(
            buffer_wgs84,
            OUTPUT_DIR / f"{site_id}.geojson",
            {
                "site_id": site_id,
                "centroid_lat": clat,
                "centroid_lon": clon,
                "radius_m": CONTROL_RADIUS_M,
                "area_ha": round(buffer_utm.area / 10_000, 1),
                "method": f"{CONTROL_RADIUS_M}m circular buffer around locked control point",
            },
        )

    print("\nDone. Geometries saved for reuse by the Layer 2 extraction pipeline.")


if __name__ == "__main__":
    main()
