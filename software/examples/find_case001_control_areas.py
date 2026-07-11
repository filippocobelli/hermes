"""
Case 001 (Núñez de Balboa) — Control Area candidate search (v2, subtraction method).

v1 searched for explicitly-tagged farmland/scrub/meadow parcels. Only 3 were
found in an 8 km radius — not because rural Extremadura lacks agricultural
land (it is overwhelmingly agricultural/dehesa outside the solar parks), but
because OpenStreetMap tagging coverage for ordinary farmland is sparse here,
unlike solar installations (384 transformation-like ways found in the same
radius, apparently meticulously mapped).

v2 inverts the approach: instead of requiring positively-tagged open land,
it computes eligible land BY SUBTRACTION —

    eligible_zone = (disk of radius SEARCH_RADIUS_M around the treatment
                     centroid) MINUS (treatment footprint + small edge
                     buffer) MINUS (every other transformation found,
                     each buffered by 2 km)

— then reports the largest contiguous surviving "islands" as control area
candidates, ranked by area. This does not depend on land-cover tagging at
all. It still cannot confirm land-cover TYPE (agricultural vs. something
else unmapped) — that remains an outstanding manual/visual check, per
governance/AI_USAGE.md (this script produces candidates, not final
decisions).

Usage:
    python examples/find_case001_control_areas.py
"""

from __future__ import annotations

import requests
from pyproj import Transformer
from shapely.geometry import Point, Polygon
from shapely.ops import transform as shp_transform
from shapely.ops import unary_union

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
ELEVATION_URL = "https://api.open-elevation.com/api/v1/lookup"

TREATMENT_CENTROID = (38.4533, -6.2260)  # lat, lon
TREATMENT_NAME_HINTS = ("núñez de balboa", "nunez de balboa")

SEARCH_RADIUS_M = 8000
TRANSFORM_BUFFER_M = 2000
TREATMENT_EDGE_BUFFER_M = 100
LANDSAT_PIXEL_AREA_M2 = 30 * 30
MIN_REQUIRED_PIXELS = 30
ELEVATION_TOLERANCE_M = 100

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

    print(f"Fetching transformations within {SEARCH_RADIUS_M} m of treatment site...")
    transform_ways = fetch_transformations(lat, lon, SEARCH_RADIUS_M)
    print(f"  {len(transform_ways)} transformation-like ways found.\n")

    treatment_polys = []
    other_transform_polys = []
    for w in transform_ways:
        poly = way_to_polygon(w)
        if poly is None:
            continue
        poly_m = shp_transform(to_utm, poly)
        name = w.get("tags", {}).get("name", "").lower()
        if any(hint in name for hint in TREATMENT_NAME_HINTS):
            treatment_polys.append(poly_m)
        else:
            other_transform_polys.append(poly_m)

    if not treatment_polys:
        print("Could not identify the treatment footprint in this query. Aborting.")
        return

    treatment_union = unary_union(treatment_polys)
    treatment_centroid_utm = treatment_union.centroid

    print(f"Treatment footprint: {treatment_union.area / 10_000:.1f} ha")
    print(f"Other transformations in search radius: {len(other_transform_polys)} way(s)\n")

    excluded_parts = [treatment_union.buffer(TREATMENT_EDGE_BUFFER_M)]
    if other_transform_polys:
        other_union = unary_union(other_transform_polys)
        excluded_parts.append(other_union.buffer(TRANSFORM_BUFFER_M))
    excluded_zone = unary_union(excluded_parts)

    search_disk = treatment_centroid_utm.buffer(SEARCH_RADIUS_M)
    eligible_zone = search_disk.difference(excluded_zone)

    if eligible_zone.is_empty:
        print("No eligible land remains after exclusion — the search radius is fully "
              "covered by transformation buffers. Increase SEARCH_RADIUS_M and retry.")
        return

    islands = list(eligible_zone.geoms) if eligible_zone.geom_type == "MultiPolygon" else [eligible_zone]

    candidates = []
    for island in islands:
        pixels = int(island.area // LANDSAT_PIXEL_AREA_M2)
        if pixels < MIN_REQUIRED_PIXELS:
            continue
        centroid_utm = island.centroid
        centroid_lonlat = shp_transform(to_wgs84, centroid_utm)
        dist_to_treatment = island.distance(treatment_union)
        candidates.append(
            {
                "area_ha": island.area / 10_000,
                "pixels": pixels,
                "centroid_lat": centroid_lonlat.y,
                "centroid_lon": centroid_lonlat.x,
                "dist_to_treatment_m": dist_to_treatment,
            }
        )

    candidates.sort(key=lambda c: c["area_ha"], reverse=True)

    print(f"Eligible land (by subtraction) split into {len(islands)} contiguous island(s); "
          f"{len(candidates)} exceed the {MIN_REQUIRED_PIXELS}-pixel minimum.\n")

    if not candidates:
        print("No island exceeds the minimum pixel count. Increase SEARCH_RADIUS_M.")
        return

    top = candidates[:8]
    print(f"{'Rank':>4} | {'Area (ha)':>10} | {'Pixels':>7} | {'Dist to treatment (m)':>22} | Centroid (lat, lon)")
    print("-" * 95)
    for i, c in enumerate(top, 1):
        print(f"{i:>4} | {c['area_ha']:>10.1f} | {c['pixels']:>7} | "
              f"{c['dist_to_treatment_m']:>22.0f} | {c['centroid_lat']:.4f}, {c['centroid_lon']:.4f}")

    print("\nChecking elevation (Open-Elevation API)...")
    points = [TREATMENT_CENTROID] + [(c["centroid_lat"], c["centroid_lon"]) for c in top]
    try:
        elevations = get_elevations(points)
    except Exception as exc:
        print(f"  Elevation lookup failed: {exc}")
        elevations = None

    if elevations:
        treatment_elev = elevations[0]
        print(f"  Treatment centroid elevation: {treatment_elev:.0f} m\n")
        print(f"{'Rank':>4} | {'Elevation (m)':>13} | {'Diff (m)':>9} | Within +-{ELEVATION_TOLERANCE_M}m?")
        print("-" * 55)
        for i, (c, elev) in enumerate(zip(top, elevations[1:]), 1):
            diff = elev - treatment_elev
            ok = "yes" if abs(diff) <= ELEVATION_TOLERANCE_M else "NO"
            print(f"{i:>4} | {elev:>13.0f} | {diff:>+9.0f} | {ok}")

    print(
        "\nIMPORTANT — this method confirms only ABSENCE of known transformations, not the\n"
        "PRESENCE of correct land cover (agricultural/dehesa matching the treatment site's\n"
        "pre-2019 state). Each surviving candidate must still be visually/spectrally checked\n"
        "(e.g. Sentinel-2 true-color or NDVI at the centroid) before being accepted — this is\n"
        "an eligibility filter, not a land-cover confirmation.\n"
        "\n"
        "Next steps (human review required, per governance/AI_USAGE.md):\n"
        "  1. Visually verify land cover of top candidates via imagery.\n"
        "  2. Pick >= 2 candidates with elevation within tolerance and confirmed matching "
        "land cover.\n"
        "  3. Confirm distance-to-water-body is the same order of magnitude as the "
        "treatment site (not yet automated)."
    )


if __name__ == "__main__":
    main()
