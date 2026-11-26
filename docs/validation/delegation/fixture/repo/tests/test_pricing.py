from decimal import Decimal

from shopline.pricing import bulk_price_label


def test_bulk_discount_rounding():
    # 12 x 1.96 = 23.52, minus 15% = 19.992 -> shown as 19.99
    assert bulk_price_label(Decimal("1.96"), 12) == "19.99"


def test_bulk_discount_half_cent_rounds_up():
    # 10 x 2.33 = 23.30, minus 15% = 19.805 -> shown as 19.81
    assert bulk_price_label(Decimal("2.33"), 10) == "19.81"
