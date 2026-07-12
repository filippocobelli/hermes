# HERMES
# RP001 — Literature Review Briefing for Sections 4–5 Revision

- **Document ID:** HERMES-RP001-003
- **Version:** 0.1.0
- **Status:** Input document for Opus 4.8 methodology review — not itself part of the pre-registration
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Scientific Method Reviewer role — Sonnet 5, literature search)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** RP001
- **Related ADR:** ADR-002
- **License:** TBD

---

## Purpose

Before locking `HYPOTHESES.md` Sections 4–5, a literature review was performed (requested
explicitly, to check RP001's design against prior work before finalizing). Three concrete
issues were found that affect falsifiability and are not yet addressed in the current draft.
This document is the input briefing for the next Opus 4.8 review pass — it does not itself
modify the pre-registration.

## Finding 1 — Effect size priors exist and should inform the power analysis

HYPOTHESES.md Section 5.5 requires a power analysis "before data acquisition" using a
"pre-specified minimum effect size of interest," but no actual number has been used yet.
Literature provides usable priors:

- **Global average (116 solar farms, all climates):** daytime LST effect of approximately
  -0.5 K (SD ~0.43 K), weaker nighttime effect of approximately -0.2 K (SD ~0.25 K).
  Source: global remote-sensing assessment of solar farm effects on albedo/LST
  (ScienceDirect, Reading University).
- **Closest direct analog to Case 001 (Mediterranean climate, Alentejo, Portugal, 46 MW,
  Landsat 8, monthly means 2013–2021):** summertime (JJA) comparison showed the control area
  warming by approximately +1.74°C over the study period while the solar park area cooled by
  approximately -0.23°C — a summer-specific differential much larger than the global annual
  average. Source: Hurduc et al. 2024, *Renewable Energy*, "Impact of a small-scale solar
  park on temperature and vegetation parameters obtained from Landsat 8."

**Action needed:** Section 5.5's power analysis should be run using both the global prior
(~0.5 K) and the Mediterranean-specific, season-stratified prior (~2 K summer differential)
as bounding scenarios, since Case 001 shares the exact climate zone of the closest analog.

## Finding 2 — Documented seasonal sign reversal in Mediterranean climate specifically

The same Hurduc et al. study found the LST effect is seasonal and reverses sign: positive
(warming) anomalies in cold months, negative (cooling) anomalies in summer, for a solar park
in the *same climate zone as Núñez de Balboa*.

**Implication for HYPOTHESES.md Section 4.4:** the current design aggregates observations
"over a defined multi-season window (minimum one full annual cycle)" into a single per-site
summary. If the effect genuinely reverses sign seasonally, annual aggregation risks cancelling
a real effect toward a false null result — the opposite of the intended conservative design.

**Action needed:** Section 4.4/5.2 should be revised so the mixed-effects model includes
season (or month, or a summer/winter indicator) as an interaction term with treatment status,
not just as an aggregated-over covariate. The confirmatory test (Section 5.3) may need to
become season-stratified, with implications for the multiple-comparisons correction (Section
5.3) and the required sample size (Section 5.5).

## Finding 3 — Emissivity mismatch risk for the primary outcome variable

Multiple sources note that photovoltaic panel surfaces have markedly lower emissivity
(approximately 0.8–0.87) than natural vegetated/soil surfaces (typically >0.9–0.94), and that
standard satellite LST retrieval algorithms are generally calibrated assuming natural-surface
emissivity. Recent work (2026) specifically develops PV-specific emissivity parameterization
because conventional land-surface-emissivity-based LST retrieval introduces substantial error
over solar arrays (RMSE improvements from ~11–19°C down to ~4–9°C reported when correcting
for this).

**Implication for HYPOTHESES.md Section 4.1:** RP001 uses the standard Landsat Collection 2
Level-2 LST product (ADR-002), which uses a general land-surface emissivity model, not a
PV-specific one. This means the treatment site's LST values may carry a systematic retrieval
bias that does not apply symmetrically to control sites (which are natural land cover, where
standard emissivity assumptions are more appropriate).

**Action needed:** this must be documented explicitly as a **known limitation** of using the
standard Level-2 product (not necessarily fixed before locking, since building a custom
PV-specific emissivity correction is a substantial undertaking outside RP001's current scope
per ADR-002's own reasoning for choosing the reproducible standard product over custom
modelling). At minimum, Section 4.1 or a new "Limitations" note should state that the LST
comparison may be affected by a differential retrieval bias specific to photovoltaic surfaces,
distinguishing this from a genuine physical temperature difference.

## Finding 4 (supporting, not requiring action) — Buffer distance validated by literature

Two independent studies (Longyangxia, China, 850 MW; Stateline, USA, 300 MW), using
field-based measurements, found the solar-park "cool island" effect on surrounding land
extends up to approximately 700–730 m from the plant boundary, with LST reductions up to
2.3°C near the edge, decaying exponentially with distance. HERMES's 2 km buffer (ADR-004,
HYPOTHESES.md Section 1 Criterion 4 / Section 2) is therefore well within a conservative
margin above the empirically observed effect radius. No action needed — this is recorded to
strengthen the pre-registration's justification (the buffer is evidence-based, not arbitrary).

## Finding 5 (context, exploratory only) — Regional mesoscale effects are a real but separate research question

See `EXPLORATORY_HYPOTHESES.md` EH-002. Literature confirms regional land-use clustering can
plausibly affect mesoscale precipitation/climate, but existing evidence is almost entirely
from climate-model studies at installed areas far larger than Extremadura's current
build-out. This does not require any change to RP001's design; logged separately as a future
Research Program candidate.

## Summary of Required Changes to HYPOTHESES.md (for Opus review)

1. Section 5.5: run power analysis using literature-derived effect sizes (0.5 K global prior
   and ~2 K Mediterranean-summer prior) rather than an unspecified placeholder.
2. Section 4.4 / 5.2 / 5.3: add season as an interaction term with treatment status in the
   mixed-effects model; reconsider whether the confirmatory test should be season-stratified,
   with corresponding update to the multiple-comparisons correction.
3. Section 4.1: add an explicit, documented limitation regarding PV-specific emissivity
   retrieval bias in the standard Landsat C2 L2 product.
4. No change needed to the 2 km buffer (Section 1/2) — literature-validated as conservative.

## Related Documents

- `research_programs/RP001-surface-transformation-energy-balance/HYPOTHESES.md`
- `research_programs/RP001-surface-transformation-energy-balance/EXPLORATORY_HYPOTHESES.md`
- `governance/adr/ADR-002-lst-primary-outcome.md`

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial literature briefing, prepared ahead of Opus 4.8 review of Sections 4-5 |
