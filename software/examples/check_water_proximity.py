"""
Case 001 (Núñez de Balboa) — Water body proximity check (v2, resilient).

v1 failed with a 504 Gateway Timeout from the public overpass-api.de
instance (likely overloaded after repeated queries this session). v2 adds:
  - retry with exponential backoff,
  - fallback across multiple public Overpass mirrors,
  - per-point error isolation (one failed point does not abort the others),
  - a small delay between requests to avoid triggering server-side
    rate limiting.

Usage:
    python examples/check_water_proximity.py
"""

from __future__ import annotations

import time

import requests
from pyproj import Transformer
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import transform as shp_transform

OVERPASS_MIRRORS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.openstreetmap.ru/api/interpreter",
]

POINTS = {
    "Treatment (Núñez de Balboa)": (38.4533, -6.2260),
    "Control 1 (C4)": (38.40879, -6.26301),
    "Control 2 (C1)": (38.43534, -6.17401),
    "Backup (C5)": (38.43507, -6.16257),
}

SEARCH_RADIUS_M = 5000
MAX_RETRIES_PER_MIRROR = 2
BACKOFF_BASE_S = 3
DELAY_BETWEEN_POINTS_S = 2

HEADERS = {
    "User-Agent": "HERMES-research-framework/0.1 (https://github.com/filippocobelli/hermes)",
    "Accept": "application/json",
}


def overpass(query: str) -> list[dict] | None:
    """Try each mirror in turn, with retries and backoff. Returns None if all fail."""
    for mirror in OVERPASS_MIRRORS:
        for attempt in range(1, MAX_RETRIES_PER_MIRROR + 1):
            try:
                resp = requests.post(mirror, data={"data": query}, headers=HEADERS, timeout=90)
                resp.raise_for_status()
                return resp.json().get("elements", [])
            except requests.exceptions.RequestException as exc:
                print(f"    [{mirror}] attempt {attempt}/{MAX_RETRIES_PER_MIRROR} failed: {exc}")
                if attempt < MAX_RETRIES_PER_MIRROR:
                    time.sleep(BACKOFF_BASE_S * attempt)
        print(f"    Giving up on {mirror}, trying next mirror...")
    return None


def element_to_geom(el: dict):
    geom = el.get("geometry")
    if not geom or len(geom) < 2:
        return None
    coords = [(pt["lon"], pt["lat"]) for pt in geom]
    if el["type"] == "way" and el.get("tags", {}).get("natural") == "water" and len(coords) >= 3:
        if coords[0] != coords[-1]:
            coords.append(coords[0])
        try:
            poly = Polygon(coords)
            return poly if poly.is_valid and poly.area > 0 else LineString(coords)
        except Exception:
            return LineString(coords)
    return LineString(coords)


def build_query(lat: float, lon: float, radius_m: int) -> str:
    return f"""
    [out:json][timeout:60];
    (
      way["waterway"~"river|stream|canal"](around:{radius_m},{lat},{lon});
      way["natural"="water"](around:{radius_m},{lat},{lon});
    );
    out geom;
    """


def nearest_water_distance(lat: float, lon: float, to_utm) -> tuple[float | None, str]:
    ways = overpass(build_query(lat, lon, SEARCH_RADIUS_M))
    if ways is None:
        return None, "QUERY_FAILED"
    if not ways:
        return None, "NO_RESULTS"

    point_utm = Point(*to_utm(lon, lat))
    min_dist = None
    for w in ways:
        geom = element_to_geom(w)
        if geom is None or geom.is_empty:
            continue
        geom_utm = shp_transform(to_utm, geom)
        d = point_utm.distance(geom_utm)
        if min_dist is None or d < min_dist:
            min_dist = d
    return min_dist, "OK" if min_dist is not None else "NO_VALID_GEOM"


def main() -> None:
    to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True).transform

    print(f"Checking nearest water feature within {SEARCH_RADIUS_M} m of each point "
          f"(with retry/fallback across {len(OVERPASS_MIRRORS)} mirrors)...\n")

    results = {}
    for i, (label, (lat, lon)) in enumerate(POINTS.items()):
        print(f"[{label}]")
        dist, status = nearest_water_distance(lat, lon, to_utm)
        results[label] = (dist, status)
        if status == "OK":
            print(f"  -> {dist:.0f} m\n")
        elif status == "NO_RESULTS":
            print(f"  -> no water feature found within {SEARCH_RADIUS_M} m\n")
        elif status == "QUERY_FAILED":
            print(f"  -> QUERY FAILED after all mirrors/retries — try again later or "
                  f"increase SEARCH_RADIUS_M\n")
        else:
            print(f"  -> unexpected status: {status}\n")

        if i < len(POINTS) - 1:
            time.sleep(DELAY_BETWEEN_POINTS_S)

    treatment_dist, treatment_status = results.get("Treatment (Núñez de Balboa)", (None, "MISSING"))

    print("=" * 70)
    if treatment_status != "OK":
        print(f"Treatment site water-distance check did not succeed (status: "
              f"{treatment_status}). Cannot compute comparison ratios. Re-run later — "
              "the public Overpass instance may be temporarily overloaded.")
        return

    print(f"Treatment reference distance: {treatment_dist:.0f} m\n")
    for label, (dist, status) in results.items():
        if label.startswith("Treatment"):
            continue
        if status == "QUERY_FAILED":
            print(f"{label}: query failed — re-run later, no result to compare.")
            continue
        if status == "NO_RESULTS":
            print(f"{label}: no water feature within {SEARCH_RADIUS_M} m — "
                  "NOT comparable (treatment has closer water access).")
            continue
        ratio = dist / treatment_dist if treatment_dist > 0 else float("inf")
        same_order = 0.1 <= ratio <= 10
        verdict = "OK — same order of magnitude" if same_order else "MISMATCH — check manually"
        print(f"{label}: {dist:.0f} m (ratio {ratio:.2f}x treatment) -> {verdict}")

    print(
        "\nCaveats: 'same order of magnitude' uses a placeholder tolerance (ratio "
        "0.1x-10x) — tighten if stricter comparison is desired. Query covers rivers, "
        "streams, canals and mapped water polygons only; does not include water bodies "
        "mapped as OSM relations (multipolygons), which are rare for small streams but "
        "possible for larger reservoirs."
    )


if __name__ == "__main__":
    main()
