"""Layer 1 — Data Acquisition.

Responsible for retrieving raw data from external sources (satellite imagery,
public datasets, APIs). Must never modify original datasets (see
foundation/FOUNDATION.md -> Data Principles). Store provenance for every
acquired dataset.

Backend is abstracted behind DataSource (see ADR-003) so it can be swapped
(e.g. Planetary Computer -> USGS M2M) without touching Layers 2-6.
"""

from hermes.acquisition.base import AcquiredScene, AcquisitionRequest, DataSource

__all__ = ["AcquiredScene", "AcquisitionRequest", "DataSource"]
