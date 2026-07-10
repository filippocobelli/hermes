# HERMES
# DOC-008 — System Architecture

- **Document ID:** HERMES-FND-008
- **Version:** 0.1.1
- **Status:** Draft for Review
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Systems Architect role)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** RP001
- **Related ADR:** ADR-001
- **License:** TBD (see foundation license decision)

---

## Purpose

This document defines the architectural principles of the HERMES framework.

## Architectural Vision

HERMES is a modular scientific framework.

Scientific questions drive the software architecture.

Software is an implementation of documented research questions.

## Core Components

Foundation

Research Programs

Software

Datasets

Validation

Publications

## Software Layers

Layer 1 — Data Acquisition

Layer 2 — Data Normalisation

Layer 3 — Spatial Database

Layer 4 — Scientific Models

Layer 5 — Statistical Analysis

Layer 6 — Reporting

## Repository Layout

```
foundation/
governance/
research_programs/
software/
datasets/
documentation/
publications/
tests/
tools/
```

## Design Principles

- Modularity
- Reproducibility
- Explainability
- Traceability
- Testability

## Technology Stack (initial proposal)

Python

PostgreSQL/PostGIS

Docker

GitHub

MkDocs Material

GitHub Actions

Jupyter

## Scientific Traceability

Every output must identify:

- Research Question
- Dataset
- Algorithm
- Configuration
- Software Version
- Git Commit

## Validation

No software module is considered complete without:

- unit tests
- documentation
- reproducible example

## Future Evolution

The architecture shall evolve through ADR documents only.

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial draft |
| 0.1.1 | 2026-07-10 | Added mandatory metadata block, linked ADR-001, added change log |
