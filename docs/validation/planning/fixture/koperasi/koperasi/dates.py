from datetime import date


def days_between(start: date, end: date) -> int:
    """Number of days between two dates, in either order."""
    return abs((end - start).days)


def parse_iso_date(text: str) -> date:
    """Parse YYYY-MM-DD. Raises ValueError otherwise."""
    return date.fromisoformat(text)
