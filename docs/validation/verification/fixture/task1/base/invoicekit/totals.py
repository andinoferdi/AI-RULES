from decimal import ROUND_HALF_UP, Decimal


def subtotal(lines):
    """Sum of quantity * unit price for (quantity, unit_price) pairs."""
    return sum((Decimal(str(qty)) * Decimal(str(price)) for qty, price in lines), Decimal("0"))


def money(value):
    """Round to cents, half up."""
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
