# HERMES
# RP001 — Hypotheses & Pre-Registration

- **Document ID:** HERMES-RP001-001
- **Version:** 0.3.0
- **Status:** Draft for Review — Sections 1–5 drafted; Sections 4–5 reviewed with Opus 4.8
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Scientific Method Reviewer role — Sections 1–3 Sonnet 5, Sections 4–5 Opus 4.8)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** RP001
- **Related ADR:** ADR-001, ADR-002, ADR-004
- **License:** TBD

---

## Purpose

This document completes the pre-registration required by
`research_programs/RP001-surface-transformation-energy-balance/RESEARCH_QUESTION.md`
before any dataset is selected or acquired.

Per ADR-002, RP001's primary outcome is Land Surface Temperature (LST), with albedo as a
secondary outcome. "Surface energy balance" is the motivating physical context, not a
directly measured quantity.

---

## 1. Case Selection Criteria

**Status:** Draft

A transformation site qualifies as a valid treatment case for RP001 if it satisfies all of
the following:

1. **Size threshold** — minimum contiguous transformed area large enough to be resolvable by
   the chosen thermal data resolution. Because LST native resolution is coarse (see Section 4
   and ADR-002), this threshold is tied to the sensor: the transformed area must span at
   least a defined minimum number of clean thermal pixels (see Section 4 for the exact
   pixel-count rule). Placeholder: ≥ 25 hectares contiguous when using Landsat-class thermal
   data.
2. **Age threshold** — the transformation must have existed, unchanged in footprint, for at
   least 2 full years prior to the observation window.
3. **Documented transformation date** — verifiable independently (permitting records,
   change-detection on archival imagery), not inferred from the outcome dataset.
4. **No concurrent confounding transformation within 2 km of the sampled interior pixels**
   — refined per ADR-004: this criterion applies to the specific pixels used for LST
   sampling, not to every point of the site's full perimeter. If a site's own footprint
   contains a sub-region ("clean sampling zone") whose interior-buffered pixels are all
   ≥ 2 km from any other large-scale anthropogenic transformation, that sub-region may be
   used even if other parts of the same site are closer to a neighbouring transformation.
   The clean zone must be computed by a fixed, pre-defined geometric rule (erode by one pixel
   for edge-mixing, then subtract 2 km buffers around every identified neighbour) — never
   chosen by hand per case.

**Selection order across transformation classes** (to mitigate the bias risk flagged in
ADR-001), ordered by data availability and verifiability, NOT by expected outcome:

1. Photovoltaic installations (motivating case, not privileged in analysis)
2. Logistics hubs / large parking areas
3. Urban expansion
4. Remaining Foundation classes in order of dataset availability

This order shall not change after seeing preliminary results without a new ADR.

## 2. Control Area Selection Criteria

**Status:** Draft

A control area is valid if, relative to the treatment area, it matches within tolerance on:

- **Climate zone** (Köppen or equivalent) — exact match required.
- **Elevation** — within ±100 m (placeholder).
- **Pre-transformation land cover class** — same class the treatment area had *before*
  transformation (historical imagery), not current surrounding cover.
- **Latitude** — within ±2° (solar geometry).
- **Distance to nearest water body** — same order of magnitude (microclimate moderation).
- **No large-scale anthropogenic transformation within 2 km of the control area's own
  sampled interior pixels** *(added 2026-07-10)* — a control area must be a genuinely
  undisturbed baseline. Applying Criterion 4's ADR-004 clean-zone logic (Section 1) to
  candidate control areas as well as treatment areas: a control area near another
  transformation is not a clean baseline regardless of whether that transformation happens
  to also be near the treatment site. This must be checked with the same geometry-based
  method used for treatment sites (see `software/examples/check_case001_confounders_geom.py`
  as the reference implementation), not assumed from visual inspection alone.

Control areas shall be selected **before** outcome data is examined. Multiple control areas
per treatment case are required (minimum 2), not merely preferred — this is now a hard
requirement because the analysis in Section 5 relies on between-site variance estimation.

## 3. Confounding Variables to Control For

**Status:** Draft

Minimum set logged and controlled for in every case/control comparison:

