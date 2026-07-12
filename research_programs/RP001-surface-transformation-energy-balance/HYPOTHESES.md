# HERMES
# RP001 — Hypotheses & Pre-Registration

- **Document ID:** HERMES-RP001-001
- **Version:** 0.4.0
- **Status:** Draft for Review — Sections 4–5 revised with Opus 4.8 after literature review; ready for Owner lock decision
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Scientific Method Reviewer role — Sections 1–3 Sonnet 5; Sections 4–5 Opus 4.8, revised after literature review HERMES-RP001-003)
- **Last Updated:** 2026-07-11
- **Related Research Questions:** RP001
- **Related ADR:** ADR-001, ADR-002, ADR-004
- **License:** TBD

---

## Purpose

This document completes the pre-registration required by
`research_programs/RP001-surface-transformation-energy-balance/RESEARCH_QUESTION.md`
before any dataset is selected or acquired.

Per ADR-002, RP001's primary outcome is Land Surface Temperature (LST). "Surface energy
balance" is the motivating physical context, not a directly measured quantity.

Sections 4–5 were revised (v0.4) following a literature review (HERMES-RP001-003) that
identified three issues in the prior draft: absence of effect-size priors for power analysis,
a documented seasonal sign reversal of the LST effect in Mediterranean climate, and a
photovoltaic-specific emissivity retrieval bias. All three are addressed below.

---

## 1. Case Selection Criteria

**Status:** Draft

A transformation site qualifies as a valid treatment case for RP001 if it satisfies all of
the following:

1. **Size threshold** — the transformed area must span at least a defined minimum number of
   clean thermal pixels (Section 4 pixel-count rule). Placeholder: ≥ 25 ha contiguous with
   Landsat-class thermal data.
2. **Age threshold** — the transformation must have existed, unchanged in footprint, for at
   least 2 full years prior to the observation window.
3. **Documented transformation date** — verifiable independently, not inferred from the
   outcome dataset. (Required also for the before/after design in Section 4.5.)
4. **No concurrent confounding transformation within 2 km of the sampled interior pixels**
   (ADR-004 clean-zone rule). Buffer of 2 km validated by literature: the solar "cool island"
   effect is observed to extend ~700 m from plant boundaries (Longyangxia, Stateline studies),
   so 2 km is a conservative margin.

**Selection order across transformation classes** (ADR-001 bias mitigation), ordered by data
availability and verifiability, NOT by expected outcome:

1. Photovoltaic installations
2. Logistics hubs / large parking areas
3. Urban expansion
4. Remaining Foundation classes in order of dataset availability

## 2. Control Area Selection Criteria

**Status:** Draft

A control area is valid if, relative to the treatment area, it matches within tolerance on:
climate zone (Köppen, exact match), elevation (±100 m placeholder), pre-transformation land
cover class, latitude (±2°), distance to nearest water body (same order of magnitude), and —
per the 2026-07-10 update — has no large-scale anthropogenic transformation within 2 km of
its own sampled interior pixels (same ADR-004 clean-zone check as treatment sites).

Control areas selected **before** outcome data is examined. Minimum 2 control areas per
treatment case (hard requirement — the Section 5 variance estimation and the
difference-in-differences design both depend on it).

## 3. Confounding Variables to Control For

**Status:** Draft

Minimum set: pre-transformation land cover class; elevation; latitude/climate zone; proximity
to water bodies; regional weather anomalies in the observation window; seasonal timing
(matched treatment/control); concurrent regional-scale change (drought, wildfire); time of
satellite overpass (LST is diurnal — same sensor, comparable overpass times); surface
emissivity (see Section 4.1 limitation).

**NDVI is deliberately NOT in this list as a controlled covariate** — see Section 4.3 for the
reasoning (NDVI is a mediator of the transformation's effect, not a confounder; controlling
for it would answer a different, narrower question than RP001 poses).

---

## 4. Outcomes and Metrics

