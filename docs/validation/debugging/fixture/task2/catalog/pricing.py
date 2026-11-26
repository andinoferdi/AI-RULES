"""Storefront prices. Partner prices get a markup, rounded to whole rupiah."""
from dataclasses import replace
from decimal import ROUND_HALF_UP, Decimal


def apply_markup(products, rate: Decimal):
    priced = []
    for product in products:
        if product.source == "partner":
            price = (product.price * (1 + rate)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
            product = replace(product, price=price)
        priced.append(product)
    return priced
