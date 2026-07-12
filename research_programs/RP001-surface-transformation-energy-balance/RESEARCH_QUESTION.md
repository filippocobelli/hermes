# HERMES
# RP001 — Research Question

- **Document ID:** HERMES-RP001-000
- **Version:** 0.3.0
- **Status:** **Locked** (2026-07-11) — see PRE_REGISTRATION_LOCK.md
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Scientific Method Reviewer role)
- **Last Updated:** 2026-07-11
- **Related Research Questions:** RP001 (this document)
- **Related ADR:** ADR-001, ADR-002, ADR-004
- **License:** TBD

---

## Title

Surface Transformation and Land Surface Temperature — Seasonal Effects

## Primary Question

Does large-scale anthropogenic transformation of land surfaces produce statistically
significant changes in Land Surface Temperature (LST) compared with equivalent control areas,
after controlling for known environmental variables — **and does this effect differ between
summer and winter?**

This is now two pre-registered confirmatory hypotheses, not one (see HYPOTHESES.md Section
5.3):

- **H0(summer, JJA):** no treatment–control LST difference in summer.
- **H0(winter, DJF):** no treatment–control LST difference in winter.

> **Note on framing (ADR-002, and HYPOTHESES.md v0.4 §4.4):** the motivating physical context
> is surface *energy balance*, but the directly measured, falsifiable outcome is LST. A
> literature review (HERMES-RP001-003) found that solar-park LST effects in Mediterranean
> climates — the same climate zone as RP001's Case 001 — reverse sign seasonally (cooling in
> summer, warming in winter). An annual-aggregate design risks cancelling two real,
> opposite-signed effects into a false null. RP001 is therefore season-stratified by design,
> not averaged across the year.

## Secondary Question

Does the transformation produce a measurable change in vegetation cover (NDVI), relative to
the same control areas, using a difference-in-differences design comparing pre- and
post-transformation imagery? (HYPOTHESES.md §4.5). This is a secondary, not confirmatory,
outcome — see Scope below for why NDVI is not used as a covariate for the primary LST
question.

## Background

First Research Program under the generalized HERMES framework (ADR-001), framed around
*anthropogenic transformation* in general — photovoltaic sites are one candidate case among
several (`foundation/FOUNDATION.md` → Initial Motivation).

LST (not modelled energy balance) is the measured outcome, per ADR-002, primarily for
reproducibility and clean falsifiability.

## Scope

In scope:

- Comparison of LST (primary, season-stratified) and albedo (secondary) between treatment and
  control areas.
- Vegetation change via difference-in-differences (secondary outcome, §4.5).
- Any transformation class from the Foundation's Initial Motivation, on equal methodological
  footing.

**RP001 measures the total effect of transformation on LST** — including the pathway by which
transformation alters vegetation, which in turn affects LST. NDVI is therefore treated as a
**mediator**, not a confounder, and is deliberately excluded as a covariate in the primary
model (HYPOTHESES.md §4.3). Decomposing the effect into direct/vegetation-mediated components
is logged as exploratory (EXPLORATORY_HYPOTHESES.md, EH-003), not confirmatory.

Out of scope for RP001 specifically:

- Direct measurement/modelling of full surface energy balance (net radiation, sensible/latent/
  ground heat flux) — may become a separate future Research Program (ADR-002, Alternative A).
- Mechanistic attribution beyond statistical association.
- Atmospheric circulation effects beyond the immediate surface — including the regional
  mesoscale land-atmosphere feedback hypothesis (EH-002), explicitly logged as a candidate
  *future* Research Program requiring different data (precipitation/reanalysis), not a
  modification of RP001.
- Any policy or advocacy conclusion (Foundation → What HERMES Is Not).

## Required Pre-Registration (before any dataset is selected)

Per ADR-001 bias mitigation, the following are defined in `HYPOTHESES.md` before any specific
case or dataset is chosen:

1. Case selection criteria (§1) — including the ADR-004 clean-zone refinement.
2. Control area selection criteria (§2) — including the no-nearby-transformation check.
3. Confounding variables (§3) — explicitly excluding NDVI as a controlled covariate (§4.3).
4. Primary/secondary metrics (§4) — LST primary (season-stratified), albedo secondary,
   vegetation DiD secondary, documented emissivity limitation.
5. Statistical design (§5) — mixed-effects model with season × treatment interaction, two
   confirmatory seasonal hypotheses, FDR correction, literature-informed power analysis.

Items 4–5 were reviewed with Opus 4.8 twice: once for initial design, once after a literature
review (HERMES-RP001-003) that materially revised the seasonal structure, the treatment of
NDVI, and added the emissivity limitation. Ready for Owner lock decision.

## Falsifiability

Both seasonal hypotheses are falsifiable independently: a null result in either or both
seasons is a valid, publishable outcome (Foundation Core Principles — "Negative results are
scientific results"). Two-tailed tests preserve falsifiability in both directions per season,
essential given the literature predicts opposite signs by season.

## Case 001 Status Note

Case 001 (Núñez de Balboa) is currently the only identified case. Per HYPOTHESES.md §5.6, a
single treatment site cannot support confirmatory site-level inference (minimal degrees of
freedom for the site random effect). Case 001 is explicitly framed as a **pilot /
proof-of-methodology** — validating the acquisition-to-model pipeline and producing a first
effect-size estimate — not as a confirmatory result on its own. Confirmatory inference
requires the multi-site sample sized by the power analysis (§5.5).

## Status of This Document

Defines the Research Question and scope. The full pre-registered analysis plan lives in
`HYPOTHESES.md`.

## Related Documents

- `foundation/FOUNDATION.md`
- `governance/adr/ADR-001-generalized-scope.md`
- `governance/adr/ADR-002-lst-primary-outcome.md`
- `governance/adr/ADR-004-criterion4-refinement.md`
- `research_programs/RP001-surface-transformation-energy-balance/HYPOTHESES.md`
- `research_programs/RP001-surface-transformation-energy-balance/EXPLORATORY_HYPOTHESES.md`
- `research_programs/RP001-surface-transformation-energy-balance/LITERATURE_BRIEFING_sections4-5.md`

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial Research Question document |
| 0.2.0 | 2026-07-10 | Primary outcome refined to LST per ADR-002 |
| 0.3.0 | 2026-07-11 | Aligned with HYPOTHESES.md v0.4: primary question restructured into two seasonal hypotheses; NDVI/total-effect framing added to Scope; vegetation DiD added as secondary question; EH-002/EH-003 referenced; Case 001 pilot status noted |
