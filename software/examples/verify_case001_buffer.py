"""
Verify Case 001 (Núñez de Balboa) — Criterion 4 visual check.

Reads a small windowed crop DIRECTLY from remote Cloud-Optimized GeoTIFFs via
HTTP range requests — no full-scene download needed. This is dramatically
faster than downloading an entire Landsat/Sentinel scene (hundreds of MB)
just to look at a few square kilometres.

Uses Sentinel-2 L2A (10 m resolution) rather than Landsat for this specific
visual QA check: Landsat remains the official RP001 data source (ADR-002),
but Sentinel-2's finer resolution makes small-scale visual inspection (e.g.
"is there another development within 2 km?") much easier for a human to
read. This script does NOT feed into the scientific pipeline — it is a
QA/visual-inspection tool only.

Usage:
    python examples/verify_case001_buffer.py
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import numpy as np
import planetary_computer
import pystac_client
import rasterio
from PIL import Image
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds

PC_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

# Case 001 - Núñez de Balboa
# See research_programs/RP001-surface-transformation-energy-balance/cases/case-001-nunez-de-balboa.md
# Padded wider than the plant footprint alone, to visually cover the 2 km
# Criterion 4 buffer with margin.
CASE_001_BBOX = (-6.30, 38.40, -6.15, 38.51)  # min_lon, min_lat, max_lon, max_lat

OUTPUT_DIR = Path("data/case_001_verification")


def read_window_remote(
    href: str, bbox_wgs84: tuple[float, float, float, float]
) -> np.ndarray:
    """Read a single band cropped to a WGS84 bbox directly from a remote COG,
    without downloading the full file (GDAL /vsicurl + HTTP range requests)."""
    with rasterio.open(href) as src:
        left, bottom, right, top = transform_bounds("EPSG:4326", src.crs, *bbox_wgs84)
        window = from_bounds(left, bottom, right, top, transform=src.transform)
        return src.read(1, window=window)


def stretch(band: np.ndarray, low: float = 2, high: float = 98) -> np.ndarray:
    """Simple percentile stretch to 0-255, for visualization only."""
    lo, hi = np.percentile(band, [low, high])
    band = np.clip((band.astype(np.float32) - lo) / max(hi - lo, 1e-6), 0, 1)
    return (band * 255).astype(np.uint8)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    client = pystac_client.Client.open(
        PC_STAC_URL, modifier=planetary_computer.sign_inplace
    )

    search = client.search(
        collections=["sentinel-2-l2a"],
        bbox=CASE_001_BBOX,
        datetime="2024-01-01/2025-12-31",
        query={"eo:cloud_cover": {"lt": 5}},
    )
    items = list(search.items())
    if not items:
        print("No low-cloud Sentinel-2 scenes found. Widen the date range or cloud threshold.")
        return

    items.sort(key=lambda it: it.properties.get("eo:cloud_cover", 100))
    best = items[0]
    print(
        f"Selected scene: {best.id} | "
        f"cloud_cover={best.properties.get('eo:cloud_cover')} | {best.datetime}"
    )

    red_href = best.assets["B04"].href
    green_href = best.assets["B03"].href
    blue_href = best.assets["B02"].href

    print("Reading windowed crop directly from remote COGs (no full download)...")
    red = read_window_remote(red_href, CASE_001_BBOX)
    green = read_window_remote(green_href, CASE_001_BBOX)
    blue = read_window_remote(blue_href, CASE_001_BBOX)

    rgb = np.dstack([stretch(red), stretch(green), stretch(blue)])

    png_path = OUTPUT_DIR / f"true_color_preview_case001_{best.id}.png"
    Image.fromarray(rgb).save(png_path)

    print(f"\nTrue-color preview saved to: {png_path}")
    print(
        "Open this PNG and visually inspect the surroundings of the plant footprint "
        "for other large-scale anthropogenic transformations "
        "(HYPOTHESES.md Section 1, Criterion 4)."
    )


if __name__ == "__main__":
    main()