- Pre-existing (pre-transformation) land cover class
- Elevation
- Latitude / climate zone
- Proximity to water bodies
- Regional weather anomalies during the observation window
- Seasonal timing of the observation window (matched between treatment and control)
- Any known concurrent regional-scale change (drought, wildfire) affecting both areas
- Time of satellite overpass (LST is strongly diurnal; treatment and control observations
  must come from the same sensor and comparable overpass times)
- Surface emissivity (LST retrieval is emissivity-dependent; emissivity differences between
  land cover types can masquerade as temperature differences)

Each specific case may require additional case-specific confounders, documented in a per-case
appendix.

---

## 4. Primary Metrics

**Status:** Reviewed with Opus 4.8 — Approved for pre-registration

### 4.1 Primary outcome

**Land Surface Temperature (LST).** Per ADR-002, this is the declared primary outcome.

- **Data source (primary):** Landsat 8/9 Collection 2 Level-2 surface temperature product,
  which provides atmospherically corrected, emissivity-aware LST at 30 m grid spacing (TIRS
  thermal data natively ~100 m, resampled to 30 m in the product). Rationale: it is a public,
  documented, reproducible Level-2 product — an independent reviewer can re-download the exact
  same scenes.
- **Data source (secondary / cross-check):** MODIS MOD11/MYD11 LST (~1 km) for temporal
  density and as an independent-sensor consistency check on the Landsat-derived effect.
- **Pixel-count rule (resolves Section 1 size threshold):** a treatment site must contain at
  least **30 valid (cloud-free, non-edge) Landsat LST pixels** wholly interior to the
  transformed footprint, after excluding a one-pixel buffer along the footprint boundary to
  avoid mixed-pixel contamination — and, per ADR-004, also ≥ 2 km from any other identified
  large-scale transformation. At 30 m spacing, 30 interior pixels after a boundary buffer
  corresponds roughly to the ≥ 25 ha placeholder in Section 1; the pixel-count rule is the
  binding criterion, the hectare figure is indicative.

### 4.2 Secondary outcome

**Albedo (surface shortwave reflectance).** Retrieved from the same Landsat Collection 2
surface reflectance product via an established narrowband-to-broadband albedo conversion.
Albedo is reported as a secondary outcome and as a candidate covariate/mechanistic hint, not
as an independent confirmatory test.

### 4.3 Covariate (not an outcome)

**NDVI**, from the same surface reflectance product, used to characterise vegetation state of
treatment and control areas and as a covariate — explicitly NOT an outcome, to avoid
circularity (vegetation change is often part of the transformation itself).

### 4.4 Observation window and aggregation

- Observations are restricted to cloud-free thermal retrievals over a defined multi-season
  window (minimum one full annual cycle) to avoid seasonal aliasing.
- Treatment and control observations must be **paired in time** (same or near-adjacent
  overpass dates) so that regional weather does not differentially affect one side.
- Per-site LST is summarised per observation date, then across dates, producing a per-site
  distribution rather than a pool of pixels (see Section 5 for why).

---

## 5. Statistical Design, Test, and Significance Threshold

**Status:** Reviewed with Opus 4.8 — Approved for pre-registration

### 5.1 Unit of analysis

The unit of analysis is the **site**, not the pixel. This is the single most important
methodological decision in RP001 and is non-negotiable without a new ADR.

Rationale: pixels within a single site are strongly spatially autocorrelated and are NOT
independent observations. Treating thousands of pixels as independent would inflate effective
sample size by orders of magnitude and produce spuriously tiny p-values even for a
non-existent effect. This is the most common way studies of this kind reach false positives,
and RP001 shall not commit it.

### 5.2 Handling spatial autocorrelation

Two complementary safeguards:

1. **Per-site aggregation** — each site/date yields a summary statistic (e.g. median LST of
   valid interior pixels), collapsing within-site pixel autocorrelation before any
   comparison.
2. **Mixed-effects model** — the confirmatory analysis uses a linear mixed-effects model with
   **site (and matched control-cluster) as a random effect**, and transformation status
   (treatment vs control) as the fixed effect of interest, with the Section 3 confounders as
   covariates. This explicitly models the nested structure (observations within sites within
   matched clusters) rather than pretending observations are independent.

