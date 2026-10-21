# fleet_utils.py
# Utility helpers for KM-Waechter.
# Written in 2013. Modernized 2025: dead code removed, conversion constant corrected.

KM_PER_MILE: float = 1.60934        # 1 mile = 1.60934 km  →  1 km = 1/1.60934 miles


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles. Used by the nightly UK partner report."""
    return km / KM_PER_MILE


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a number as a whole-number percentage string."""
    return f"{int(value)}%"


def mean(values: list) -> float:
    """Return the arithmetic mean of a list of numbers. Returns 0 if the list is empty."""
    if not values:
        return 0.0
    return sum(values) / len(values)
