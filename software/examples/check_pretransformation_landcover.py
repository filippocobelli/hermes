"""
Case 001 (Núñez de Balboa) — Pre-transformation land cover check.

Núñez de Balboa broke ground in March 2019 (power-technology.com). This
fetches a true-color Landsat crop over the treatment footprint from BEFORE
that date, to visually establish what land cover existed prior to the
transformation — needed for control-area matching (HYPOTHESES.md Section 2)
and still an open item in case-001-nunez-de-balboa.md.

Uses Landsat (not Sentinel-2) for consistency with RP001's official data
source (ADR-002) and because Landsat 8 has reliable Collection 2 Level-2
coverage back to 2013, well before this site existed.

Usage:
    python examples/check_pretransformation_landcover.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import planetary_computer
import pystac_client
import rasterio
from PIL import Image
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds

PC_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

# Same bbox used for Case 001 (treatment footprint + margin)
CASE_001_BBOX = (-6.2657, 38.4227, -6.1857, 38.4827)

# Pre-construction window: groundbreaking was March 2019
PRE_TRANSFORMATION_START = "2015-01-01"
PRE_TRANSFORMATION_END = "2018-12-31"

OUTPUT_DIR = Path("data/case_001_verification")


def read_window_remote(href: str, bbox_wgs84: tuple[float, float, float, float]) -> np.ndarray:
    with rasterio.open(href) as src:
        left, bottom, right, top = transform_bounds("EPSG:4326", src.crs, *bbox_wgs84)
        window = from_bounds(left, bottom, right, top, transform=src.transform)
        return src.read(1, window=window)


def stretch(band: np.ndarray, low: float = 2, high: float = 98) -> np.ndarray:
    lo, hi = np.percentile(band, [low, high])
    band = np.clip((band.astype(np.float32) - lo) / max(hi - lo, 1e-6), 0, 1)
    return (band * 255).astype(np.uint8)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    client = pystac_client.Client.open(PC_STAC_URL, modifier=planetary_computer.sign_inplace)
    search = client.search(
        collections=["landsat-c2-l2"],
        bbox=CASE_001_BBOX,
        datetime=f"{PRE_TRANSFORMATION_START}/{PRE_TRANSFORMATION_END}",
        query={"eo:cloud_cover": {"lt": 15}, "platform": {"in": ["landsat-8"]}},
    )
    items = sorted(list(search.items()), key=lambda it: it.properties.get("eo:cloud_cover", 100))

    if not items:
        print("No low-cloud Landsat 8 scenes found in 2015-2018. Widening cloud threshold...")
        search = client.search(
            collections=["landsat-c2-l2"],
            bbox=CASE_001_BBOX,
            datetime=f"{PRE_TRANSFORMATION_START}/{PRE_TRANSFORMATION_END}",
            query={"platform": {"in": ["landsat-8"]}},
        )
        items = sorted(list(search.items()), key=lambda it: it.properties.get("eo:cloud_cover", 100))

    if not items:
        print("No pre-transformation Landsat 8 scenes found at all for this bbox/window.")
        return

    best = items[0]
    print(f"Selected PRE-transformation scene: {best.id} | "
          f"cloud_cover={best.properties.get('eo:cloud_cover')} | {best.datetime}")

    red = read_window_remote(best.assets["red"].href, CASE_001_BBOX)
    green = read_window_remote(best.assets["green"].href, CASE_001_BBOX)
    blue = read_window_remote(best.assets["blue"].href, CASE_001_BBOX)

    rgb = np.dstack([stretch(red), stretch(green), stretch(blue)])
    png_path = OUTPUT_DIR / f"pre_transformation_{best.id}.png"
    Image.fromarray(rgb).save(png_path)

    print(f"\nSaved pre-transformation true-color image to: {png_path}")
    print(f"Scene date: {best.datetime} — compare this land cover against candidates "
          "C1-C5 from select_case001_control_points.py.")


if __name__ == "__main__":
    main()
