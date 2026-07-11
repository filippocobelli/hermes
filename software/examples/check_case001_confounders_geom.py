"""
Case 001 (Núñez de Balboa) — Criterion 4 verification, geometry-aware.

The first version of this check (check_case001_confounders.py) flagged 31
OSM features within the 2 km buffer, almost all tagged simply
"power=generator, generator:source=solar" with no name. This is expected
OSM mapping practice for large solar farms: each panel row/array block is
frequently digitised as its own way, all belonging to the SAME plant, not
to separate nearby developments.

Treating these as independent "confounding transformations" without
checking their actual geometry would have been a methodological error —
counting a plant's own internal structure as evidence against itself.
Per Foundation Core Principles ("Method before conclusion"), this version
fixes that by working with real geometry instead of a single centroid
point:

  1. Downloads full way geometries (not just centroids).
  2. Clusters adjacent/overlapping solar-tagged polygons together (a
     tolerance buffer merges polygons separated only by internal access
     roads/gaps into one cluster).
  3. Identifies the cluster containing the named "Planta Solar Núñez de
     Balboa" way as the Case 001 treatment footprint.
  4. Reports any OTHER, spatially distinct cluster and its true minimum
     distance to the Case 001 footprint boundary (not to an arbitrary
     centroid point).

Usage:
    python examples/check_case001_confounders_geom.py
"""

from __future__ import annotations

import requests
from pyproj import Transformer
from shapely.geometry import Polygon
from shapely.ops import transform as shp_transform
from shapely.ops import unary_union

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

CASE_001_CENTROID = (38.4533, -6.2260)  # lat, lon — search anchor only, not a distance reference
SEARCH_RADIUS_M = 6000
CRITERION_4_BUFFER_M = 2000
CLUSTER_TOLERANCE_M = 150  # merge polygons separated by up to this gap (internal roads)

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


def main() -> None:
    lat, lon = CASE_001_CENTROID
    print(f"Fetching way geometries within {SEARCH_RADIUS_M} m of ({lat}, {lon})...")
    ways = fetch_ways(lat, lon, SEARCH_RADIUS_M)
    print(f"Retrieved {len(ways)} ways.\n")

    # Project to a metric CRS (UTM 29N covers this longitude) for area/distance in metres.
    to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True).transform

    records = []
    for w in ways:
        poly = way_to_polygon(w)
        if poly is None:
            continue
        poly_m = shp_transform(to_utm, poly)
        name = w.get("tags", {}).get("name", "")
        records.append({"id": w["id"], "name": name, "poly": poly_m, "tags": w.get("tags", {})})

    if not records:
        print("No valid polygons retrieved.")
        return

    # --- Cluster adjacent/overlapping polygons (union-find via buffered intersection) ---
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

    buffered = [r["poly"].buffer(CLUSTER_TOLERANCE_M / 2) for r in records]
    for i in range(n):
        for j in range(i + 1, n):
            if buffered[i].intersects(buffered[j]):
                union(i, j)

    clusters: dict[int, list[int]] = {}
    for i in range(n):
        clusters.setdefault(find(i), []).append(i)

    # --- Identify the Case 001 cluster (contains the named Núñez de Balboa way) ---
    case001_cluster_id = None
    for cid, idxs in clusters.items():
        for i in idxs:
            if any(hint in records[i]["name"].lower() for hint in CASE_001_NAME_HINTS):
                case001_cluster_id = cid
                break
        if case001_cluster_id is not None:
            break

    if case001_cluster_id is None:
        print(
            "Could not identify the named Núñez de Balboa way among the results. "
            "Cannot proceed with cluster-relative distance check."
        )
        return

    case001_union = unary_union([records[i]["poly"] for i in clusters[case001_cluster_id]])
    case001_area_ha = case001_union.area / 10_000
    print(
        f"Case 001 cluster: {len(clusters[case001_cluster_id])} way(s) merged, "
        f"total area ~ {case001_area_ha:.0f} ha "
        "(cross-check vs. official ~943-1,000 ha).\n"
    )

    print(f"{'Cluster size':>12} | {'Distance to Case 001 (m)':>25} | {'Area':>9} | Name | Tags")
    print("-" * 110)

    other_clusters_within_buffer = []
    for cid, idxs in clusters.items():
        if cid == case001_cluster_id:
            continue
        cluster_union = unary_union([records[i]["poly"] for i in idxs])
        dist = cluster_union.distance(case001_union)
        cluster_area_ha = cluster_union.area / 10_000

        names = sorted({records[i]["name"] for i in idxs if records[i]["name"]})
        all_tags = {}
        for i in idxs:
            all_tags.update(records[i]["tags"])
        tag_str = ", ".join(
            f"{k}={v}"
            for k, v in all_tags.items()
            if k in ("power", "generator:source", "plant:source", "operator", "start_date")
        )
        name_str = " / ".join(names) if names else "(unnamed)"

        flag = " WARNING: WITHIN 2km" if dist <= CRITERION_4_BUFFER_M else ""
        print(f"{len(idxs):>12} | {dist:>25.0f} | {cluster_area_ha:6.1f} ha | {name_str} | {tag_str}{flag}")
        if dist <= CRITERION_4_BUFFER_M:
            other_clusters_within_buffer.append((cid, dist, len(idxs), name_str))

    print("\n" + "=" * 90)
    if other_clusters_within_buffer:
        print(
            f"{len(other_clusters_within_buffer)} DISTINCT cluster(s), separate from the "
            f"Case 001 plant itself, found within {CRITERION_4_BUFFER_M} m of its true "
            "footprint boundary. Review required before approving Case 001."
        )
    else:
        print(
            f"No distinct solar installation cluster found within {CRITERION_4_BUFFER_M} m "
            "of the Case 001 footprint boundary. The previous 31 'hits' were internal "
            "sub-components of the same plant, correctly merged into one cluster here."
        )

    print(
        "\nCaveat (record uncertainty, per Core Principles): clustering tolerance is "
        f"{CLUSTER_TOLERANCE_M} m — an assumption, not a proven fact. Internal access "
        "roads/gaps wider than this would incorrectly split the plant into separate "
        "clusters; true gaps between distinct plants narrower than this would incorrectly "
        "merge them. This choice should be reviewed, not treated as settled."
    )


if __name__ == "__main__":
    main()
