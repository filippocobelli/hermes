# HERMES
# FND-009 — Glossary

- **Document ID:** HERMES-FND-009
- **Version:** 0.1.0
- **Status:** Draft for Review
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Lead Technical Writer role)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** N/A (applies to all)
- **Related ADR:** N/A
- **License:** TBD

---

## Purpose

This document defines terms used across HERMES documentation to ensure consistent usage.
No document should redefine these terms locally.

## Terms

**Anthropogenic transformation** — Any large-scale, human-caused change to land surface
cover or use (e.g. photovoltaic installations, logistics hubs, urban expansion).

**Control area** — A comparison area not subject to the anthropogenic transformation under
study, selected to be otherwise equivalent to the treatment area on relevant environmental
variables. Selection criteria must be defined *before* dataset acquisition (see ADR-001).

**Confounding variable** — A variable correlated with both the transformation under study and
the observed outcome, capable of producing a spurious association if not controlled for.

**Research Program (RP)** — An independent, self-contained scientific investigation within
HERMES, structured around one primary Research Question (e.g. RP001).

**Research Question** — The top-level question that drives a Research Program's architecture,
hypotheses, metrics, datasets and validation.

**Hypothesis** — A specific, falsifiable, measurable statement derived from a Research
Question.

**Surface energy balance** — The balance between incoming and outgoing energy fluxes
(shortwave/longwave radiation, sensible heat, latent heat, ground heat flux) at a land surface.

**Reproducibility** — The property that an independent party, given the repository and
datasets, can re-execute the workflow and obtain the same published results.

**Falsifiability** — The property that a hypothesis is stated such that an observation could,
in principle, prove it false.

**ADR (Architecture Decision Record)** — A versioned document recording a specific
architectural decision, its context, alternatives considered, and consequences.

**Foundation** — The set of documents (`foundation/`) defining HERMES's purpose, principles,
architecture and terminology, prior to any specific Research Program.

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial glossary |
