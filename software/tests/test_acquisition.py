"""Unit tests for acquisition helpers that do not require network access."""

from pathlib import Path

from hermes.acquisition.stac_planetary_computer import _sha256


def test_sha256_deterministic(tmp_path: Path):
    f = tmp_path / "sample.tif"
    f.write_bytes(b"hermes-test-content")
    h1 = _sha256(f)
    h2 = _sha256(f)
    assert h1 == h2
    assert len(h1) == 64  # sha256 hex digest length


def test_sha256_differs_on_content_change(tmp_path: Path):
    f1 = tmp_path / "a.tif"
    f2 = tmp_path / "b.tif"
    f1.write_bytes(b"content-a")
    f2.write_bytes(b"content-b")
    assert _sha256(f1) != _sha256(f2)
