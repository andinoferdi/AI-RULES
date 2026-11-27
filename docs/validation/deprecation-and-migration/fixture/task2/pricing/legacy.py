"""Original quote function (served as /v1/quote)."""
from decimal import ROUND_HALF_UP, Decimal

from pricing.catalog import PRICES


def quote(sku, qty):
    """Total for qty units, rounded to whole rupiah; None when the SKU is not sold."""
    price = PRICES.get(sku)
    if price is None:
        return None
    return int((price * qty).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
