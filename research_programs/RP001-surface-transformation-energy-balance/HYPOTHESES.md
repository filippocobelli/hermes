# HERMES
# RP001 — Hypotheses & Pre-Registration

- **Document ID:** HERMES-RP001-001
- **Version:** 0.1.0
- **Status:** Draft for Review — Sections 4 and 5 require Scientific Method Review with a higher-capability model before approval (see note below)
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Scientific Method Reviewer role — Sonnet 5)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** RP001
- **Related ADR:** ADR-001
- **License:** TBD

---

## ⚠️ Model Review Note

Sections 4 (Primary Metrics) and 5 (Statistical Test and Significance Threshold) define the
falsifiability boundary of RP001. Per project agreement, these should be reviewed with
**Claude Opus 4.8** before being marked `Approved`, given the higher stakes of getting
statistical design wrong. This document marks them as `Draft — pending Opus review`.

---

## Purpose

This document completes the pre-registration required by
`research_programs/RP001-surface-transformation-energy-balance/RESEARCH_QUESTION.md`
before any dataset is selected or acquired.

---

## 1. Case Selection Criteria

**Status:** Draft

A transformation site qualifies as a valid treatment case for RP001 if it satisfies all of
the following:

1. **Size threshold** — minimum contiguous transformed area, to be set large enough to be
   resolvable by the chosen remote-sensing data resolution (see Section 4). Placeholder:
   ≥ 10 hectares contiguous.
2. **Age threshold** — the transformation must have existed, unchanged in footprint, for at
   least 2 full years prior to the observation window, to allow surface conditions to
   stabilize (e.g. vegetation regrowth patterns around infrastructure, soil compaction).
3. **Documented transformation date** — the date of land-cover change must be verifiable
   independently (permitting records, satellite imagery change-detection, or equivalent),
   not inferred from the same dataset used for the outcome measurement.
4. **No concurrent confounding transformation** — no other large-scale land transformation
   within a defined buffer radius (placeholder: 2 km) during the observation window.

**Selection order across transformation classes** (to mitigate the bias risk flagged in
ADR-001): classes will be studied in the following order, chosen by **data availability and
verifiability**, not by expected outcome:

1. Photovoltaic installations (motivating case, but not privileged in analysis)
2. Logistics hubs / large parking areas
3. Urban expansion
4. Remaining classes per Foundation → Initial Motivation, in order of dataset availability

This order and its rationale must not be changed after seeing preliminary results without a
new ADR documenting why.

## 2. Control Area Selection Criteria

**Status:** Draft

A control area is valid if, relative to the treatment area, it matches within defined
tolerance on:

- **Climate zone** (Köppen classification or equivalent) — exact match required.
- **Elevation** — within ±100 m, placeholder tolerance.
- **Pre-transformation land cover class** — same class as the treatment area had before
  transformation (verified via historical imagery), not the current surrounding land cover.
- **Latitude** — within ±2°, to control for solar geometry effects on energy balance.
- **Distance to nearest water body** — within same order of magnitude, to control for
  local microclimate moderation.

Control areas shall be selected **before** outcome data is examined, using only the criteria
above plus the pre-transformation land cover record. Multiple control areas per treatment
case are preferred over a single control area, to allow variance estimation.

## 3. Confounding Variables to Control For

**Status:** Draft

Minimum set to be logged and controlled for in every case/control pair:

- Pre-existing (pre-transformation) land cover class
- Elevation
- Latitude / climate zone
- Proximity to water bodies
- Regional weather anomalies during the observation window (to avoid attributing a weather
  event to the transformation itself)
- Seasonal timing of the observation window (must be matched between treatment and control)
- Any known concurrent regional-scale change (e.g. drought, wildfire) affecting both areas

This list is a minimum. Each specific case in Section 1 may require additional
case-specific confounders, to be documented in a per-case appendix.

## 4. Primary Metrics — Draft, pending Opus review

**Status:** Draft — pending Opus review

Candidate metrics (not yet finalized):

- Land Surface Temperature (LST), from satellite thermal bands
- Albedo (surface reflectance)
- Normalized Difference Vegetation Index (NDVI), as a covariate rather than outcome
- Sensible and latent heat flux, if derivable from available data sources without requiring
  in-situ instrumentation not currently planned

Open questions for review: which metric(s) are primary vs. secondary; minimum spatial/temporal
resolution required to resolve the effect size expected from a 10-hectare site; data source
selection (e.g. Landsat, Sentinel, MODIS) and its implications for the age/size thresholds in
Section 1.

## 5. Statistical Test and Significance Threshold — Draft, pending Opus review

**Status:** Draft — pending Opus review

Placeholder approach (not approved):

- Paired or matched-pairs comparison between treatment and control areas.
- Significance threshold: placeholder α = 0.05, two-tailed — **to be reviewed**, including
  whether a correction for multiple comparisons is needed given multiple transformation
  classes and multiple metrics.
- Effect size reporting required in addition to p-value (placeholder: Cohen's d or
  equivalent), to avoid conflating statistical and practical significance.
- Power analysis to be conducted **before** data acquisition to determine minimum number of
  case/control pairs needed, given the effect size this study is powered to detect.

This section must not be finalized without addressing: independence of observations across
multiple pixels within a single site (spatial autocorrelation), and whether a mixed-effects
model (site as random effect) is more appropriate than a simple paired test.

## Status of This Document

Sections 1–3: Draft, ready for standard technical review.
Sections 4–5: Draft, **not to be used for dataset acquisition decisions until reviewed with
Opus 4.8** and formally marked `Approved`.

## Related Documents

- `research_programs/RP001-surface-transformation-energy-balance/RESEARCH_QUESTION.md`
- `governance/adr/ADR-001-generalized-scope.md`
- `foundation/GLOSSARY.md`

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial draft; Sections 1–3 drafted, Sections 4–5 flagged for Opus review |
