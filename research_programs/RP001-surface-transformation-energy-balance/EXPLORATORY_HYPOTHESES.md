# HERMES
# RP001 — Exploratory Hypotheses (Non-Confirmatory)

- **Document ID:** HERMES-RP001-002
- **Version:** 0.1.0
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

## Status and Path Forward

EH-001 is logged here for traceability, in case future case selection (Case 002, 003, ...)
naturally produces the variation in "distance to nearest other transformation" needed to test
it. If and when RP001 (or a future RP) has enough cases to test EH-001 properly, it would
require its own pre-registration (metric, test, threshold, power analysis) before being
treated as confirmatory — exactly as HYPOTHESES.md Sections 4–5 were for the primary question.

Until then: EH-001 does not change Case 001's selection criteria, ADR-004's clean-zone
approach, or any part of the locked RP001 methodology.

## Related Documents

- `research_programs/RP001-surface-transformation-energy-balance/HYPOTHESES.md`
- `governance/adr/ADR-004-criterion4-refinement.md`
- `research_programs/RP001-surface-transformation-energy-balance/cases/case-001-nunez-de-balboa.md`

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial exploratory hypothesis log; EH-001 recorded |
