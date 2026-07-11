"""
Case 001 (Núñez de Balboa) — Criterion 4 verification via OpenStreetMap Overpass API.

Per Foundation Core Principles ("Evidence before belief", "Method before
conclusion"), this replaces subjective visual estimation from satellite
imagery with a reproducible, vector-based check: it queries OpenStreetMap
for tagged power/industrial infrastructure within a search radius around
the Case 001 centroid and computes exact great-circle distances.

This is a verification tool for HYPOTHESES.md Section 1, Criterion 4
("no concurrent confounding transformation within a defined buffer
radius"). It does not itself decide Case 001's status — it produces
evidence that must be recorded in the case document.

Usage:
    python examples/check_case001_confounders.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Case 001 - Núñez de Balboa centroid (WGS84)
# See research_programs/RP001-surface-transformation-energy-balance/cases/case-001-nunez-de-balboa.md
CASE_001_CENTROID = (38.4533, -6.2260)  # lat, lon

SEARCH_RADIUS_M = 5000  # wider than the buffer, for context
CRITERION_4_BUFFER_M = 2000


@dataclass
class NearbyFeature:
    osm_type: str
    osm_id: int
    tags: dict
    lat: float
    lon: float
    distance_m: float


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in metres."""
    R = 6371000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def build_query(lat: float, lon: float, radius_m: int) -> str:
    """Tags of interest: any power plant, solar generators specifically,
    and industrial/quarry land use — plausible confounding transformations."""
    return f"""
    [out:json][timeout:60];
    (
      node["power"="plant"](around:{radius_m},{lat},{lon});
      way["power"="plant"](around:{radius_m},{lat},{lon});
      relation["power"="plant"](around:{radius_m},{lat},{lon});

      node["power"="generator"]["generator:source"="solar"](around:{radius_m},{lat},{lon});
      way["power"="generator"]["generator:source"="solar"](around:{radius_m},{lat},{lon});

      way["landuse"="industrial"](around:{radius_m},{lat},{lon});
      way["landuse"="quarry"](around:{radius_m},{lat},{lon});
    );
    out center tags;
    """


def query_overpass(lat: float, lon: float, radius_m: int) -> list[NearbyFeature]:
    query = build_query(lat, lon, radius_m)
    headers = {
        "User-Agent": "HERMES-research-framework/0.1 (https://github.com/filippocobelli/hermes)",
        "Accept": "application/json",
    }
    response = requests.post(
        OVERPASS_URL, data={"data": query}, headers=headers, timeout=90
    )
    response.raise_for_status()
    data = response.json()

    features: list[NearbyFeature] = []
    for el in data.get("elements", []):
        if el["type"] == "node":
            el_lat, el_lon = el["lat"], el["lon"]
        else:
            center = el.get("center")
            if not center:
                continue
            el_lat, el_lon = center["lat"], center["lon"]

        dist = haversine_m(lat, lon, el_lat, el_lon)
        features.append(
            NearbyFeature(
                osm_type=el["type"],
                osm_id=el["id"],
                tags=el.get("tags", {}),
                lat=el_lat,
                lon=el_lon,
                distance_m=dist,
            )
        )
    return sorted(features, key=lambda f: f.distance_m)


def main() -> None:
    lat, lon = CASE_001_CENTROID
    print(
        f"Querying OpenStreetMap (Overpass API) within {SEARCH_RADIUS_M} m of "
        f"Case 001 centroid ({lat}, {lon})...\n"
    )

    features = query_overpass(lat, lon, SEARCH_RADIUS_M)

    if not features:
        print("No tagged power/industrial features found in the search radius.")
        return

    print(f"{'Distance (m)':>12} | {'Type':>10} | {'ID':>12} | Tags")
    print("-" * 90)
    for f in features:
        flag = " ⚠️  WITHIN 2km BUFFER" if f.distance_m <= CRITERION_4_BUFFER_M else ""
        tag_str = ", ".join(
            f"{k}={v}"
            for k, v in f.tags.items()
            if k in ("power", "generator:source", "plant:source", "landuse", "name")
        )
        print(f"{f.distance_m:12.0f} | {f.osm_type:>10} | {f.osm_id:>12} | {tag_str}{flag}")

    within_buffer = [f for f in features if f.distance_m <= CRITERION_4_BUFFER_M]
    print("\n" + "=" * 90)
    if within_buffer:
        print(
            f"⚠️  {len(within_buffer)} feature(s) found WITHIN the {CRITERION_4_BUFFER_M} m "
            "Criterion 4 buffer. Case 001 should NOT be marked Approved until reviewed."
        )
    else:
        print(
            f"✅ No tagged power/industrial features found within {CRITERION_4_BUFFER_M} m. "
            "Criterion 4 provisionally satisfied — subject to the OSM completeness caveat below."
        )

    print(
        "\nCaveat (per Core Principles — record uncertainty): this check is only as "
        "complete as OpenStreetMap's tagging coverage in this area. Absence of a "
        "result is not proof of absence. Cross-check against the Sentinel-2 visual "
        "inspection already performed for this case, and note both in the case "
        "document — do not treat either check alone as final."
    )


if __name__ == "__main__":
    main()
