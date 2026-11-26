"""Vendor name clean-up for CSV uploads. Owned by procurement (see README, EXP-88)."""


def normalize_vendor(name: str) -> str:
    """Collapse whitespace and title-case the vendor name."""
    return " ".join(name.split()).title()
