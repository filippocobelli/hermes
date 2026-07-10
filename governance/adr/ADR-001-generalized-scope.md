# ADR-001 — Generalization of Scope from Photovoltaic-Specific to General Anthropogenic Transformation Framework

- **Document ID:** ADR-001
- **Version:** 0.1.0
- **Status:** Accepted
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Systems Architect / Scientific Method Reviewer role)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** RP001
- **Related ADR:** N/A
- **License:** TBD

---

## Title

Generalization of HERMES scope from photovoltaic-specific research to a general framework for studying anthropogenic land transformation and energy balance.

## Status

Accepted

## Context

The original research motivation for HERMES was a specific question: whether photovoltaic
installations measurably influence local or regional thermal balance.

During project definition, it became clear that restricting the framework to photovoltaic
systems specifically would introduce a significant risk: a framework built around a single
technology, motivated by a specific hypothesis about that technology, is structurally exposed
to confirmation bias. Every methodological choice (control area selection, metric definition,
dataset selection) would be made in the shadow of an implicit expected outcome about
photovoltaics specifically.

There is also a practical scientific concern: surface energy balance effects from anthropogenic
land transformation are not unique to photovoltaic installations. Logistics hubs, airports,
industrial districts, urban expansion, data centres, parking areas, mining sites and artificial
lakes all transform land surfaces in ways that may produce comparable, measurable effects.
A framework that can only study one class of transformation cannot distinguish an effect that
is specific to photovoltaics from an effect that is generic to any large-scale surface change —
which is itself a critical scientific question.

## Decision

HERMES scope is generalized. The framework shall be designed to study any class of
large-scale anthropogenic surface transformation, using a consistent methodology, metrics,
and validation pipeline. Photovoltaic installations become one specific case among several
(see Foundation → Initial Motivation), not the defining subject of the project.

RP001 ("Surface Transformation and Energy Balance") is scoped as the first research program
under this general framework, not as "the photovoltaic study."

## Alternatives Considered

**A. Keep HERMES photovoltaic-specific.**
Rejected. Introduces structural bias risk (see Context) and limits scientific value of the
control-area methodology, since a photovoltaic-only framework cannot test whether an observed
effect is technology-specific or generic to surface transformation.

**B. Split into two projects: a general framework and a photovoltaic-specific study built on top of it.**
Considered but deferred. Not rejected outright — this may become the actual shape of the
project once RP001 produces results. For now, a single unified framework is simpler to govern
and avoids premature architectural commitment.

## Consequences

### Positive

- Removes single-technology bias from framework design.
- Enables true control-group comparisons across transformation types (a photovoltaic site
  can be compared not only to undisturbed land but to other anthropogenic transformations).
- Increases long-term reusability of the framework for future research programs.
- Aligns with stated Mission: "reduce uncertainty," not "confirm a hypothesis about
  photovoltaics."

### Negative / Risks

- Broader scope requires more general (and more complex) data models, metrics and control-area
  definitions than a single-technology study would need. This increases Foundation and
  software design effort before RP001 can produce results.
- **Scientific Method Reviewer note:** generalization does not by itself remove bias — it only
  removes *technology-specific* bias. The project must still guard against a new risk:
  selection bias in which anthropogenic transformations get studied first, and in what order.
  If photovoltaic sites remain the first or most-resourced dataset in practice (even under a
  "general" framework), RP001 results could still be interpreted as "the photovoltaic study in
  disguise." This must be actively managed — for example by defining RP001's control area and
  case selection criteria before any specific dataset is chosen, and by documenting that
  selection order in RP001 itself.
- Scope generalization is a one-way door in terms of governance expectations: reverting to a
  narrow scope later would itself require a new ADR and public justification.

## Related Documents

- `foundation/FOUNDATION.md` — Initial Motivation, Vision, Mission
- `research_programs/RP001-surface-transformation-energy-balance/` — first program under this scope
- `foundation/008_SYSTEM_ARCHITECTURE.md`

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial ADR, documenting decision already taken during project definition |
