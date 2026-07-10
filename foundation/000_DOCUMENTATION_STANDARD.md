# HERMES
# DOC-000 — Documentation Standard

- **Document ID:** HERMES-FND-000
- **Version:** 0.1.1
- **Status:** Approved
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Systems Architect / Scientific Method Reviewer role)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** N/A (applies to all)
- **Related ADR:** ADR-000
- **License:** TBD (see foundation license decision)

---

## 1. Purpose

This document defines the documentation standards for the HERMES project.

The objective is to ensure that every document produced by the project is:

- understandable;
- traceable;
- versioned;
- reproducible;
- reviewable.

The documentation is considered part of the scientific method.

## 2. Guiding Principles

Documentation shall:

1. Describe reality as accurately as possible.
2. Distinguish facts from assumptions.
3. Distinguish observations from interpretations.
4. Record uncertainty.
5. Preserve project history.

## 3. Mandatory Metadata

Every document shall begin with:

- Document ID
- Title
- Version
- Status
- Owner
- Reviewers
- Last Updated
- Related Research Questions
- Related ADR
- License

## 4. Versioning

Semantic Versioning is adopted.

`Major.Minor.Patch`

- Major: structural changes
- Minor: new content
- Patch: corrections

## 5. Document Structure

Executive Summary

Purpose

Scope

Definitions

Scientific Context

Requirements

Implementation

Validation

Limitations

Future Work

References

Appendices

## 6. Naming Convention

Foundation documents:

`HERMES-FND-XXX`

Research Programs:

`HERMES-RPXXX`

Architecture Decisions:

`ADR-XXXX`

Request for Comments:

`RFC-XXXX`

## 7. References

Every factual statement should reference its source whenever practical.

## 8. Traceability

Every figure, table, algorithm and conclusion must be traceable back to:

- Research Question
- Dataset
- Software Version
- Commit ID
- Configuration

## 9. Review Workflow

Draft → Technical Review → Scientific Review → Approved

## 10. Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial draft |
| 0.1.1 | 2026-07-10 | Added mandatory metadata block per own §3 requirement |
