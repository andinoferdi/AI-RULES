"""Replacement quote function (served as /v2/quote since 2.0)."""
from decimal import ROUND_HALF_EVEN, Decimal

from pricing.catalog import PRICES


class UnknownSku(KeyError):
    pass


def quote_v2(sku, qty):
    """Total for qty units in rupiah with sen (2 places, banker's rounding)."""
    try:
        price = PRICES[sku]
    except KeyError:
        raise UnknownSku(sku) from None
    if qty <= 0:
        raise ValueError("qty must be positive")
    return (price * qty).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
