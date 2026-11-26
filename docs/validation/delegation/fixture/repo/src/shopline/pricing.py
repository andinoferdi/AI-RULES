from decimal import Decimal

from shopline.money import format_price

BULK_THRESHOLD = 10
BULK_RATE = Decimal("0.15")


def bulk_price(unit_price: Decimal, quantity: int) -> Decimal:
    total = unit_price * quantity
    if quantity >= BULK_THRESHOLD:
        total = total * (1 - BULK_RATE)
    return total


def bulk_price_label(unit_price: Decimal, quantity: int) -> str:
    return format_price(bulk_price(unit_price, quantity))
