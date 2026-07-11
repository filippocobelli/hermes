"""
Case 001 (Núñez de Balboa) — Control Area point selection (final step).

The previous script found ONE large (12,598 ha) contiguous eligible zone,
not multiple ranked candidates — because most of the 8 km search radius
survives the exclusion of the treatment site and 383 nearby transformations.

This script extracts concrete, well-separated CANDIDATE POINTS from that
zone (not the whole shapeless blob), each with:
  - an extra safety margin eroded from the eligible zone boundary (so a
    candidate isn't right at the edge of a 2 km exclusion buffer),
  - elevation check,
  - a direct Google Maps link for the final visual land-cover check.

Candidates are sampled at increasing distance from the treatment centroid,
in 8 compass directions, so the selection isn't hand-picked / cherry-picked
per case (same discipline as ADR-004's clean-zone rule: fixed, reproducible
procedure, not manual choice per case).

Usage:
    python examples/select_case001_control_points.py
"""

from __future__ import annotations

import math

import requests
from pyproj import Transformer
from shapely.geometry import Point, Polygon
from shapely.ops import transform as shp_transform
from shapely.ops import unary_union

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
ELEVATION_URL = "https://api.open-elevation.com/api/v1/lookup"

TREATMENT_CENTROID = (38.4533, -6.2260)
TREATMENT_NAME_HINTS = ("núñez de balboa", "nunez de balboa")

SEARCH_RADIUS_M = 8000
TRANSFORM_BUFFER_M = 2000
TREATMENT_EDGE_BUFFER_M = 100
SAFETY_MARGIN_M = 500  # extra erosion so candidates aren't right at a buffer edge

CANDIDATE_DISTANCES_M = [2500, 3500, 4500, 5500, 6500]
CANDIDATE_BEARINGS_DEG = [0, 45, 90, 135, 180, 225, 270, 315]

TREATMENT_ELEV_TOLERANCE_M = 100

HEADERS = {
    "User-Agent": "HERMES-research-framework/0.1 (https://github.com/filippocobelli/hermes)",
    "Accept": "application/json",
}


def overpass(query: str) -> list[dict]:
    resp = requests.post(OVERPASS_URL, data={"data": query}, headers=HEADERS, timeout=150)
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


def fetch_transformations(lat: float, lon: float, radius_m: int) -> list[dict]:
    query = f"""
    [out:json][timeout:120];
    (
      way["power"="plant"](around:{radius_m},{lat},{lon});
      way["power"="generator"]["generator:source"="solar"](around:{radius_m},{lat},{lon});
      way["landuse"="industrial"](around:{radius_m},{lat},{lon});
      way["landuse"="quarry"](around:{radius_m},{lat},{lon});
      way["landuse"="residential"](around:{radius_m},{lat},{lon});
    );
    out geom;
    """
    return overpass(query)


def get_elevations(points: list[tuple[float, float]]) -> list[float]:
    locations = "|".join(f"{lat},{lon}" for lat, lon in points)
    resp = requests.get(ELEVATION_URL, params={"locations": locations}, timeout=30)
    resp.raise_for_status()
    return [r["elevation"] for r in resp.json().get("results", [])]