**Status:** Revised with Opus 4.8 (v0.4) — ready for Owner lock

### 4.1 Primary outcome — Land Surface Temperature (LST)

Per ADR-002. Data source: Landsat 8/9 Collection 2 Level-2 surface temperature product
(atmospherically corrected, 30 m grid). Secondary cross-check: MODIS MOD11/MYD11 (~1 km).

**Pixel-count rule:** a treatment site must contain ≥ 30 valid (cloud-free, non-edge) interior
Landsat LST pixels, after a one-pixel boundary buffer (mixed-pixel exclusion) and, per ADR-004,
≥ 2 km from any other identified transformation.

**Known limitation — photovoltaic emissivity bias (documented, not corrected).** PV panels
have lower emissivity (~0.8–0.87) than natural vegetated/soil surfaces (>0.9). The standard
Landsat C2 L2 LST product assumes natural-surface emissivity, so LST over the treatment site
may carry a systematic retrieval bias not present at natural-cover control sites. Building a
PV-specific emissivity correction is deliberately out of scope (it would replace the
reproducible standard product with a contestable custom model, contradicting ADR-002's
rationale). This asymmetric bias is declared as a limitation on every RP001 LST result.

**Partial safeguard against misattribution:** an emissivity artifact would be approximately
constant in sign across the year. The documented Mediterranean seasonal *sign reversal* of the
LST effect (Section 4.4) therefore cannot be explained by emissivity bias alone — a
sign-reversing seasonal signal is evidence of a real physical effect, not a pure retrieval
artifact. This does not remove the bias but bounds its interpretation.

### 4.2 Secondary outcome — Albedo

Surface shortwave reflectance from the Landsat C2 L2 surface reflectance product
(narrowband-to-broadband conversion). Reported as secondary; not an independent confirmatory
test.

### 4.3 NDVI — mediator, not covariate; and the "total effect" framing

RP001 measures the **total effect** of the anthropogenic transformation on LST — including the
pathway by which the transformation alters vegetation, which in turn alters LST. Vegetation
removal/alteration is *part of what "transforming" the land means*, consistent with the
research question's framing of "anthropogenic transformation" as a whole.

Therefore NDVI is treated as a **mediator** of the effect, not a confounder, and is **excluded
from the confirmatory model as a covariate**. Controlling for a mediator would block part of
the very effect RP001 aims to measure (over-control / mediator-blocking bias) and would answer
a narrower question ("the direct effect of panels at fixed vegetation") than the one posed.

NDVI is retained as a **descriptive/diagnostic variable** and as the basis for the Section 4.5
secondary vegetation outcome. A formal mediation analysis (how much of the LST effect is
transmitted via vegetation change) is logged as **exploratory only** — see EXPLORATORY_HYPOTHESES.md.

**NDVI reliability caveat over treatment pixels:** after construction, NDVI over the treatment
footprint reflects a mixed panel+soil+inter-row-vegetation spectral signature, not residual
vegetation alone. NDVI over post-construction treatment pixels is therefore an optical-signature
descriptor, not a clean vegetation measure — recorded as a limitation wherever NDVI is used.

### 4.4 Seasonal structure of the LST outcome (critical revision)

Literature for the same climate zone (Hurduc et al. 2024, Alentejo, Portugal — Mediterranean)
documents that the solar-park LST effect **reverses sign seasonally**: cooling in summer,
warming in winter, reducing the amplitude of the seasonal cycle.

**Consequence for the confirmatory design:** aggregating across a full year into a single
per-site LST summary (the prior v0.3 design) could cancel two genuine, opposite-signed seasonal
effects toward a false null. RP001 therefore does **not** use an annual aggregate as the
confirmatory outcome. Instead:

- The confirmatory analysis is **season-stratified**. Summer (JJA) and winter (DJF) are the
  two pre-registered seasonal windows.
- The mixed-effects model (Section 5) includes a **season × treatment-status interaction**.
- Two pre-registered confirmatory hypotheses result (Section 5.3), one per season, each with
  its own null.

