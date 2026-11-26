from decimal import ROUND_DOWN, Decimal

CENT = Decimal("0.01")


def to_amount(value) -> Decimal:
    return Decimal(str(value))


def format_price(amount: Decimal, currency: str = "USD") -> str:
    """Format an amount for people: two decimals, thousands separators."""
    shown = amount.quantize(CENT, rounding=ROUND_DOWN)
    return f"{shown:,.2f}"