def main() -> None:
    lat, lon = TREATMENT_CENTROID
    to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True).transform
    to_wgs84 = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True).transform

    print("Rebuilding eligible zone (same method as previous step)...")
    transform_ways = fetch_transformations(lat, lon, SEARCH_RADIUS_M)

    treatment_polys, other_polys = [], []
    for w in transform_ways:
        poly = way_to_polygon(w)
        if poly is None:
            continue
        poly_m = shp_transform(to_utm, poly)
        name = w.get("tags", {}).get("name", "").lower()
        (treatment_polys if any(h in name for h in TREATMENT_NAME_HINTS) else other_polys).append(poly_m)

    treatment_union = unary_union(treatment_polys)
    treatment_centroid_utm = treatment_union.centroid

    excluded = [treatment_union.buffer(TREATMENT_EDGE_BUFFER_M)]
    if other_polys:
        excluded.append(unary_union(other_polys).buffer(TRANSFORM_BUFFER_M))
    excluded_zone = unary_union(excluded)

    search_disk = treatment_centroid_utm.buffer(SEARCH_RADIUS_M)
    eligible_zone = search_disk.difference(excluded_zone)
    safe_zone = eligible_zone.buffer(-SAFETY_MARGIN_M)  # extra margin from any exclusion edge

    print(f"Safe zone (eligible, minus {SAFETY_MARGIN_M} m extra margin): "
          f"{safe_zone.area / 10_000:.1f} ha\n")

    tx, ty = treatment_centroid_utm.x, treatment_centroid_utm.y
    candidate_points = []
    for dist in CANDIDATE_DISTANCES_M:
        for bearing_deg in CANDIDATE_BEARINGS_DEG:
            theta = math.radians(bearing_deg)
            px = tx + dist * math.sin(theta)
            py = ty + dist * math.cos(theta)
            pt = Point(px, py)
            if safe_zone.contains(pt):
                lonlat = shp_transform(to_wgs84, pt)
                candidate_points.append(
                    {"dist_m": dist, "bearing_deg": bearing_deg, "lat": lonlat.y, "lon": lonlat.x}
                )

    if not candidate_points:
        print("No candidate points fall inside the safe zone. Reduce SAFETY_MARGIN_M or "
              "widen SEARCH_RADIUS_M.")
        return

    # Keep well-separated candidates: greedily pick points at least 1 km apart from
    # each other, preferring shorter distance to treatment first (closer = easier
    # weather/regional matching), then diversify by bearing.
    candidate_points.sort(key=lambda c: c["dist_m"])
    selected = []
    for c in candidate_points:
        pt_utm = Point(*to_utm(c["lon"], c["lat"]))
        if all(pt_utm.distance(Point(*to_utm(s["lon"], s["lat"]))) >= 1000 for s in selected):
            selected.append(c)
        if len(selected) >= 5:
            break

    print(f"{len(selected)} well-separated candidate point(s) selected:\n")
    print(f"{'#':>2} | {'Dist (m)':>9} | {'Bearing':>7} | {'Lat, Lon':>20} | Google Maps")
    print("-" * 100)
    for i, c in enumerate(selected, 1):
        maps_url = f"https://maps.google.com/?q={c['lat']:.5f},{c['lon']:.5f}"
        print(f"{i:>2} | {c['dist_m']:>9} | {c['bearing_deg']:>6}° | "
              f"{c['lat']:.5f}, {c['lon']:.5f} | {maps_url}")

    print("\nChecking elevation (Open-Elevation API)...")
    points = [TREATMENT_CENTROID] + [(c["lat"], c["lon"]) for c in selected]
    elevations = get_elevations(points)
    treatment_elev = elevations[0]
    print(f"  Treatment centroid elevation: {treatment_elev:.0f} m\n")
    print(f"{'#':>2} | {'Elevation (m)':>13} | {'Diff (m)':>9} | Within +-{TREATMENT_ELEV_TOLERANCE_M}m?")
    print("-" * 55)
    for i, (c, elev) in enumerate(zip(selected, elevations[1:]), 1):
        diff = elev - treatment_elev
        ok = "yes" if abs(diff) <= TREATMENT_ELEV_TOLERANCE_M else "NO"
        print(f"{i:>2} | {elev:>13.0f} | {diff:>+9.0f} | {ok}")

    print(
        "\nNext step (human review, per governance/AI_USAGE.md): open the Google Maps "
        "links above and visually confirm each candidate is agricultural/dehesa land "
        "(matching the treatment site's pre-2019 cover), not something unmapped "
        "(unlikely but not yet ruled out by this script). Pick >= 2 of these that pass "
        "visual inspection and elevation tolerance as the final RP001 Case 001 control areas."
    )


if __name__ == "__main__":
    main()
