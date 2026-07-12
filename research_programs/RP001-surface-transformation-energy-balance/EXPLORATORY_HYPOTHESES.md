# HERMES
# RP001 — Exploratory Hypotheses (Non-Confirmatory)

- **Document ID:** HERMES-RP001-002
- **Version:** 0.2.0
- **Status:** Draft — Exploratory only, never confirmatory
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Scientific Method Reviewer role — Sonnet 5)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** RP001
- **Related ADR:** ADR-004
- **License:** TBD

---

## Purpose

This document records hypotheses that are **not** part of RP001's pre-registered
confirmatory analysis (`HYPOTHESES.md`). Per `HYPOTHESES.md` Section 5.6, any analysis
decision made after seeing outcome data — or any hypothesis proposed outside the locked
pre-registration — is exploratory by definition and must never be silently promoted to a
confirmatory claim.

Exploratory hypotheses may motivate a *future*, separately pre-registered Research Program,
but they do not change RP001's primary question, methodology, or the meaning of its results.

## EH-001 — Regional Transformation Density Hypothesis

**Origin:** Raised during Case 001 (Núñez de Balboa) review, when two neighbouring solar
plants were found within 2 km of the treatment site (see ADR-004).

**Informal statement (as proposed):** Nearby anthropogenic transformations "work in synergy"
on local heating — the closer they are to each other, the more they collectively heat the
area.

**Falsifiable, testable restatement:**

> Among treatment sites of comparable size and technology, sites located near other
> large-scale anthropogenic transformations (within some defined proximity, e.g. 2–5 km)
> show a larger LST anomaly (treatment − control difference) than otherwise comparable
> isolated sites, after controlling for the same confounders as RP001 (HYPOTHESES.md
> Section 3).

**Why this is NOT part of RP001's confirmatory design:**

1. **Different physical mechanism.** RP001's primary outcome, LST, is a surface radiative
   temperature — a pixel's value is determined by what is directly beneath it at the moment
   of satellite overpass. There is no established physical mechanism by which a separate
   installation 1.4–1.7 km away directly alters an interior pixel's LST reading. EH-001, if
   real, would operate through a different pathway (e.g. regional-scale heat island
   accumulation, altered local boundary-layer dynamics) — a mesoscale/aggregate effect, not a
   pixel-level one. Testing it properly would likely require a different outcome variable or
   spatial scale of analysis than RP001 uses.
2. **Not testable from a single case.** EH-001 requires *comparing* near-other-transformation
   sites against isolated sites of similar size — this needs a sample of multiple treatment
   sites already, which RP001's Case 001 alone cannot provide.
3. **Sequencing risk.** Per Foundation Core Principles ("Method before conclusion"), the
   methodology must not be shaped around a hypothesis before that hypothesis has been tested.
   Adjusting RP001's design now to accommodate EH-001 would risk building the study around a
   preferred conclusion.

## EH-002 — Regional Mesoscale Land-Atmosphere Feedback Hypothesis

**Origin:** Extension of EH-001, raised after discovering Case 001's surrounding region
contains 384 transformation-tagged features within 8 km (see Case 001 verification history).
Filippo proposed a causal chain: installation → air heating → atmospheric heating →
circulation pattern shifts (analogous to El Niño) → altered precipitation → increased heat
wave frequency.

**Reviewer assessment of the proposed mechanism, as originally stated:** NOT physically
plausible at the scale involved. El Niño is an ocean-atmosphere coupled phenomenon operating
across the Pacific basin (millions of km²), driven by ocean heat content and trade-wind
dynamics — a fundamentally different physical system from a localized land-surface energy
perturbation covering a few hundred to a few thousand hectares. No literature was found
supporting a mechanism at this scale.

**A physically plausible, literature-supported restatement:**

> Regional clustering of large-scale anthropogenic land transformations (e.g. the observed
> density of solar installations in parts of Extremadura) may produce mesoscale
> land-atmosphere feedback effects on local precipitation and/or heat wave frequency,
> distinct from and larger in spatial extent than the effect of any single installation.

**Literature support for the general phenomenon (not for this specific case):**

- Land-use/land-cover change can alter regional climate through biogeophysical pathways
  (albedo, heat/moisture partitioning) with effects of similar or greater magnitude than
  greenhouse-gas-driven change, and landscape heterogeneity can induce mesoscale circulations.
- Existing studies demonstrating measurable precipitation effects from solar/wind
  installations operate at installed areas vastly larger than Extremadura's current
  build-out (e.g. climate-model studies of hypothetical Sahara-scale deployment), and are
  almost universally regional climate *modelling* studies (e.g. WRF), not satellite
  observational studies of actual installed capacity.
- Mesoscale (whole-region, real-installation) observational studies of this kind are
  explicitly noted in the literature as under-studied relative to panel-scale and
  hypothetical-regional-scale modelling studies — i.e. a genuine research gap exists, but at
  a different scale and with different data requirements than RP001.

**Why this is NOT part of RP001, and not a simple future addition to it:**

1. **Different outcome variable entirely.** RP001 measures LST via satellite (a surface
   radiative property). Testing EH-002 requires precipitation records and/or atmospheric
   boundary-layer/reanalysis data (e.g. ERA5) — data types HERMES has no acquisition
   infrastructure for yet (Layer 1 currently targets Landsat/STAC imagery only).
2. **Different spatial/temporal scale.** RP001 is site-level, pixel-based. EH-002 would need
   regional-scale analysis, likely requiring a regional climate model or long time series of
   station/reanalysis data — a different software architecture (Layers 4-5 would need new
   model classes).
3. **Already anticipated, correctly sequenced.** `foundation/FOUNDATION.md` already lists
   "Atmospheric circulation" among HERMES's Long-Term Research Areas. EH-002 is evidence this
   area has real scientific merit — but it belongs there, as a future, separately
   pre-registered Research Program (tentatively RP00X), not as a modification to RP001's
   already near-complete design.

## Status and Path Forward

EH-001 and EH-002 do not change RP001's methodology, Case 001 selection, or any locked
Section of `HYPOTHESES.md`. Both remain logged for traceability and as motivation for a
future Research Program, to be scoped and pre-registered independently — with its own
Research Question, data sources, and falsifiable hypotheses — if and when HERMES has the
infrastructure (atmospheric/precipitation data acquisition) to test it properly.

## Related Documents

- `research_programs/RP001-surface-transformation-energy-balance/HYPOTHESES.md`
- `governance/adr/ADR-004-criterion4-refinement.md`
- `research_programs/RP001-surface-transformation-energy-balance/cases/case-001-nunez-de-balboa.md`

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial exploratory hypothesis log; EH-001 recorded |
| 0.2.0 | 2026-07-10 | EH-002 added (regional mesoscale land-atmosphere feedback), correcting an initially-proposed El Niño-scale mechanism to a literature-supported mesoscale framing; connected to existing Foundation "Atmospheric circulation" long-term research area |
