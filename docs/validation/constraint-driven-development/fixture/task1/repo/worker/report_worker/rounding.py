"""Legacy rounding kept for invoices issued before 2025; see LED-090."""

from decimal import ROUND_HALF_EVEN, Decimal


def round_half_even_cents(value):  # type: ignore[no-untyped-def]
    return int(Decimal(value).quantize(Decimal("1"), rounding=ROUND_HALF_EVEN))  # noqa: E501
