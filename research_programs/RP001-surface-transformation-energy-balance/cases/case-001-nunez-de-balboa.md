# HERMES
# RP001 — Case 001: Núñez de Balboa Photovoltaic Plant

- **Document ID:** HERMES-RP001-CASE-001
- **Version:** 0.1.0
- **Status:** Candidate — pending Criterion 4 visual/GIS verification
- **Owner:** Filippo Cobelli
- **Reviewers:** Claude (AI-assisted, Scientific Method Reviewer role — Sonnet 5)
- **Last Updated:** 2026-07-10
- **Related Research Questions:** RP001
- **Related ADR:** ADR-001, ADR-002, ADR-003
- **License:** TBD

---

## Site Identification

- **Name:** Núñez de Balboa Photovoltaic Plant
- **Operator/Owner:** Iberdrola Renovables Energía (100%)
- **Location:** Municipalities of Usagre, Hinojosa del Valle and Bienvenida, Province of
  Badajoz, Extremadura, Spain
- **Coordinates (centroid, WGS84):** 38.4533, -6.2260 (source: Global Energy Monitor,
  citing Iberdrola / Google Maps)
- **Capacity:** 500 MWp / 391 MWac
- **Area:** ~943–1,000 ha (sources vary; pv-maps.com reports 943 ha — 809 ha in Usagre,
  134 ha in Hinojosa del Valle)
- **Commissioning date:** First power to grid April 2020; full construction completed
  within one year, commissioned 2020
- **Panels:** 1,430,000 PV panels on 288,000 ground mounts

## Acquisition Bounding Box (for Layer 1 `AcquisitionRequest`)

Padded box centered on the plant centroid, sized to comfortably include the full ~1,000 ha
footprint plus a margin for the Section 1 Criterion 4 buffer check and for future control-area
search:

```
bbox = (-6.2657, 38.4227, -6.1857, 38.4827)  # (min_lon, min_lat, max_lon, max_lat)
```

Approx. 7.0 km (E-W) × 6.7 km (N-S) centered on 38.4527, -6.2257.

## Case Selection Criteria Check (HYPOTHESES.md Section 1)

| Criterion | Status | Notes |
|---|---|---|
| 1. Size ≥ 25 ha / ≥ 30 valid interior Landsat pixels | ✅ Pass | ~943–1,000 ha, vastly exceeds threshold |
| 2. Age ≥ 2 years, unchanged footprint | ✅ Pass | Commissioned 2020; 6 years stable as of 2026; no reported footprint expansion |
| 3. Documented transformation date, independently verifiable | ✅ Pass | Multiple independent sources (Iberdrola official, Global Energy Monitor, Copernicus/Sentinel-2 imagery published 2020) |
| 4. No concurrent confounding transformation within 2 km buffer | ⚠️ **Pending** | Other Iberdrola regional pipeline projects (Francisco Pizarro, Ceclavín, Arenales, Campo Arañuelo, Majada Alata, San Antonio) are confirmed in different provinces (Cáceres/Alcántara/Cedillo), not within 2 km. However, one secondary source describes the access road area as having "many photovoltaic installations" — this requires direct visual/GIS confirmation via Layer 1 imagery before the case is locked. |

## Outstanding Verification (blocking full "Approved" status)

1. Pull a true-color (or false-color) composite over the bbox above using Layer 1
   (Planetary Computer STAC, Landsat or Sentinel-2) and visually confirm no other
   large-scale anthropogenic transformation exists within 2 km of the plant footprint.
2. Confirm exact footprint polygon (not just bbox) — needed later for the pixel interior
   buffer rule in HYPOTHESES.md Section 4.1. Candidate source: OpenStreetMap /
   OpenInfraMap polygon for "Planta Solar Núñez de Balboa".
3. Determine pre-transformation land cover class (needed for control area matching,
   Section 2) — likely dry cereal cropland / dehesa-type pastureland typical of Tierra de
   Barros, to be confirmed via pre-2019 archival imagery.

## Related Documents

- `research_programs/RP001-surface-transformation-energy-balance/HYPOTHESES.md`
- `governance/adr/ADR-003-acquisition-backend.md`

## Change Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-10 | Initial case candidate identified; Criteria 1-3 pass, Criterion 4 pending visual verification |
