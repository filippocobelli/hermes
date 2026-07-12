# HERMES
# RP001 — Pre-Registration Lock Record

- **Document ID:** HERMES-RP001-LOCK-001
- **Version:** 1.0.0
- **Status:** Locked
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted — Sonnet 5 for Sections 1-3 and Research Question drafting; Opus 4.8 for Sections 4-5 statistical design, twice, second pass post-literature-review)
- **Lock Date:** 2026-07-11
- **Related Research Questions:** RP001
- **Related ADR:** ADR-001, ADR-002, ADR-004
- **License:** TBD

---

## Purpose

This document formally records the pre-registration lock for RP001, per
`HYPOTHESES.md` Section 5.7 and `RESEARCH_QUESTION.md`. From this date, any deviation from
the locked methodology requires a new ADR and must be disclosed as a pre-registration
deviation in any publication.

## Locked Documents (exact versions)

| Document | Version | Locked Sections |
|---|---|---|
| `research_programs/RP001-.../RESEARCH_QUESTION.md` | 0.3.0 | All |
| `research_programs/RP001-.../HYPOTHESES.md` | 0.4.0 | Sections 1–5 (Sections 1–3 lower-stakes, Sections 4–5 statistically load-bearing) |

## What Is Locked

1. **Primary outcome:** Land Surface Temperature (LST), Landsat C2 L2, season-stratified
   (JJA / DJF), two independent confirmatory nulls.
2. **Secondary outcomes:** albedo; vegetation change via difference-in-differences.
3. **NDVI treatment:** excluded as a confirmatory-model covariate (mediator, not confounder);
   total-effect framing.
4. **Unit of analysis:** site, not pixel.
5. **Model:** linear mixed-effects, site as random effect, season × treatment-status
   interaction as the fixed effect of interest.
6. **Significance threshold:** α = 0.05, two-tailed, per season.
7. **Multiple-comparisons correction:** Benjamini–Hochberg FDR across the confirmatory family
   (currently {H0(summer), H0(winter)} for the photovoltaic class).
8. **Effect size reporting:** mandatory alongside every p-value (°C, 95% CI).
9. **Power analysis requirement:** must be computed from literature-informed effect-size
   priors (~0.5 K global annual, ~2 K Mediterranean summer) before acquisition; study reported
   as underpowered if the achievable site count falls short.
10. **Case selection criteria (1–4)** and **control area criteria**, including the ADR-004
    clean-zone refinement and the no-nearby-transformation check for controls.
11. **Documented limitations:** photovoltaic emissivity retrieval bias (asymmetric,
    undcorrected); NDVI mixed-signature over post-construction treatment pixels; temporal
    pairing assumption (regional weather affects treatment/control comparably).
12. **Case 001 status:** explicitly a pilot / proof-of-methodology, not a standalone
    confirmatory result.

## What Is NOT Locked (may still evolve without a new ADR)

- Software implementation details (Layers 2–6) not yet built.
- Identification of additional cases (Case 002, 003, ...) — subject to the same locked
  Section 1 criteria, but the specific sites are not yet chosen.
- Exploratory hypotheses (EH-001, EH-002, EH-003) — by definition never locked, never
  confirmatory.

## Process Followed (for traceability)

1. Initial draft (Sections 1–3, Sonnet 5).
2. Sections 4–5 first pass (Opus 4.8).
3. Case 001 identified and verified (site selection, control areas) — surfaced two real
   methodological gaps during verification (ADR-004 buffer refinement; water-proximity
   correction of Control 1 candidate).
4. **Literature review performed before lock** (explicitly requested, not skipped) —
   `LITERATURE_BRIEFING_sections4-5.md` — surfacing three further issues: missing effect-size
   priors, undocumented seasonal sign reversal, undocumented emissivity bias.
5. Sections 4–5 revised (Opus 4.8, second pass): seasonal stratification, NDVI reclassified as
   mediator, vegetation DiD added as secondary outcome, emissivity limitation documented,
   Case 001 reframed as pilot.
6. `RESEARCH_QUESTION.md` aligned to the revised design.
7. Owner lock confirmation: 2026-07-11.

## Owner Confirmation

Locked by Filippo Cobelli (Owner), per `governance/AI_USAGE.md` — final approval of
methodology, validation procedures, and project governance remains human responsibility. AI
assistance (Sonnet 5, Opus 4.8) served as technical/scientific-method reviewer throughout;
this record exists precisely so that AI-assisted drafting is not mistaken for AI authority
over the scientific decision.

## Change Log

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-11 | Pre-registration locked |
