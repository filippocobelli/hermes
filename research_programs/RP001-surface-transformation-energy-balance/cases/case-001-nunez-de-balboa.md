# HERMES
# RP001 — Case 001: Núñez de Balboa Photovoltaic Plant

- **Document ID:** HERMES-RP001-CASE-001
- **Version:** 0.2.0
- **Status:** Case Selection Approved (Criteria 1–4) — Control Area identification pending
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Scientific Method Reviewer role — Sonnet 5)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** RP001
- **Related ADR:** ADR-001, ADR-002, ADR-003, ADR-004
- **License:** TBD

---

## Site Identification

- **Name:** Núñez de Balboa Photovoltaic Plant
- **Operator/Owner:** Iberdrola Renovables Energía (100%)
- **Location:** Municipalities of Usagre, Hinojosa del Valle and Bienvenida, Province of
  Badajoz, Extremadura, Spain
- **Coordinates (centroid, WGS84):** 38.4533, -6.2260
- **Capacity:** 500 MWp / 391 MWac
- **Area (official):** ~943–1,000 ha (sources vary)
- **Area (measured, OSM geometry, this case):** 858 ha total footprint; 808.2 ha interior
  after one-pixel (30 m) edge buffer
- **Commissioning date:** First power to grid April 2020

## Acquisition Bounding Box (for Layer 1 `AcquisitionRequest`)

```
bbox = (-6.2657, 38.4227, -6.1857, 38.4827)  # (min_lon, min_lat, max_lon, max_lat)
```

## Case Selection Criteria Check (HYPOTHESES.md Section 1) — Final

| Criterion | Status | Notes |
|---|---|---|
| 1. Size ≥ 25 ha / ≥ 30 valid interior Landsat pixels | ✅ Pass | 808.2 ha interior; ~8,980 raw interior pixels before neighbour subtraction |
| 2. Age ≥ 2 years, unchanged footprint | ✅ Pass | Commissioned 2020; 6 years stable as of 2026 |
| 3. Documented transformation date, independently verifiable | ✅ Pass | Multiple independent sources (Iberdrola, Global Energy Monitor, Copernicus/Sentinel-2 2020 imagery) |
| 4. No confounding transformation within 2 km of sampled pixels (ADR-004, refined) | ✅ **Pass** | Two neighbouring solar plants found (86.7 ha at 1,453 m; 38.1 ha at 1,680 m), both real and distinct (not internal sub-components — confirmed via geometry-based clustering after an initial centroid-distance methodology error was caught and fixed). Clean sampling zone after subtracting both neighbours' 2 km buffers: **786.2 ha, ~8,736 valid interior Landsat pixels** — vastly exceeds the 30-pixel minimum. |

**Case Selection: APPROVED.** All four criteria satisfied. Sampling for this case must be
restricted to the clean sampling zone (786.2 ha sub-region), computed via
`software/examples/compute_case001_clean_zone.py`, not the full footprint.

## Verification Method Notes (for reproducibility)

- Footprint and neighbour geometries retrieved from OpenStreetMap via Overpass API
  (`power=plant`, `power=generator`+`generator:source=solar` tags), not from visual estimation.
- An initial check using a single centroid-to-point distance flagged 31 "confounding"
  features — this was a methodology error (OSM maps individual panel-array blocks as
  separate ways within the same plant). Fixed by clustering adjacent/overlapping polygons
  before measuring distance. Documented here so the error is not silently repeated for
  future cases.
- Clean-zone computation: erode footprint by 30 m (edge-mixing buffer) → subtract 2 km buffer
  around each confirmed external neighbour → remaining area / 900 m² per pixel.
- Sentinel-2 true-color visual inspection was also performed (lower confidence, human
  interpretation only) — geometry-based OSM check is the authoritative verification for this
  case; the visual check served only as an initial screening step.

## Outstanding Items (before Case 001 is fully ready for acquisition)

1. **Control area identification** — HYPOTHESES.md Section 2 requires ≥ 2 control areas
   matching climate zone, elevation, pre-transformation land cover, latitude, water
   proximity, AND (per the 2026-07-10 update) passing the same no-nearby-transformation
   check used here for the treatment site. Not yet done.
2. **Pre-transformation land cover class** — needed for control area matching. Likely dry
   cereal cropland / dehesa-type pastureland typical of Tierra de Barros; to be confirmed via
   pre-2019 archival imagery, not assumed.

## Related Documents

- `research_programs/RP001-surface-transformation-energy-balance/HYPOTHESES.md`
- `governance/adr/ADR-003-acquisition-backend.md`
- `governance/adr/ADR-004-criterion4-refinement.md`
- `software/examples/check_case001_confounders_geom.py`
- `software/examples/compute_case001_clean_zone.py`

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial case candidate identified; Criteria 1-3 pass, Criterion 4 pending visual verification |
| 0.2.0 | 2026-07-10 | Criterion 4 resolved via ADR-004 clean-zone method: PASS with 786.2 ha / ~8,736 pixels available. Case Selection approved. Control area identification now the next open task. |
