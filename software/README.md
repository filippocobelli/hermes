# HERMES — Software

- **Document ID:** HERMES-SW-000
- **Version:** 0.1.0
- **Status:** Draft for Review
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Systems Architect role)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** N/A (infrastructure)
- **Related ADR:** N/A
- **License:** TBD

---

## Purpose

Software implementation of the HERMES framework, structured per the layers defined in
[`foundation/008_SYSTEM_ARCHITECTURE.md`](../foundation/008_SYSTEM_ARCHITECTURE.md).

No research program logic lives here yet — this is bootstrap infrastructure only.

## Layer Mapping

| Layer | Directory | Status |
|---|---|---|
| 1 — Data Acquisition | `src/hermes/acquisition/` | Placeholder |
| 2 — Data Normalisation | `src/hermes/normalisation/` | Placeholder |
| 3 — Spatial Database | `src/hermes/database/` | Placeholder + Docker Compose |
| 4 — Scientific Models | `src/hermes/models/` | Placeholder |
| 5 — Statistical Analysis | `src/hermes/analysis/` | Placeholder |
| 6 — Reporting | `src/hermes/reporting/` | Placeholder |

## Requirements

- Python ≥ 3.11
- Docker (for PostgreSQL/PostGIS)

## Setup

```bash
cd software
cp .env.example .env
docker compose up -d
python -m venv .venv
source .venv/bin/activate
pip install -e .
python bootstrap.py
```

`bootstrap.py` verifies the environment (Python version, required env vars, database
connectivity) and reports status. It does not run any scientific code.

## Traceability

Per `foundation/008_SYSTEM_ARCHITECTURE.md` § Scientific Traceability, every future analysis
output must identify: Research Question, Dataset, Algorithm, Configuration, Software Version,
Git Commit. This will be enforced once Layer 4/5 modules exist — not yet applicable to
bootstrap-only code.

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial bootstrap scaffold |
