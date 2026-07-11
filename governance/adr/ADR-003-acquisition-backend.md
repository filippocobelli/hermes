# ADR-003 — Data Acquisition Backend: STAC via Microsoft Planetary Computer, Behind an Abstract Interface

- **Document ID:** ADR-003
- **Version:** 0.1.0
- **Status:** Accepted
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Systems Architect role — Sonnet 5)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** RP001
- **Related ADR:** ADR-002
- **License:** TBD

---

## Title

Selection of Microsoft Planetary Computer (STAC API) as the initial Layer 1 data acquisition
backend, isolated behind an abstract `DataSource` interface.

## Status

Accepted

## Context

Per ADR-002, RP001 requires Landsat Collection 2 Level-2 scenes (LST + surface reflectance).
Three realistic access paths exist:

1. **USGS M2M / EarthExplorer API** — the authoritative official source. Requires account
   registration and API credentials. Gives the exact Level-2 products used in ADR-002.
2. **Microsoft Planetary Computer (STAC API)** — public STAC catalogue mirroring Landsat
   Collection 2 Level-2, no heavyweight auth (SAS-token signing only), good for rapid
   prototyping, widely used in the remote-sensing community.
3. **Google Earth Engine** — powerful but introduces a proprietary compute/query environment.
   Conflicts with the Foundation success criterion that results must be reproducible "without
   requiring information outside the repository."

## Decision

Layer 1 (`src/hermes/acquisition/`) is built around an abstract `DataSource` interface
(`base.py`), so the acquisition backend is swappable without touching Layers 2–6.

The initial concrete implementation targets **Microsoft Planetary Computer's STAC API**, using
the same Landsat Collection 2 Level-2 collection specified in ADR-002. This is a prototyping
and development choice, not a permanent commitment to a third-party service.

An official **USGS M2M-backed implementation** is deferred but explicitly anticipated as a
second `DataSource` implementation before RP001 moves from prototyping to locked dataset
acquisition for publication — because the Foundation's Data Principles favour authoritative
public sources with the longest-term availability guarantee, and USGS is the data's origin.

## Alternatives Considered

**A. USGS M2M as the only implementation from day one.**
Rejected as the *starting* point (not rejected long-term). Registration and credential setup
would slow initial prototyping of Layers 2–6, which do not depend on which backend is used.

**B. Google Earth Engine.**
Rejected. Conflicts with the "reproducible from public datasets without external
information" success criterion — GEE requires its own account, quota, and proprietary
compute model that a reviewer would need to replicate exactly.

**C. Direct concrete implementation with no abstract interface (call Planetary Computer
directly from Layers 2+).**
Rejected. Would hard-couple the entire pipeline to one third-party service, contradicting the
"Every output should be reproducible" and "Software should be modular" principles in
`foundation/008_SYSTEM_ARCHITECTURE.md`.

## Consequences

### Positive

- Layers 2–6 depend only on `AcquiredScene` / `DataSource`, never on Planetary Computer
  specifics — swapping to USGS M2M later requires a new class, not a rewrite.
- Faster path to a working end-to-end pipeline for methodology testing.
- Every downloaded scene records a `provenance.json` (source, STAC item ID, retrieval
  timestamp, asset checksums) per Foundation Data Principles ("store provenance").

### Negative / Risks

- Planetary Computer is a third-party service (Microsoft); its continued availability,
  rate limits, or catalogue completeness are outside HERMES's control. This is an accepted,
  bounded risk for the prototyping phase only.
- Original USGS scene identifiers must be preserved in provenance so that a future switch to
  USGS M2M can be verified to reference the *same* underlying scenes, not just equivalent
  ones.
- The abstract interface adds a small amount of upfront design overhead versus calling the
  API directly; considered justified given the swap is anticipated, not hypothetical.

## Related Documents

- `governance/adr/ADR-002-lst-primary-outcome.md`
- `foundation/008_SYSTEM_ARCHITECTURE.md`
- `software/src/hermes/acquisition/`

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial ADR |
