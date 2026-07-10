"""Minimal tests for bootstrap.py — check logic only, no live DB required."""

import os

from bootstrap import check_env_vars, check_python, MIN_PYTHON


def test_check_python_ok():
    ok, version = check_python()
    assert ok is True
    assert isinstance(version, str)


def test_check_env_vars_missing(monkeypatch):
    for var in ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]:
        monkeypatch.delenv(var, raising=False)
    ok, missing = check_env_vars()
    assert ok is False
    assert set(missing) == {"DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"}


def test_check_env_vars_present(monkeypatch):
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "hermes")
    monkeypatch.setenv("DB_USER", "hermes")
    monkeypatch.setenv("DB_PASSWORD", "hermes")
    ok, missing = check_env_vars()
    assert ok is True
    assert missing == []
