"""
Example: search for Landsat Collection 2 Level-2 scenes via Planetary Computer.

This performs a SEARCH only (no download) so it is safe to run as a quick
connectivity/config check.

Usage:
    python examples/search_landsat_example.py
"""

from datetime import date

from hermes.acquisition.base import AcquisitionRequest
from hermes.acquisition.stac_planetary_computer import PlanetaryComputerDataSource


def main() -> None:
    source = PlanetaryComputerDataSource()

    # Example bbox: a small area, placeholder coordinates - replace with a
    # real RP001 case site once Section 1 case selection is finalised.
    request = AcquisitionRequest(
        bbox=(11.10, 43.10, 11.20, 43.20),  # example: Chiusdino area, Tuscany
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        max_cloud_cover=20.0,
    )

    scenes = source.search(request)

    print(f"Found {len(scenes)} scenes matching request.")
    for scene in scenes[:5]:
        print(f"- {scene.scene_id} | {scene.datetime_utc} | cloud_cover={scene.cloud_cover}")


if __name__ == "__main__":
    main()
