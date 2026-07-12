"""Layer 2 — Landsat Collection 2 L2 scale/offset conversion and QA masking.

Reference: USGS Landsat Collection 2 Level-2 Science Product Guide.

Surface Temperature (ST) band: DN -> Kelvin via ST_SCALE/ST_OFFSET.
Surface Reflectance (SR) bands: DN -> reflectance [0,1] via SR_SCALE/SR_OFFSET.
QA_PIXEL: bit-packed quality flags; a conservative clear-sky mask rejects
Fill, Dilated Cloud, Cirrus, Cloud, Cloud Shadow, and Snow (bits 0-5).
"""

from __future__ import annotations

import numpy as np

ST_SCALE = 0.00341802
ST_OFFSET = 149.0  # Kelvin

SR_SCALE = 0.0000275
SR_OFFSET = -0.2

# QA_PIXEL bits to reject: Fill(0), Dilated Cloud(1), Cirrus(2), Cloud(3),
# Cloud Shadow(4), Snow(5). Any of these set -> pixel excluded.
QA_REJECT_MASK = 0b0000000000111111


def st_dn_to_kelvin(dn: np.ndarray) -> np.ndarray:
    """Convert raw Surface Temperature DN values to Kelvin."""
    return dn.astype(np.float64) * ST_SCALE + ST_OFFSET


def kelvin_to_celsius(k: np.ndarray) -> np.ndarray:
    return k - 273.15


def sr_dn_to_reflectance(dn: np.ndarray) -> np.ndarray:
    """Convert raw Surface Reflectance DN values to reflectance [0, 1]."""
    refl = dn.astype(np.float64) * SR_SCALE + SR_OFFSET
    return np.clip(refl, 0.0, 1.0)


def qa_clear_mask(qa_pixel: np.ndarray) -> np.ndarray:
    """Boolean mask, True where the pixel is clear (no fill/cloud/cirrus/
    shadow/snow flags set in QA_PIXEL)."""
    return (qa_pixel.astype(np.uint16) & QA_REJECT_MASK) == 0
