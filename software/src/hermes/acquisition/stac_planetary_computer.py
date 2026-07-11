"""Layer 1 — Data Acquisition: Microsoft Planetary Computer STAC backend.

Per ADR-003, this is the initial acquisition backend for RP001 (Landsat
Collection 2 Level-2). Kept behind the DataSource interface (see base.py)
so it can be swapped for an official USGS M2M backend later without
touching downstream layers.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import planetary_computer
import pystac_client
import requests

from hermes.acquisition.base import AcquiredScene, AcquisitionRequest, DataSource

PC_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

# Assets needed for LST (lwir11, qa_pixel) and albedo/NDVI (optical bands),
# per HYPOTHESES.md Section 4.
REQUIRED_ASSETS = [
    "lwir11",
    "qa_pixel",
    "red",
    "green",
    "blue",
    "nir08",
    "swir16",
    "swir22",
]


class PlanetaryComputerDataSource(DataSource):
    """DataSource implementation backed by Microsoft Planetary Computer's STAC API."""

    def __init__(self, stac_url: str = PC_STAC_URL) -> None:
        self._client = pystac_client.Client.open(
            stac_url, modifier=planetary_computer.sign_inplace
        )
        self._stac_url = stac_url

    def search(self, request: AcquisitionRequest) -> list[AcquiredScene]:
        search = self._client.search(
            collections=[request.collection],
            bbox=request.bbox,
            datetime=f"{request.start_date.isoformat()}/{request.end_date.isoformat()}",
            query={"eo:cloud_cover": {"lt": request.max_cloud_cover}},
        )

        scenes: list[AcquiredScene] = []
        for item in search.items():
            assets = {
                name: item.assets[name].href
                for name in REQUIRED_ASSETS
                if name in item.assets
            }
            if not assets:
                continue

            scenes.append(
                AcquiredScene(
                    scene_id=item.id,
                    datetime_utc=item.datetime.isoformat() if item.datetime else "",
                    cloud_cover=item.properties.get("eo:cloud_cover", -1),
                    assets=assets,
                    source=f"planetary-computer:{request.collection}",
                    provenance={
                        "stac_url": self._stac_url,
                        "collection": request.collection,
                        "item_id": item.id,
                        "item_self_href": item.get_self_href(),
                        "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    },
                )
            )
        return scenes

    def download(self, scene: AcquiredScene, dest_dir: Path) -> Path:
        scene_dir = dest_dir / scene.scene_id
        scene_dir.mkdir(parents=True, exist_ok=True)

        checksums: dict[str, str] = {}
        local_paths: dict[str, str] = {}

        for asset_name, url in scene.assets.items():
            local_path = scene_dir / f"{asset_name}.tif"
            if not local_path.exists():
                _download_file(url, local_path)
            checksums[asset_name] = _sha256(local_path)
            local_paths[asset_name] = str(local_path)

        provenance_record = {
            **scene.provenance,
            "scene_id": scene.scene_id,
            "source": scene.source,
            "datetime_utc": scene.datetime_utc,
            "cloud_cover": scene.cloud_cover,
            "downloaded_at": datetime.now(timezone.utc).isoformat(),
            "local_assets": local_paths,
            "checksums_sha256": checksums,
        }
        provenance_path = scene_dir / "provenance.json"
        provenance_path.write_text(json.dumps(provenance_record, indent=2))

        return scene_dir


def _download_file(url: str, dest: Path) -> None:
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
