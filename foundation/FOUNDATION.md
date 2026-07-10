# HERMES
# FND-001 — Foundation

- **Document ID:** HERMES-FND-001
- **Version:** 0.1.0
- **Status:** Draft for Review
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Systems Architect / Lead Technical Writer / Scientific Method Reviewer roles)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** RP001
- **Related ADR:** ADR-001
- **License:** TBD

---

## Executive Summary

HERMES (Holistic Energy Research Model for Environmental Systems) is an open scientific
framework currently in its Foundation phase.

The project does **not** aim to prove or disprove a specific scientific theory.

Its purpose is to develop a transparent, reproducible and verifiable methodology for studying
interactions between anthropogenic activities, land transformation, energy systems and
environmental processes.

The initial research motivation originated from questions regarding photovoltaic installations
and their possible influence on local and regional thermal balance. During project definition
it became clear that limiting the framework to photovoltaic systems would introduce
unnecessary bias (see ADR-001). The scope was therefore generalized into a broader scientific
framework capable of studying any anthropogenic transformation.

## Purpose

To provide an open, reproducible methodology and software ecosystem for studying whether,
and to what extent, anthropogenic land transformation measurably affects environmental
systems — starting with surface energy balance.

## Scope

HERMES studies anthropogenic surface transformations in general, not any single technology.
Photovoltaic installations are one case among several under study (see Initial Motivation).
Scope boundaries and their rationale are recorded in ADR-001.

## Vision

HERMES should become an open scientific framework rather than a single research project.

The framework should be reusable for multiple independent studies concerning environmental
systems.

The software is not the objective. The methodology is the objective. The software is only an
implementation of the methodology.

## Mission

Reduce uncertainty through:

- transparent methods
- open datasets
- reproducible analyses
- independent validation

The framework should allow anyone to reproduce every published result.

## What HERMES Is

- An engineering framework.
- An open science project.
- A reproducible research platform.
- A methodology.
- A software ecosystem.

## What HERMES Is Not

- Not an advocacy project.
- Not an anti-photovoltaic project.
- Not a pro-photovoltaic project.
- Not a political initiative.
- Not an attempt to replace climate science.
- Not a platform for opinions.

## Initial Motivation

The original research question originated from the observation that large anthropogenic
surface transformations may modify local energy balance.

Examples include:

- photovoltaic plants
- logistics hubs
- airports
- industrial districts
- urban expansion
- data centres
- large parking areas
- mining sites
- artificial lakes

The framework should determine whether measurable effects exist, their magnitude and their
statistical significance. The framework shall not assume any conclusion beforehand.

## Scientific Philosophy

Every hypothesis must be:

- measurable
- reproducible
- falsifiable

The framework distinguishes between:

```
Observation
    ↓
Correlation
    ↓
Mechanistic explanation
    ↓
Causal inference
```

Correlation alone shall never be interpreted as causation.

## First Research Program

**RP001 — Surface Transformation and Energy Balance**

Primary Question:

> Does large-scale anthropogenic transformation of land surfaces produce statistically
> significant changes in surface energy balance compared with equivalent control areas
> after controlling for environmental variables?

Full detail: [`research_programs/RP001-surface-transformation-energy-balance/RESEARCH_QUESTION.md`](../research_programs/RP001-surface-transformation-energy-balance/RESEARCH_QUESTION.md)

## Long-Term Research Areas

Future research programs may include:

- Anthropogenic heat sources
- Life-cycle environmental assessment
- Carbon balance
- Urban energy balance
- Water balance
- Atmospheric circulation
- Infrastructure effects
- Land use evolution
- Remote sensing methodologies

## Architectural Principles

Research Questions drive the architecture.

```
Research Question
    ↓
Hypothesis
    ↓
Metrics
    ↓
Datasets
    ↓
Algorithms
    ↓
Validation
    ↓
Publication
```

Software shall always remain subordinate to scientific questions.

Full detail: [`foundation/008_SYSTEM_ARCHITECTURE.md`](008_SYSTEM_ARCHITECTURE.md)

## Core Principles

- Evidence before belief.
- Method before conclusion.
- Verification before trust.
- Transparency before authority.
- Reproducibility before publication.
- Every hypothesis must be falsifiable.
- Every important decision must be documented.
- Negative results are scientific results.
- Better evidence replaces previous evidence.

## Documentation Principles

Documentation is considered part of the scientific method.

Every document shall be: versioned, traceable, reviewable, reproducible, cross-referenced.

No document shall exist without a purpose.

Full standard: [`foundation/000_DOCUMENTATION_STANDARD.md`](000_DOCUMENTATION_STANDARD.md)

## Software Principles

- The software should be modular.
- Research programs should remain independent.
- Every output should be reproducible.
- Every analysis should be executable from raw datasets.

## Data Principles

- Prefer public datasets.
- Never modify original datasets.
- Store provenance.
- Version processed datasets.
- Document preprocessing.

## Validation Principles

Every conclusion should be reproducible.

Every figure should identify: dataset, algorithm, software version, configuration, research
question, git commit.

## Repository Structure (planned)

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

## Development Workflow

```
Research Question
    ↓
Specification
    ↓
Implementation
    ↓
Validation
    ↓
Review
    ↓
Publication
```

## Technology Stack (planned)

Python, Git, GitHub, PostgreSQL/PostGIS, Docker, MkDocs, GitHub Actions, Jupyter.

## AI Usage

The project makes use of AI-assisted drafting and software development.

Artificial intelligence shall never be considered scientific authority.

Scientific responsibility remains entirely human.

AI usage shall always be documented.

Full policy: [`governance/AI_USAGE.md`](../governance/AI_USAGE.md)

## Current Weaknesses

- The Foundation documentation is incomplete.
- No scientific methodology has yet been formally documented.
- No datasets have been acquired.
- No validation pipeline exists.
- No software architecture has been implemented.
- No statistical framework has been defined.
- No research program has been executed.

## Immediate Priorities

1. Complete Foundation.
2. Define documentation standard. ✅ (HERMES-FND-000)
3. Define methodology.
4. Acquire first datasets.
5. Implement bootstrap.
6. Implement downloader.
7. Produce first reproducible notebook.
8. Generate first scientific report.

## Success Criteria

The project is considered successful when an independent researcher can:

- clone the repository
- download the datasets
- execute the workflow
- reproduce the published results
- evaluate every methodological decision independently

without requiring information outside the repository.

## Final Statement

HERMES should not be evaluated by the conclusions it reaches.

It should be evaluated by the quality, transparency and reproducibility of the methods it
provides.

Scientific knowledge advances when methods remain open to verification.

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Rewritten from original HERMES.rtf audit into standard document format with mandatory metadata |
