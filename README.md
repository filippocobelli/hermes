# HERMES
**Holistic Energy Research Model for Environmental Systems**

> Open scientific framework for reproducible research on anthropogenic energy balance, land transformation and environmental systems.

---

## Project Status

**Version:** 0.1.0 (Foundation)

HERMES is an open scientific framework whose objective is to build transparent, reproducible methods for investigating environmental systems and anthropogenic transformations.

The framework does **not** begin from conclusions.

It begins from scientific questions.

---

## Core Objectives

- Build a fully reproducible scientific workflow.
- Use open datasets whenever possible.
- Document every methodological decision.
- Publish code, documentation and validation procedures.
- Preserve negative results.
- Separate observation, correlation, causation and interpretation.

---

## First Research Program

**RP001 — Surface Transformation and Energy Balance**

Primary research question:

> Does large-scale anthropogenic land transformation produce statistically significant changes in surface energy balance after controlling for known environmental variables?

See [`research_programs/RP001-surface-transformation-energy-balance/`](research_programs/RP001-surface-transformation-energy-balance/).

---

## Repository Structure

```
foundation/
governance/
research_programs/
software/
datasets/
documentation/
publications/
tests/
tools/
```

---

## Guiding Principles

1. Evidence before belief.
2. Method before conclusion.
3. Verification before trust.
4. Reproducibility is mandatory.
5. Every hypothesis must be falsifiable.
6. Every important decision is documented.
7. Better evidence replaces previous evidence.

Full details: [`foundation/FOUNDATION.md`](foundation/FOUNDATION.md)

---

## Development Workflow

Every task follows the same lifecycle:

```
Research Question
        ↓
Specification
        ↓
Implementation
        ↓
Validation
        ↓
Review
        ↓
Release
```

No code is considered complete without documentation and validation.

---

## Documentation Standard

All documents in this project follow [`foundation/000_DOCUMENTATION_STANDARD.md`](foundation/000_DOCUMENTATION_STANDARD.md).

Architecture decisions are recorded as ADRs in [`governance/adr/`](governance/adr/).

Terminology is standardized in [`foundation/GLOSSARY.md`](foundation/GLOSSARY.md).

---

## AI Transparency

This project makes use of AI-assisted drafting tools for documentation, software architecture discussions and code generation support.

Artificial intelligence is used as a technical assistant, not as a scientific authority.

All scientific decisions, methodological choices, validation procedures and project governance remain under human responsibility.

Full policy: [`governance/AI_USAGE.md`](governance/AI_USAGE.md)

---

## Roadmap

Foundation → Bootstrap → Dataset Acquisition → Scientific Analysis → Validation → Publication

---

## Contributing

The contribution process will be defined in `CONTRIBUTING.md`.

---

## License

To be defined during Foundation.

---

## Citation

Citation instructions will be provided through `CITATION.cff`.

---

## Philosophy

Do not trust the conclusions.

Inspect the method.

Run the code.

Verify the data.

Improve the model.
