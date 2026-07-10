# HERMES
# RP001 — Research Question

- **Document ID:** HERMES-RP001-000
- **Version:** 0.2.0
- **Status:** Draft for Review
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Scientific Method Reviewer role)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** RP001 (this document)
- **Related ADR:** ADR-001, ADR-002
- **License:** TBD

---

## Title

Surface Transformation and Land Surface Temperature

## Primary Question

Does large-scale anthropogenic transformation of land surfaces produce statistically
significant changes in Land Surface Temperature (and, secondarily, albedo) compared with
equivalent control areas, after controlling for known environmental variables?

> **Note on framing (ADR-002):** RP001's motivating physical context is surface *energy
> balance*. However, energy balance is not directly measured. The declared, measurable
> primary outcome is Land Surface Temperature (LST), a reproducible quantity retrievable from
> public satellite thermal data. Any statement about energy balance is an *interpretation* of
> LST/albedo results, explicitly labelled as such, never a direct measurement claim.

## Background

This is the first Research Program under the generalized HERMES framework (see ADR-001).
It is framed around *anthropogenic transformation* in general, not around any single
technology such as photovoltaic installations. Photovoltaic sites are one candidate case
among several (see `foundation/FOUNDATION.md` → Initial Motivation).

The choice of LST as the measured outcome (rather than modelled energy balance) is documented
and justified in ADR-002, primarily on grounds of reproducibility and clean falsifiability.

## Scope

In scope:

- Comparison of LST (primary) and albedo (secondary) between a treatment area (subject to
  anthropogenic transformation) and one or more control areas.
- Any transformation class listed in the Foundation's Initial Motivation, evaluated on equal
  methodological footing.

Out of scope (for RP001 specifically; may become separate future Research Programs):

- Direct measurement or modelling of full surface energy balance (net radiation, sensible /
  latent / ground heat flux). A dedicated energy-balance-modelling program, where the model
  assumptions are themselves the subject of study, may follow (see ADR-002, Alternative A).
- Attribution of a *mechanism* beyond statistical association, unless a specific mechanistic
  hypothesis is separately defined and tested.
- Atmospheric circulation effects beyond the immediate surface.
- Any policy or advocacy conclusion (see Foundation → What HERMES Is Not).

## Required Pre-Registration (before any dataset is selected)

As Scientific Method Reviewer, the following must be defined and documented **before** any
specific case or dataset is chosen, to prevent selection bias (see ADR-001):

1. **Case selection criteria** — what qualifies a site as a valid treatment case, and the
   order in which transformation classes will be studied, with justification for that order.
2. **Control area selection criteria** — how a control area is defined as "otherwise
   equivalent," and what environmental variables must match within what tolerance.
3. **Confounding variables to control for** — an explicit list.
4. **Primary metric(s)** — the specific outcome(s) and their data source.
5. **Statistical test and significance threshold** — defined in advance.

These five items are addressed in `HYPOTHESES.md`. Items 4 and 5 have been reviewed with
Opus 4.8 and are ready to be locked by the Owner before dataset acquisition. This document
(`RESEARCH_QUESTION.md`) does not itself constitute the pre-registration; `HYPOTHESES.md`
does.

## Falsifiability

The primary question is falsifiable: a null result (no statistically significant LST
difference between treatment and control areas, after controlling for the Section 3
confounders) is a valid, publishable outcome per Foundation Core Principles ("Negative
results are scientific results"). The two-tailed test preserves falsifiability in both
directions (warming or cooling).

## Status of This Document

This document defines the Research Question and scope. The full pre-registered analysis plan
(hypotheses, metrics, dataset criteria, statistical design) lives in `HYPOTHESES.md`.

## Related Documents

- `foundation/FOUNDATION.md`
- `governance/adr/ADR-001-generalized-scope.md`
- `governance/adr/ADR-002-lst-primary-outcome.md`
- `research_programs/RP001-surface-transformation-energy-balance/HYPOTHESES.md`

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial Research Question document, with pre-registration requirements |
| 0.2.0 | 2026-07-10 | Primary outcome refined to LST per ADR-002; energy balance reframed as interpretation; scope and falsifiability sections updated |
