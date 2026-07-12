"""Layer 2 — Season classification for HYPOTHESES.md Section 4.4 stratification.

Summer (JJA) and Winter (DJF) are the two pre-registered confirmatory
seasonal windows (HYPOTHESES.md Section 5.3). Spring/autumn are
"transition" — exploratory only, never confirmatory.
"""

from __future__ import annotations

from datetime import date, datetime

SUMMER_MONTHS = {6, 7, 8}
WINTER_MONTHS = {12, 1, 2}


def classify_season(d: date | datetime) -> str:
    month = d.month
    if month in SUMMER_MONTHS:
        return "summer"
    if month in WINTER_MONTHS:
        return "winter"
    return "transition"
