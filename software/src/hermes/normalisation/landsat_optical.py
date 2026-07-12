"""Layer 2 — Vegetation index and broadband albedo from Landsat surface reflectance.

NDVI: standard normalized difference vegetation index.
Albedo: Liang (2001) narrowband-to-broadband shortwave albedo conversion
for Landsat-class sensors ("Narrowband to broadband conversions of land
surface albedo I: Algorithms", Remote Sensing of Environment, 76(2)).

Caveat (HYPOTHESES.md Section 4.3): over post-construction treatment
pixels, NDVI reflects a mixed panel+soil+inter-row-vegetation optical
signature, not clean vegetation cover. NDVI/albedo here are computed
identically for treatment and control pixels; the interpretation
difference is a modelling/analysis concern, not a computation one.
"""

from __future__ import annotations

import numpy as np


def compute_ndvi(red: np.ndarray, nir: np.ndarray) -> np.ndarray:
    denom = nir + red
    with np.errstate(divide="ignore", invalid="ignore"):
        ndvi = np.where(denom != 0, (nir - red) / denom, np.nan)
    return ndvi


def compute_broadband_albedo(
    blue: np.ndarray,
    red: np.ndarray,
    nir: np.ndarray,
    swir16: np.ndarray,
    swir22: np.ndarray,
) -> np.ndarray:
    """Liang (2001) simplified shortwave albedo formula (Landsat bands)."""
    return (
        0.356 * blue
        + 0.130 * red
        + 0.373 * nir
        + 0.085 * swir16
        + 0.072 * swir22
        - 0.0018
    )
