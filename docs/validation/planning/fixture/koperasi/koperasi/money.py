"""Rupiah amounts are whole integers everywhere in this project."""


def format_rupiah(amount: int) -> str:
    """Format 1250000 as 'Rp 1.250.000'. Negative amounts are rejected."""
    if amount < 0:
        raise ValueError("negative amount")
    return "Rp " + f"{amount:,}".replace(",", ".")


def parse_rupiah(text: str) -> int:
    """Parse '150000', '150.000' or 'Rp 150.000' into 150000.

    Raises ValueError for anything that is not a non-negative whole amount.
    Zero is accepted.
    """
    cleaned = text.strip()
    if cleaned.lower().startswith("rp"):
        cleaned = cleaned[2:].strip()
    cleaned = cleaned.replace(".", "")
    if not cleaned.isdigit():
        raise ValueError(f"not a rupiah amount: {text!r}")
    return int(cleaned)
