"""Parking fees, in whole rupiah."""
from datetime import datetime
from math import ceil

FIRST_HOUR = 5_000
NEXT_HOUR = 3_500
DAILY_CAP = 40_000
VEHICLES = ("car", "motorbike")


def _started_hours(entry: datetime, exit: datetime) -> int:
    seconds = (exit - entry).total_seconds()
    if seconds < 0:
        raise ValueError("exit is before entry")
    return max(1, ceil(seconds / 3600))


def _hourly(hours: int) -> int:
    if hours == 0:
        return 0
    return FIRST_HOUR + (hours - 1) * NEXT_HOUR


def fee_for_stay(entry: datetime, exit: datetime, vehicle: str = "car") -> int:
    """Fee for one stay, from entry to exit."""
    if vehicle not in VEHICLES:
        raise ValueError(f"unknown vehicle type: {vehicle}")
    days, rest = divmod(_started_hours(entry, exit), 24)
    return days * DAILY_CAP + min(DAILY_CAP, _hourly(rest))