Spring/autumn are analysed as **exploratory** (transition seasons, less clear prior), not
confirmatory.

### 4.5 Secondary outcome — vegetation change via difference-in-differences (before/after)

Motivated by the research question's "transformation" framing and by the availability of
verifiable pre-transformation imagery (Criterion 3): RP001 includes a **secondary,
difference-in-differences (DiD)** outcome on vegetation.

- **Estimand:** (ΔNDVI treatment: after − before) − (ΔNDVI control: after − before).
- **Why DiD, not simple before/after:** the control term absorbs the common climatic/inter-annual
  trend (e.g. a wet 2018 vs. a dry 2025), isolating the transformation-attributable change from
  background climate variability. A simple before/after on the treatment alone cannot separate
  the two and is explicitly rejected as insufficient.
- **Before window:** pre-construction (for Case 001, groundbreaking March 2019 → use pre-2019
  imagery, consistent with the 2018 scene already identified).
- **Status:** secondary outcome, reported alongside but not as the primary confirmatory test.
  Subject to the Section 4.3 NDVI mixed-signature caveat over treatment pixels.

### 4.6 Observation window and temporal pairing

- Cloud-free thermal retrievals over ≥ one full annual cycle, so both seasonal windows are
  populated.
- Treatment and control observations **paired in time** (same/near-adjacent overpass dates).
  **This pairing rests on an explicit, verifiable assumption:** that regional weather anomalies
  on a given date affect treatment and control comparably. This assumption is checked (Section
  3 lists regional weather anomaly as a controlled variable) and reported, not merely asserted.
- Per-site LST summarised per date (median of valid interior pixels), then within each seasonal
  window — producing per-site, per-season distributions, not a pooled-pixel dataset.

---

## 5. Statistical Design, Test, and Significance Threshold

**Status:** Revised with Opus 4.8 (v0.4) — ready for Owner lock

### 5.1 Unit of analysis

The unit of analysis is the **site**, not the pixel — non-negotiable without a new ADR.
Pixels within a site are spatially autocorrelated and not independent; treating them as
independent would inflate the effective sample size and produce false positives.

### 5.2 Model

Linear mixed-effects model with:

- **Fixed effects:** treatment status (treatment vs control); season (JJA/DJF);
  **season × treatment-status interaction** (the term of primary interest, per Section 4.4);
  Section 3 confounders as covariates.
- **Random effect:** site (and matched control-cluster), capturing the nested structure
  (observations within sites within matched clusters).

