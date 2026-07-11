# ADR-004 — Refinement of Case Selection Criterion 4: Buffer Applies to Sampled Pixels, Not Full Site Perimeter

- **Document ID:** ADR-004
- **Version:** 0.1.0
- **Status:** Accepted
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Systems Architect / Scientific Method Reviewer role — Sonnet 5)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** RP001
- **Related ADR:** ADR-001, ADR-002
- **License:** TBD

---

## Title

Refinement of HYPOTHESES.md Section 1, Criterion 4 ("no concurrent confounding
transformation within a 2 km buffer") to apply to the specific pixels sampled for LST
measurement, rather than to every point of the treatment site's full perimeter.

## Status

Accepted

## Context

Case 001 (Núñez de Balboa, Badajoz, Spain) was checked against Criterion 4 using a
geometry-aware, OpenStreetMap-based method (see
`research_programs/RP001-.../cases/case-001-nunez-de-balboa.md`). After correctly excluding
the plant's own internal sub-components (individually mapped panel-array ways, initially
misidentified as 31 separate "confounding transformations" — a methodological bug in the
first version of the check, fixed by clustering adjacent/overlapping polygons before
measuring distance), two genuinely distinct, separately-tagged solar plants were found within
2 km of the Case 001 footprint: an unnamed 86.7 ha plant at 1,453 m and an unnamed 38.1 ha
plant at 1,680 m.

Applying Criterion 4 literally ("no confounding transformation within 2 km of the site") would
disqualify Case 001. However, this reveals a structural feature of the region rather than a
defect specific to this case: Extremadura has one of the highest densities of utility-scale
solar development in Europe (Iberdrola alone had over 1,300 MW of further regional pipeline
projects at the time Núñez de Balboa was commissioned). Requiring total isolation from other
transformations within 2 km would systematically exclude large photovoltaic sites in exactly
the regions where they are most common and best documented, biasing case selection toward
atypical, isolated installations rather than representative ones — itself a form of selection
bias that ADR-001 already warned against.

Separately, per HYPOTHESES.md Section 4.1, the LST outcome is measured only from pixels
strictly interior to the treatment footprint (excluding a one-pixel boundary buffer to avoid
mixed-pixel contamination at the true land-cover edge). A satellite thermal pixel's measured
value depends on the land cover directly beneath it; a separate plant 1.4–1.7 km away does not
physically contaminate an interior pixel's LST value. The real purposes Criterion 4 was meant
to serve are: (a) case purity/documentation clarity, and (b) protecting the independence of
control area selection (Section 2) — not preventing every possible photon or heat-flux
interaction at arbitrary distance.

## Decision

Criterion 4 is refined as follows:

> No concurrent confounding transformation shall be present within 2 km of the **specific
> interior pixels used for LST sampling** in a given case. If a treatment site's own footprint
> is large enough to contain a sub-region whose interior-buffered pixels are all ≥ 2 km from
> any other large-scale anthropogenic transformation, that sub-region may be used for
> sampling even if other parts of the same site's perimeter are closer to a neighbouring
> transformation.

This does not relax the criterion's intent (avoiding confounded measurements) — it corrects an
overly literal reading (applying a pixel-relevant distance rule to the entire site boundary
regardless of where sampling actually occurs).

Practical consequence for Case 001: before final approval, a "clean sampling zone" must be
computed — the portion of the treatment footprint's interior (after the standard one-pixel
edge buffer) that lies ≥ 2 km from both identified neighbouring plants — and checked against
the ≥ 30 valid interior pixel requirement (HYPOTHESES.md Section 4.1). If the clean zone
satisfies this, Case 001 is approved for Criterion 4 using only that sub-region. If not, Case
001 is disqualified and the next candidate in the Section 1 selection order is evaluated.

## Alternatives Considered

**A. Apply Criterion 4 literally to the full site perimeter (reject Case 001).**
Rejected as the sole rule. Would likely disqualify most large photovoltaic sites in
Extremadura and similar solar-dense regions, introducing a selection bias toward atypical,
isolated sites — undermining representativeness and repeating the class of bias ADR-001 was
written to avoid.

**B. Drop Criterion 4 entirely.**
Rejected. The underlying purpose (case purity, protecting control-area independence) is
legitimate and should be preserved, just applied at the correct spatial scale.

**C. Refine Criterion 4 to apply to sampled pixels, with a documented sub-region rule (chosen).**
Accepted. Preserves the criterion's intent while avoiding an overly literal application that
would bias case selection.

## Consequences

### Positive

- Avoids a selection bias that would systematically exclude representative, well-documented
  large-scale sites in solar-dense regions.
- Keeps Criterion 4 physically grounded in what can actually confound an LST measurement
  (pixel-level, not whole-site-level).
- Reusable rule for future RP001 cases in other transformation-dense regions.

### Negative / Risks

- **Reviewer note:** using only a sub-region of a large site changes the effective sample
  size (fewer interior pixels than the full footprint would provide), which feeds into the
  power analysis (HYPOTHESES.md Section 5.5) and must be recomputed with the actual clean-zone
  pixel count, not the full-site pixel count.
- If the clean-zone rule is invoked for multiple cases, it introduces a new degree of
  freedom (how the clean sub-region is drawn) that must be specified by an automatic,
  pre-defined geometric rule (as done here: erode by one pixel, then subtract 2 km buffers
  around identified neighbours) — never chosen by hand per case, to avoid the appearance of
  cherry-picking favourable pixels.
- Requires maintaining, per case, a documented list of nearby transformations checked and
  excluded/subtracted, for future independent reproducibility.

## Related Documents

- `research_programs/RP001-surface-transformation-energy-balance/HYPOTHESES.md`
- `research_programs/RP001-surface-transformation-energy-balance/cases/case-001-nunez-de-balboa.md`
- `governance/adr/ADR-001-generalized-scope.md`

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial ADR, following discovery of 2 nearby solar plants within Case 001's 2km buffer |
