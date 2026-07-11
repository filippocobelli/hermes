"""Layer 1 — Data Acquisition: abstract interface.

Any concrete data source (STAC/Planetary Computer, USGS M2M, etc.) must
implement this interface. This isolation is required by ADR-003: the
acquisition backend must be swappable without touching downstream layers
(Layers 2-6 depend only on AcquiredScene / DataSource, never on a specific
provider).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


@dataclass
class AcquisitionRequest:
    """A request for scenes matching given spatial/temporal/quality criteria."""

    bbox: tuple[float, float, float, float]  # min_lon, min_lat, max_lon, max_lat
    start_date: date
    end_date: date
    max_cloud_cover: float = 20.0  # percent
    collection: str = "landsat-c2-l2"


@dataclass
class AcquiredScene:
    """A scene found by a DataSource.search() call. Not yet downloaded."""

    scene_id: str
    datetime_utc: str
    cloud_cover: float
    assets: dict[str, str]  # asset name -> remote URL
    source: str  # e.g. "planetary-computer:landsat-c2-l2"
    provenance: dict = field(default_factory=dict)


class DataSource(ABC):
    """Abstract interface for Layer 1 acquisition backends.

    Per foundation Data Principles: implementations must never modify
    original datasets, and must record provenance for every acquired scene.
    """

    @abstractmethod
    def search(self, request: AcquisitionRequest) -> list[AcquiredScene]:
        """Search for available scenes matching the request. Does not download."""
        raise NotImplementedError

    @abstractmethod
    def download(self, scene: AcquiredScene, dest_dir: Path) -> Path:
        """Download the required assets for a scene into dest_dir.

        Must write a provenance.json alongside the downloaded assets and
        must never modify the original asset content. Returns the path to
        the scene's local directory.
        """
        raise NotImplementedError
