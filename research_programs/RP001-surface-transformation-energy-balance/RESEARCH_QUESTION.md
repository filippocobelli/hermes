# HERMES
# RP001 — Research Question

- **Document ID:** HERMES-RP001-000
- **Version:** 0.1.0
- **Status:** Draft for Review
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Scientific Method Reviewer role)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** RP001 (this document)
- **Related ADR:** ADR-001
- **License:** TBD

---

## Title

Surface Transformation and Energy Balance

## Primary Question

Does large-scale anthropogenic transformation of land surfaces produce statistically
significant changes in surface energy balance compared with equivalent control areas, after
controlling for known environmental variables?

## Background

This is the first Research Program under the generalized HERMES framework (see ADR-001).
It is deliberately framed around *anthropogenic transformation* in general, not around any
single technology such as photovoltaic installations. Photovoltaic sites are one candidate
case among several (see `foundation/FOUNDATION.md` → Initial Motivation).

## Scope

In scope:

- Comparison of surface energy balance metrics between a treatment area (subject to
  anthropogenic transformation) and one or more control areas.
- Any transformation class listed in the Foundation's Initial Motivation, evaluated on equal
  methodological footing.

Out of scope (for RP001 specifically, may become separate future Research Programs):

- Attribution of a *mechanism* beyond statistical correlation, unless a specific mechanistic
  hypothesis is separately defined and tested.
- Atmospheric circulation effects beyond the immediate surface boundary layer.
- Any policy or advocacy conclusion (see Foundation → What HERMES Is Not).

## Required Pre-Registration (before any dataset is selected)

As Scientific Method Reviewer, the following must be defined and documented **before** any
specific case or dataset is chosen, to prevent selection bias (see ADR-001, Negative/Risks):

1. **Case selection criteria** — what qualifies a site as a valid treatment case, and the
   order in which transformation classes will be studied, with justification for that order.
2. **Control area selection criteria** — how a control area is defined as "otherwise
   equivalent," and what environmental variables must match within what tolerance.
3. **Confounding variables to control for** — an explicit list (e.g. pre-existing land cover,
   elevation, latitude/climate zone, proximity to water bodies, regional weather patterns).
4. **Primary metric(s)** — the specific surface energy balance metric(s) to be measured
   (e.g. land surface temperature, albedo, sensible/latent heat flux) and their data source.
5. **Statistical test and significance threshold** — defined in advance, not chosen after
   seeing the data.

These five items must be completed in a `HYPOTHESES.md` and/or `METHODOLOGY.md` document
before proceeding to dataset acquisition. This document (`RESEARCH_QUESTION.md`) does not
itself constitute pre-registration.

## Falsifiability

The primary question is falsifiable: a null result (no statistically significant difference
between treatment and control areas, after controlling for the variables in item 3 above)
is a valid, publishable outcome per Foundation Core Principles ("Negative results are
scientific results").

## Status of This Document

This document defines the Research Question only. Hypotheses, metrics, dataset selection and
methodology are intentionally left for a separate, subsequent document to avoid conflating
"what we are asking" with "what we expect to find."

## Related Documents

- `foundation/FOUNDATION.md`
- `governance/adr/ADR-001-generalized-scope.md`
- `research_programs/RP001-surface-transformation-energy-balance/HYPOTHESES.md` (pending)

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial Research Question document, with pre-registration requirements added by Scientific Method Reviewer |