Residual spatial autocorrelation shall be checked (e.g. Moran's I on model residuals) and
reported; if present, it is disclosed as a limitation rather than hidden.

### 5.3 Confirmatory test and threshold

- **Primary confirmatory test:** the fixed-effect coefficient for transformation status in
  the mixed-effects model (treatment vs control LST difference, controlling for covariates).
- **Significance threshold:** α = 0.05, **two-tailed** (the direction of any LST effect is
  not assumed a priori — this preserves falsifiability in both directions).
- **Multiple-comparisons correction:** because RP001 will eventually run across multiple
  transformation classes and two outcomes (LST primary, albedo secondary), the family of
  confirmatory tests shall be corrected. The primary outcome (LST) per transformation class
  is the pre-registered confirmatory family; a Benjamini–Hochberg false-discovery-rate
  correction is applied across that family. Albedo and any per-class exploratory analyses are
  labelled exploratory and are NOT counted toward confirmatory claims.

### 5.4 Effect size (mandatory alongside p-value)

A p-value alone is insufficient. Every confirmatory result reports:

- the estimated LST difference in **kelvin/°C** with a 95% confidence interval (the physically
  meaningful effect size), and
- a standardised effect size for cross-study comparison.

A statistically significant but physically negligible LST difference (e.g. a few hundredths
of a degree) shall be reported as such — statistical significance is not promoted to practical
or physical significance.

### 5.5 Statistical power (computed BEFORE data acquisition)

Power is driven by the **number of matched site clusters**, not the number of pixels. Before
acquisition, a power analysis shall determine the minimum number of treatment sites (each with
≥ 2 controls) required to detect a pre-specified minimum LST difference of scientific interest
(the minimum effect size to be declared in advance, not after seeing data). If the achievable
number of qualifying sites is below the powered minimum, RP001 shall report the study as
underpowered rather than proceed and over-claim.

Note (per ADR-004): where a site's usable sample is a "clean sampling zone" smaller than its
full footprint, the power analysis must use the actual clean-zone pixel count for that site,
not its full-footprint pixel count.

### 5.6 Pre-registration lock

Sections 4 and 5 constitute the pre-registered analysis plan. Once locked and committed, any
deviation (change of primary outcome, test, threshold, correction method, or effect-size
definition) requires a new ADR and must be reported in the publication as a deviation from
pre-registration. Analysis decisions made after seeing outcome data are, by definition,
exploratory and shall be labelled as such — see
`research_programs/RP001-surface-transformation-energy-balance/EXPLORATORY_HYPOTHESES.md`
for hypotheses explicitly logged as non-confirmatory.

---

## Status of This Document

- Sections 1–3: Draft, ready for standard technical review.
- Sections 4–5: Reviewed with Opus 4.8, approved for pre-registration. Ready to be **locked**
  by human decision (Owner) before dataset acquisition begins.

Human responsibility note (per governance/AI_USAGE.md): AI has drafted and reviewed this
methodology as technical assistant. Final approval and locking of the pre-registration is a
human decision reserved to the Owner.

## Related Documents

- `research_programs/RP001-surface-transformation-energy-balance/RESEARCH_QUESTION.md`
- `research_programs/RP001-surface-transformation-energy-balance/EXPLORATORY_HYPOTHESES.md`
- `governance/adr/ADR-001-generalized-scope.md`
- `governance/adr/ADR-002-lst-primary-outcome.md`
- `governance/adr/ADR-004-criterion4-refinement.md`
- `foundation/GLOSSARY.md`

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial draft; Sections 1–3 drafted, Sections 4–5 flagged for Opus review |
| 0.2.0 | 2026-07-10 | Sections 4–5 completed and reviewed with Opus 4.8 (LST primary per ADR-002, site as unit of analysis, mixed-effects model, FDR correction, power on site count); Section 1 pixel-count rule and Section 3 emissivity/overpass-time confounders added |
| 0.3.0 | 2026-07-10 | Section 1 Criterion 4 refined per ADR-004 (clean sampling zone); Section 2 control area criteria now require the same no-nearby-transformation check; Section 5.5 power note on clean-zone pixel counts; linked new EXPLORATORY_HYPOTHESES.md |
