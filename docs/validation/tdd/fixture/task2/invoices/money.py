"""Rupiah amounts are whole numbers; the CSV files use a dot as thousands separator."""


def parse_idr(text: str) -> int:
    cleaned = text.strip().replace("Rp", "").replace(".", "").strip()
    if not cleaned.isdigit():
        raise ValueError(f"not a rupiah amount: {text!r}")
    return int(cleaned)


def format_idr(amount: int) -> str:
    return "Rp " + f"{amount:,}".replace(",", ".")
