"""
Case 001 — Mandatory sanity check on pilot extraction output.

Checks performed:
  1. Physical plausibility ranges (LST, NDVI, albedo).
  2. Pixel-count floor from HYPOTHESES.md Section 4.1 (>= 30 valid interior
     pixels) — NOTE: the extraction script (run_case001_pilot_extraction.py)
     only required n_valid_pixels > 0, not >= 30. This script flags any row
     that would fail the pre-registered floor, since those rows should not
     be used for confirmatory-style analysis.
  3. Pixel-count consistency across dates per site (large drops suggest
     partial cloud contamination not fully caught by QA masking).
  4. Descriptive statistics (mean/median/SD) per site per season.
  5. Treatment-control differences per season, compared in direction (not
     magnitude — Case 001 alone is a pilot, HYPOTHESES.md Section 5.6) to
     the literature prior (Hurduc et al.: summer cooling, winter warming).

Usage:
    python examples/check_case001_pilot_sanity.py
"""

from __future__ import annotations

import csv
import statistics
from collections import defaultdict
from pathlib import Path

CSV_PATH = Path("data/case_001_pilot_extraction.csv")

# HYPOTHESES.md Section 4.1
MIN_VALID_PIXELS = 30

# Physical plausibility ranges (generous — flag, don't silently drop)
LST_RANGE_C = (-10.0, 70.0)
NDVI_RANGE = (-1.0, 1.0)
ALBEDO_RANGE = (0.0, 1.0)


def load_rows() -> list[dict]:
    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    for r in rows:
        r["n_valid_pixels"] = int(r["n_valid_pixels"])
        r["lst_c_median"] = float(r["lst_c_median"])
        r["ndvi_median"] = float(r["ndvi_median"])
        r["albedo_median"] = float(r["albedo_median"])
    return rows


def check_plausibility(rows: list[dict]) -> list[str]:
    issues = []
    for r in rows:
        if not (LST_RANGE_C[0] <= r["lst_c_median"] <= LST_RANGE_C[1]):
            issues.append(f"  LST out of range: {r['site_id']} {r['date']} = {r['lst_c_median']:.2f}C")
        if not (NDVI_RANGE[0] <= r["ndvi_median"] <= NDVI_RANGE[1]):
            issues.append(f"  NDVI out of range: {r['site_id']} {r['date']} = {r['ndvi_median']:.3f}")
        if not (ALBEDO_RANGE[0] <= r["albedo_median"] <= ALBEDO_RANGE[1]):
            issues.append(f"  Albedo out of range: {r['site_id']} {r['date']} = {r['albedo_median']:.3f}")
    return issues


def check_pixel_floor(rows: list[dict]) -> list[dict]:
    return [r for r in rows if r["n_valid_pixels"] < MIN_VALID_PIXELS]


def check_pixel_consistency(rows: list[dict]) -> None:
    by_site = defaultdict(list)
    for r in rows:
        by_site[r["site_id"]].append(r["n_valid_pixels"])

    print("Pixel count consistency per site (expect low variance — same polygon every date):")
    for site_id, counts in by_site.items():
        mean_n = statistics.mean(counts)
        min_n, max_n = min(counts), max(counts)
        pct_drop = (1 - min_n / mean_n) * 100 if mean_n > 0 else 0
        flag = " <-- check" if pct_drop > 30 else ""
        print(f"  {site_id:20s} | mean={mean_n:.0f} min={min_n} max={max_n} "
              f"(max drop {pct_drop:.0f}%){flag}")


def descriptive_stats(rows: list[dict]) -> None:
    groups = defaultdict(list)
    for r in rows:
        groups[(r["site_id"], r["season"])].append(r)

    print("\nDescriptive statistics per site / season:")
    print(f"{'Site':20s} | {'Season':10s} | {'N':>4} | {'LST mean':>9} | {'LST SD':>7} | "
          f"{'NDVI mean':>9} | {'Albedo mean':>11}")
    print("-" * 90)
    for (site_id, season), items in sorted(groups.items()):
        lst_vals = [r["lst_c_median"] for r in items]
        ndvi_vals = [r["ndvi_median"] for r in items]
        albedo_vals = [r["albedo_median"] for r in items]
        lst_mean = statistics.mean(lst_vals)
        lst_sd = statistics.stdev(lst_vals) if len(lst_vals) > 1 else 0.0
        print(f"{site_id:20s} | {season:10s} | {len(items):>4} | {lst_mean:>8.2f}C | "
              f"{lst_sd:>6.2f}C | {statistics.mean(ndvi_vals):>9.3f} | "
              f"{statistics.mean(albedo_vals):>11.3f}")


def treatment_control_comparison(rows: list[dict]) -> None:
    groups = defaultdict(list)
    for r in rows:
        groups[(r["site_id"], r["season"])].append(r["lst_c_median"])

    print("\nTreatment vs Control LST difference per season (pilot only — NOT confirmatory, "
          "see HYPOTHESES.md Section 5.6):")
    for season in ("summer", "winter"):
        treatment_vals = groups.get(("treatment", season), [])
        if not treatment_vals:
            continue
        treatment_mean = statistics.mean(treatment_vals)
        for control_id in ("control_1_C5", "control_2_C1"):
            control_vals = groups.get((control_id, season), [])
            if not control_vals:
                continue
            control_mean = statistics.mean(control_vals)
            diff = treatment_mean - control_mean
            print(f"  {season:8s} | treatment - {control_id}: {diff:+.2f} C "
                  f"(treatment={treatment_mean:.2f}C, control={control_mean:.2f}C)")

    print(
        "\n  Literature prior (Hurduc et al. 2024, same climate zone): summer cooling, "
        "winter warming expected. Directional consistency here is informative for pilot "
        "validation only — magnitude/significance require the full multi-site sample "
        "(HYPOTHESES.md Section 5.5-5.6)."
    )


def main() -> None:
    rows = load_rows()
    print(f"Loaded {len(rows)} rows from {CSV_PATH}\n")

    print("=" * 90)
    print("1. Physical plausibility check")
    print("=" * 90)
    issues = check_plausibility(rows)
    if issues:
        print(f"FOUND {len(issues)} implausible value(s):")
        for issue in issues:
            print(issue)
    else:
        print("OK — all LST/NDVI/albedo values within plausible physical ranges.")

    print("\n" + "=" * 90)
    print(f"2. Pixel-count floor check (HYPOTHESES.md Section 4.1: >= {MIN_VALID_PIXELS})")
    print("=" * 90)
    below_floor = check_pixel_floor(rows)
    if below_floor:
        print(f"WARNING: {len(below_floor)} row(s) below the {MIN_VALID_PIXELS}-pixel floor "
              f"(extraction script did not enforce this — filter these out before analysis):")
        for r in below_floor:
            print(f"  {r['site_id']} {r['date']}: n={r['n_valid_pixels']}")
    else:
        print(f"OK — all {len(rows)} rows meet the {MIN_VALID_PIXELS}-pixel minimum.")

    print("\n" + "=" * 90)
    print("3. Pixel-count consistency")
    print("=" * 90)
    check_pixel_consistency(rows)

    print("\n" + "=" * 90)
    print("4. Descriptive statistics")
    print("=" * 90)
    descriptive_stats(rows)

    print("\n" + "=" * 90)
    print("5. Treatment-control comparison (pilot, directional only)")
    print("=" * 90)
    treatment_control_comparison(rows)


if __name__ == "__main__":
    main()
