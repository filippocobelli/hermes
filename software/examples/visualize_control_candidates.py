"""
Case 001 (Núñez de Balboa) — Visualize treatment site + control candidates.

Fetches one Sentinel-2 true-color crop covering the treatment site and all
control area candidates from select_case001_control_points.py, and marks
each location directly on the image — so land cover can be checked for all
candidates at once instead of opening separate map links.

Usage:
    python examples/visualize_control_candidates.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import planetary_computer
import pystac_client
import rasterio
from PIL import Image, ImageDraw, ImageFont
from rasterio.transform import rowcol
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds

PC_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

TREATMENT = (38.4533, -6.2260, "Treatment")

# Candidates from select_case001_control_points.py output
CANDIDATES = [
    (38.43534, -6.17401, "C1"),
    (38.40706, -6.19020, "C2"),
    (38.39607, -6.22706, "C3"),
    (38.40879, -6.26301, "C4"),
    (38.43507, -6.16257, "C5"),
]

# Bbox covering treatment + all candidates, with margin
BBOX = (-6.30, 38.38, -6.14, 38.46)  # min_lon, min_lat, max_lon, max_lat

OUTPUT_DIR = Path("data/case_001_verification")


def stretch(band: np.ndarray, low: float = 2, high: float = 98) -> np.ndarray:
    lo, hi = np.percentile(band, [low, high])
    band = np.clip((band.astype(np.float32) - lo) / max(hi - lo, 1e-6), 0, 1)
    return (band * 255).astype(np.uint8)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    client = pystac_client.Client.open(PC_STAC_URL, modifier=planetary_computer.sign_inplace)
    search = client.search(
        collections=["sentinel-2-l2a"],
        bbox=BBOX,
        datetime="2024-01-01/2025-12-31",
        query={"eo:cloud_cover": {"lt": 5}},
    )
    items = sorted(list(search.items()), key=lambda it: it.properties.get("eo:cloud_cover", 100))
    if not items:
        print("No low-cloud Sentinel-2 scenes found.")
        return

    best = items[0]
    print(f"Selected scene: {best.id} | cloud_cover={best.properties.get('eo:cloud_cover')}")

    red_href = best.assets["B04"].href
    green_href = best.assets["B03"].href
    blue_href = best.assets["B02"].href

    with rasterio.open(red_href) as src:
        left, bottom, right, top = transform_bounds("EPSG:4326", src.crs, *BBOX)
        window = from_bounds(left, bottom, right, top, transform=src.transform)
        win_transform = src.window_transform(window)
        red = src.read(1, window=window)
        crs = src.crs

    with rasterio.open(green_href) as src:
        window = from_bounds(*transform_bounds("EPSG:4326", src.crs, *BBOX), transform=src.transform)
        green = src.read(1, window=window)

    with rasterio.open(blue_href) as src:
        window = from_bounds(*transform_bounds("EPSG:4326", src.crs, *BBOX), transform=src.transform)
        blue = src.read(1, window=window)

    rgb = np.dstack([stretch(red), stretch(green), stretch(blue)])
    img = Image.fromarray(rgb).convert("RGB")
    draw = ImageDraw.Draw(img)

    from pyproj import Transformer
    to_crs = Transformer.from_crs("EPSG:4326", crs, always_xy=True).transform

    def mark(lat: float, lon: float, label: str, color: tuple[int, int, int]) -> None:
        x, y = to_crs(lon, lat)
        row, col = rowcol(win_transform, x, y)
        r = 8
        draw.ellipse([col - r, row - r, col + r, row + r], outline=color, width=3)
        draw.text((col + r + 2, row - r), label, fill=color)

    mark(TREATMENT[0], TREATMENT[1], TREATMENT[2], (255, 0, 0))
    for lat, lon, label in CANDIDATES:
        mark(lat, lon, label, (0, 255, 255))

    png_path = OUTPUT_DIR / f"control_candidates_{best.id}.png"
    img.save(png_path)
    print(f"\nSaved annotated image to: {png_path}")
    print("Red circle = treatment site. Cyan circles = control candidates (C1-C5).")


if __name__ == "__main__":
    main()