Per-site aggregation (Section 4.6) plus the site random effect jointly address within-site
spatial autocorrelation. Residual spatial autocorrelation is checked (Moran's I on residuals)
and reported, not hidden.

### 5.3 Confirmatory tests and threshold

Two pre-registered confirmatory hypotheses, from the season × treatment interaction:

- **H0(summer):** no treatment–control LST difference in JJA, controlling for covariates.
- **H0(winter):** no treatment–control LST difference in DJF, controlling for covariates.

- **Threshold:** α = 0.05, **two-tailed** (direction not assumed a priori — essential here,
  since the literature predicts opposite signs by season; falsifiability preserved in both
  directions).
- **Multiple-comparisons correction:** the confirmatory family is {H0(summer), H0(winter)}
  per transformation class. Benjamini–Hochberg FDR correction applied across this family. As
  more transformation classes are added, they extend the family. Albedo (4.2), the vegetation
  DiD (4.5), spring/autumn, and any mediation analysis are **exploratory** and excluded from
  the confirmatory family.

### 5.4 Effect size (mandatory alongside p-value)

Every confirmatory result reports the estimated LST difference in **°C with 95% CI** (the
physically meaningful effect size) and a standardised effect size. A statistically significant
but physically negligible difference is reported as such — significance is not promoted to
physical importance.

### 5.5 Statistical power (computed BEFORE acquisition), using literature priors

Power is driven by the **number of matched site clusters**, not pixel count. Two literature-
derived effect-size scenarios bound the power analysis:

- **Global annual prior:** ~0.5 K daytime LST effect (116-farm global assessment). Small — a
  conservative lower bound requiring many sites.
- **Mediterranean summer prior:** ~2 K summer treatment–control differential (Hurduc et al.,
  same climate zone as Case 001). Large — the season-stratified design (Section 4.4) is powered
  primarily against this, and a ~2 K summer effect requires far fewer sites than a 0.5 K annual
  effect.

The pre-registered minimum effect size of interest, and the resulting minimum number of
treatment sites (each with ≥ 2 controls), are set before acquisition. **If the achievable
number of qualifying sites is below the powered minimum, RP001 is reported as underpowered
rather than proceeding to over-claim.** Where a site's usable sample is an ADR-004 clean zone
smaller than its full footprint, the actual clean-zone pixel count is used.

### 5.6 Case 001 status: pilot / proof-of-methodology, not confirmatory alone

With a single treatment site (Case 001) plus 2 controls, the site-level random effect has
minimal degrees of freedom — n=1 treatment cannot support a confirmatory site-level inference.
**Case 001 alone is therefore a pilot / proof-of-methodology**, used to validate the end-to-end
pipeline (acquisition → LST extraction → seasonal model) and to produce a first effect-size
estimate. Confirmatory inference for RP001 requires the multi-site sample sized per Section 5.5.
This framing is explicit to avoid over-interpreting a single-site result.

### 5.7 Pre-registration lock

Sections 4–5 constitute the pre-registered analysis plan. Once locked, any deviation (primary
outcome, model structure, seasonal stratification, test, threshold, correction, or effect-size
definition) requires a new ADR and is reported in publication as a pre-registration deviation.
Post-hoc, data-dependent decisions are exploratory by definition and labelled as such (see
EXPLORATORY_HYPOTHESES.md).

---

## Status of This Document

- Sections 1–3: Draft, ready for standard technical review.
- Sections 4–5: Revised with Opus 4.8 after literature review. Ready for **Owner lock decision**.

Human responsibility note (per governance/AI_USAGE.md): AI has drafted and reviewed this
methodology as technical assistant. Final approval and locking of the pre-registration is a
human decision reserved to the Owner.

## Related Documents

- `research_programs/RP001-surface-transformation-energy-balance/RESEARCH_QUESTION.md`
- `research_programs/RP001-surface-transformation-energy-balance/EXPLORATORY_HYPOTHESES.md`
- `research_programs/RP001-surface-transformation-energy-balance/LITERATURE_BRIEFING_sections4-5.md`
- `governance/adr/ADR-001-generalized-scope.md`
- `governance/adr/ADR-002-lst-primary-outcome.md`
- `governance/adr/ADR-004-criterion4-refinement.md`

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial draft; Sections 1–3 drafted, Sections 4–5 flagged for Opus review |
| 0.2.0 | 2026-07-10 | Sections 4–5 completed and reviewed with Opus 4.8 (LST primary, site as unit, mixed-effects, FDR, power on site count) |
| 0.3.0 | 2026-07-10 | Section 1 Criterion 4 refined per ADR-004; Section 2 control-area no-nearby-transformation check; linked EXPLORATORY_HYPOTHESES.md |
| 0.4.0 | 2026-07-11 | Post-literature-review revision (Opus 4.8): season-stratified confirmatory design with season×treatment interaction and two seasonal nulls (4.4, 5.3); NDVI reclassified as mediator, excluded from confirmatory model, total-effect framing (4.3); vegetation difference-in-differences added as secondary outcome (4.5); emissivity bias documented as limitation with seasonal-reversal safeguard (4.1); temporal pairing stated as explicit assumption (4.6); power analysis bound by literature effect-size priors (5.5); Case 001 framed as pilot/proof-of-methodology (5.6) |
