# ADR-002 — Land Surface Temperature as Primary Outcome for RP001

- **Document ID:** ADR-002
- **Version:** 0.1.0
- **Status:** Accepted
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Systems Architect / Scientific Method Reviewer role — Opus 4.8)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** RP001
- **Related ADR:** ADR-001
- **License:** TBD

---

## Title

Adoption of Land Surface Temperature (LST) as the declared primary outcome of RP001, with
surface energy balance treated as interpretation rather than direct measurement.

## Status

Accepted

## Context

RP001's original primary question asks whether anthropogenic land transformation produces
statistically significant changes in *surface energy balance*.

Surface energy balance is the net result of several fluxes: net radiation, sensible heat
flux, latent heat flux, and ground heat flux. Measuring these directly requires either
in-situ instrumentation (flux towers, which the project does not plan to deploy) or
energy-balance models such as SEBAL or METRIC applied to satellite imagery.

The problem with model-based energy balance for RP001: SEBAL/METRIC introduce their own
substantial assumptions (aerodynamic resistance parameterisation, selection of "hot" and
"cold" anchor pixels, atmospheric correction choices). These assumptions are themselves
sources of uncertainty and potential bias, and they are difficult for an independent
reviewer to reproduce identically. Building the falsifiability of RP001 on top of a model
whose assumptions are contestable weakens the very property HERMES exists to protect:
reproducibility and clean falsifiability.

By contrast, Land Surface Temperature (LST) is a directly retrievable quantity from
satellite thermal infrared bands (Landsat 8/9 TIRS, Sentinel-3 SLSTR, MODIS), with
established, publicly documented retrieval algorithms. It is a *component/proxy* of surface
energy behaviour, not the full energy balance, but it is measurable, reproducible, and its
limitations are well understood.

## Decision

RP001 declares **Land Surface Temperature (LST)** as its primary outcome variable, and
**albedo** (surface reflectance) as a secondary outcome.

The concept "surface energy balance" is retained in the framing and discussion of RP001 as
the *motivating physical context*, but it is explicitly NOT claimed as a directly measured
quantity. Any statement RP001 makes about energy balance is an *interpretation* of LST and
albedo results, clearly labelled as such, and subject to the Foundation principle that
correlation and proxy measurement shall never be silently promoted to mechanistic or causal
claims.

RP001's primary question is therefore refined to:

> Does large-scale anthropogenic transformation of land surfaces produce statistically
> significant changes in Land Surface Temperature (and, secondarily, albedo) compared with
> equivalent control areas, after controlling for known environmental variables?

## Alternatives Considered

**A. Keep "surface energy balance" as the measured outcome, using SEBAL/METRIC.**
Rejected for RP001. Introduces model-dependent assumptions that compromise reproducibility
and give an independent reviewer too many contestable degrees of freedom. May be revisited
as a *separate future Research Program* explicitly about energy-balance modelling, where the
model assumptions themselves are the subject of study.

**B. Deploy in-situ flux instrumentation.**
Rejected. Out of scope, not planned, not fundable at project scale, and would destroy the
"reproducible from public datasets" success criterion.

**C. Declare LST as primary outcome (chosen).**
Accepted. Measurable, reproducible, public data, well-documented retrieval. Honest about
being a proxy.

## Consequences

### Positive

- Preserves clean falsifiability and reproducibility: LST retrieval from public imagery can
  be independently re-executed.
- Removes a large class of contestable model assumptions from RP001's core claim.
- Keeps the honest epistemic distinction between what is measured (LST) and what is inferred
  (energy balance implications).

### Negative / Risks

- **Scientific Method Reviewer note:** LST is a proxy. There is a standing risk that readers
  (or the project itself) will over-interpret an LST difference as an energy-balance or
  climate claim. Every RP001 output must carry the explicit caveat that LST is a surface
  radiative temperature, influenced by emissivity, time of day, viewing geometry and
  atmospheric conditions, and is not equivalent to air temperature or to net energy balance.
- LST from thermal satellite bands has coarser native resolution than optical bands
  (e.g. Landsat TIRS ~100 m resampled to 30 m; MODIS ~1 km). This interacts with the site
  size threshold in HYPOTHESES.md Section 1 and must be reconciled there.
- Cloud cover limits thermal retrieval; usable observation windows will be fewer than for a
  purely optical study. This affects statistical power (see HYPOTHESES.md Section 5).
- This decision narrows RP001's claim scope. That is intentional and considered a strength,
  but it must be communicated so RP001 is not later criticised for "not really measuring
  energy balance" — the narrowing is deliberate and documented here.

## Related Documents

- `research_programs/RP001-surface-transformation-energy-balance/RESEARCH_QUESTION.md`
- `research_programs/RP001-surface-transformation-energy-balance/HYPOTHESES.md`
- `governance/adr/ADR-001-generalized-scope.md`

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial ADR; LST declared primary outcome, energy balance demoted to interpretation |
