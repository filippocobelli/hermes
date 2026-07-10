"""
HERMES — Bootstrap check.

Verifies the local environment is correctly configured before any
research program code is run. Does not execute any scientific logic.

Usage:
    python bootstrap.py
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field

from dotenv import load_dotenv


REQUIRED_ENV_VARS = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
MIN_PYTHON = (3, 11)


@dataclass
class BootstrapReport:
    python_ok: bool = False
    python_version: str = ""
    env_vars_ok: bool = False
    missing_env_vars: list[str] = field(default_factory=list)
    db_ok: bool = False
    db_error: str = ""

    @property
    def all_ok(self) -> bool:
        return self.python_ok and self.env_vars_ok and self.db_ok


def check_python() -> tuple[bool, str]:
    version = sys.version_info
    ok = version >= MIN_PYTHON
    return ok, f"{version.major}.{version.minor}.{version.micro}"


def check_env_vars() -> tuple[bool, list[str]]:
    missing = [v for v in REQUIRED_ENV_VARS if not os.getenv(v)]
    return (len(missing) == 0), missing


def check_database() -> tuple[bool, str]:
    try:
        import psycopg

        conn_str = (
            f"host={os.getenv('DB_HOST')} "
            f"port={os.getenv('DB_PORT')} "
            f"dbname={os.getenv('DB_NAME')} "
            f"user={os.getenv('DB_USER')} "
            f"password={os.getenv('DB_PASSWORD')}"
        )
        with psycopg.connect(conn_str, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        return True, ""
    except Exception as exc:  # noqa: BLE001 — bootstrap-level diagnostic only
        return False, str(exc)


def run() -> BootstrapReport:
    load_dotenv()
    report = BootstrapReport()

    report.python_ok, report.python_version = check_python()
    report.env_vars_ok, report.missing_env_vars = check_env_vars()

    if report.env_vars_ok:
        report.db_ok, report.db_error = check_database()

    return report


def print_report(report: BootstrapReport) -> None:
    print("HERMES — Bootstrap Check")
    print("-" * 40)
    print(f"Python version : {report.python_version} "
          f"({'OK' if report.python_ok else f'FAIL — requires >= {MIN_PYTHON[0]}.{MIN_PYTHON[1]}'})")

    if report.env_vars_ok:
        print("Env variables  : OK")
    else:
        print(f"Env variables  : FAIL — missing {', '.join(report.missing_env_vars)}")

    if not report.env_vars_ok:
        print("Database       : SKIPPED (env vars missing)")
    elif report.db_ok:
        print("Database       : OK (connected)")
    else:
        print(f"Database       : FAIL — {report.db_error}")

    print("-" * 40)
    print("Result: PASS" if report.all_ok else "Result: FAIL")


if __name__ == "__main__":
    result = run()
    print_report(result)
    sys.exit(0 if result.all_ok else 1)
