import unittest
from decimal import Decimal

from catalog.feed import Product
from catalog.pricing import apply_markup


class MarkupTest(unittest.TestCase):
    def test_partner_price_is_marked_up_and_rounded(self):
        [priced] = apply_markup([Product("PTR-1", "Tas", "M", Decimal("45555"), "partner")],
                                Decimal("0.12"))
        self.assertEqual(priced.price, Decimal("51022"))

    def test_primary_price_is_unchanged(self):
        [priced] = apply_markup([Product("AND-1", "Tas", "M", Decimal("45555"), "primary")],
                                Decimal("0.12"))
        self.assertEqual(priced.price, Decimal("45555"))


if __name__ == "__main__":
    unittest.main()
