"""Timestamp parsing for the two receipt sources."""
import re
from datetime import datetime, timezone

from .tz import BUSINESS_TZ

_APP_TIMESTAMP = re.compile(
    r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.\d+)?(Z|[+-]\d{2}:\d{2})?$"
)


def parse_local_timestamp(value: str) -> datetime:
    """CSV uploads carry office wall-clock time without an offset, e.g. '2026-03-31 21:15'."""
    naive = datetime.strptime(value.strip(), "%Y-%m-%d %H:%M")
    return naive.replace(tzinfo=BUSINESS_TZ)


def parse_app_timestamp(value: str) -> datetime:
    """Mobile app timestamps are ISO 8601 in UTC, e.g. '2026-03-31T14:15:00Z'.

    Receipts are stored to the second, so fractional seconds are dropped.
    """
    match = _APP_TIMESTAMP.match(value.strip())
    if not match:
        raise ValueError(f"unrecognised app timestamp: {value!r}")
    wall_clock = datetime.strptime(match.group(1), "%Y-%m-%dT%H:%M:%S")
    return wall_clock.replace(tzinfo=timezone.utc)
