"""
Case 001 — Pilot extraction: LST, NDVI, albedo per site per date.

Validates the end-to-end pipeline (HYPOTHESES.md Section 5.6: Case 001 is
a pilot / proof-of-methodology, not a standalone confirmatory result).

For each qualifying Landsat scene (low cloud cover, within the pilot date
range), reads each required band ONCE over the combined bounding box of
all three sites (treatment clean zone + 2 control buffers) via remote
windowed reads (no full-scene download). Each site's own polygon is then
used to mask that shared crop, keeping the extraction efficient: ~7 band
reads per date instead of ~21.

Per site/date: QA-clear + in-polygon pixels only; median LST (deg C),
NDVI, and albedo; season classification (JJA/DJF/transition, per
HYPOTHESES.md Section 4.4).

Output: a tidy CSV, one row per site per observation date — this is the
analysis-ready dataset for the Section 5 mixed-effects model (Layers 4-5,
not yet built).

Usage:
    python examples/run_case001_pilot_extraction.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np
import planetary_computer
import pystac_client
import rasterio
from rasterio.features import geometry_mask
from rasterio.warp import transform_bounds, transform_geom
from rasterio.windows import from_bounds
from shapely.geometry import shape

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from hermes.normalisation.landsat_qa import (  # noqa: E402
    kelvin_to_celsius,
    qa_clear_mask,
    sr_dn_to_reflectance,
    st_dn_to_kelvin,
)
from hermes.normalisation.landsat_optical import compute_broadband_albedo, compute_ndvi  # noqa: E402
from hermes.normalisation.season import classify_season  # noqa: E402

PC_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

GEOM_DIR = Path("../research_programs/RP001-surface-transformation-energy-balance/cases/geometries")
SITE_FILES = {
    "treatment": "treatment_clean_zone.geojson",
    "control_1_C5": "control_1_C5.geojson",
    "control_2_C1": "control_2_C1.geojson",
}

PILOT_START = "2023-01-01"
PILOT_END = "2025-12-31"
MAX_CLOUD_COVER = 20.0

REQUIRED_BANDS = ["lwir11", "qa_pixel", "red", "blue", "nir08", "swir16", "swir22"]

OUTPUT_CSV = Path("data/case_001_pilot_extraction.csv")


def load_site_geometries() -> dict[str, dict]:
    sites = {}
    for site_id, filename in SITE_FILES.items():
        feature = json.loads((GEOM_DIR / filename).read_text())
        sites[site_id] = feature
    return sites


def union_bbox(sites: dict[str, dict], pad_deg: float = 0.01) -> tuple[float, float, float, float]:
    geoms = [shape(f["geometry"]) for f in sites.values()]
    for site_id, g in zip(sites.keys(), geoms):
        if g.is_empty or g.area <= 0:
            raise RuntimeError(
                f"Site '{site_id}' has an empty/zero-area geometry — its GeoJSON is likely "
                "corrupt (e.g. from a prior failed export run). Re-run "
                "export_case001_geometries.py before retrying this script."
            )
    lons, lats = [], []
    for g in geoms:
        minx, miny, maxx, maxy = g.bounds
        lons += [minx, maxx]
        lats += [miny, maxy]
    bbox = (min(lons) - pad_deg, min(lats) - pad_deg, max(lons) + pad_deg, max(lats) + pad_deg)
    if any(v != v for v in bbox):  # NaN check (NaN != NaN is True)
        raise RuntimeError(f"Computed bbox contains NaN: {bbox}. Aborting before STAC query.")
    return bbox


def read_band_window(href: str, bbox_wgs84: tuple[float, float, float, float]):
    """Read one band over bbox via remote windowed read. Returns (array, transform, crs)."""
    with rasterio.open(href) as src:
        left, bottom, right, top = transform_bounds("EPSG:4326", src.crs, *bbox_wgs84)
        window = from_bounds(left, bottom, right, top, transform=src.transform)
        win_transform = src.window_transform(window)
        data = src.read(1, window=window)
        return data, win_transform, src.crs


def site_mask(geometry_wgs84: dict, shape_hw: tuple[int, int], transform, crs) -> np.ndarray:
    """Boolean mask, True INSIDE the site polygon, for a given array shape/transform/crs."""
    geom_in_crs = transform_geom("EPSG:4326", crs.to_string(), geometry_wgs84)
    return geometry_mask([geom_in_crs], transform=transform, invert=True, out_shape=shape_hw)


def main() -> None:
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    print("Loading site geometries...")
    sites = load_site_geometries()
    for site_id, feature in sites.items():
        area_ha = feature["properties"].get("area_ha", "?")
        print(f"  {site_id}: {area_ha} ha")

    bbox = union_bbox(sites)
    print(f"\nCombined search bbox: {bbox}")

    client = pystac_client.Client.open(PC_STAC_URL, modifier=planetary_computer.sign_inplace)
    search = client.search(
        collections=["landsat-c2-l2"],
        bbox=bbox,
        datetime=f"{PILOT_START}/{PILOT_END}",
        query={
            "eo:cloud_cover": {"lt": MAX_CLOUD_COVER},
            "platform": {"in": ["landsat-8", "landsat-9"]},
        },
    )
    items = list(search.items())
    print(f"Found {len(items)} candidate scenes (cloud < {MAX_CLOUD_COVER}%).\n")

    rows = []
    for i, item in enumerate(items, 1):
        scene_date = item.datetime.date()
        season = classify_season(scene_date)
        print(f"[{i}/{len(items)}] {item.id} | {scene_date} | {season} | "
              f"cloud={item.properties.get('eo:cloud_cover'):.1f}%")

        try:
            bands = {}
            transform_ref = None
            crs_ref = None
            shape_ref = None
            for band_name in REQUIRED_BANDS:
                href = item.assets[band_name].href
                data, win_transform, crs = read_band_window(href, bbox)
                bands[band_name] = data
                if transform_ref is None:
                    transform_ref, crs_ref, shape_ref = win_transform, crs, data.shape
        except Exception as exc:
            print(f"    Skipping scene (read error: {exc})")
            continue

        clear = qa_clear_mask(bands["qa_pixel"])
        lst_c = kelvin_to_celsius(st_dn_to_kelvin(bands["lwir11"]))
        red = sr_dn_to_reflectance(bands["red"])
        blue = sr_dn_to_reflectance(bands["blue"])
        nir = sr_dn_to_reflectance(bands["nir08"])
        swir16 = sr_dn_to_reflectance(bands["swir16"])
        swir22 = sr_dn_to_reflectance(bands["swir22"])
        ndvi = compute_ndvi(red, nir)
        albedo = compute_broadband_albedo(blue, red, nir, swir16, swir22)

        for site_id, feature in sites.items():
            try:
                in_site = site_mask(feature["geometry"], shape_ref, transform_ref, crs_ref)
            except Exception as exc:
                print(f"    {site_id}: mask error ({exc}), skipping")
                continue

            valid = clear & in_site
            n_valid = int(valid.sum())
            if n_valid == 0:
                continue

            row = {
                "site_id": site_id,
                "date": scene_date.isoformat(),
                "season": season,
                "scene_id": item.id,
                "platform": item.properties.get("platform"),
                "n_valid_pixels": n_valid,
                "lst_c_median": float(np.nanmedian(lst_c[valid])),
                "ndvi_median": float(np.nanmedian(ndvi[valid])),
                "albedo_median": float(np.nanmedian(albedo[valid])),
            }
            rows.append(row)
            print(f"    {site_id}: n={n_valid} pixels, LST={row['lst_c_median']:.2f}C, "
                  f"NDVI={row['ndvi_median']:.3f}, albedo={row['albedo_median']:.3f}")

    if not rows:
        print("\nNo valid observations extracted. Check date range / cloud threshold.")
        return

    fieldnames = list(rows[0].keys())
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved {len(rows)} site-date observations to: {OUTPUT_CSV}")

    by_site_season: dict[tuple[str, str], int] = {}
    for r in rows:
        key = (r["site_id"], r["season"])
        by_site_season[key] = by_site_season.get(key, 0) + 1

    print("\nObservation counts by site / season:")
    for (site_id, season), count in sorted(by_site_season.items()):
        print(f"  {site_id:20s} | {season:10s} | {count} dates")


if __name__ == "__main__":
    main()
