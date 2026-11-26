import unittest
from decimal import Decimal

from orders.errors import PricingError
from orders.pricing import price_order


def line(sku, qty, unit_price):
    return {"sku": sku, "qty": qty, "unit_price": unit_price}


class PriceOrderTest(unittest.TestCase):
    def test_small_order_pays_shipping_and_tax(self):
        audit = []
        total = price_order({"lines": [line("A", 2, "10.00")]}, {"region": "north"}, audit)
        # 20.00 + 4.99 shipping = 24.99; 8% tax = 1.9992; 26.9892 rounds to 26.99
        self.assertEqual(total, Decimal("26.99"))
        self.assertEqual([name for name, _ in audit], ["subtotal", "discount", "tax", "total"])

    def test_loyal_customer_gets_ten_percent_off(self):
        total = price_order(
            {"lines": [line("A", 1, "100.00")]}, {"region": "WEST", "loyalty_years": 6}, []
        )
        # 100.00 - 10.00 discount, free shipping; 5% tax = 4.50
        self.assertEqual(total, Decimal("94.50"))

    def test_negative_quantity_is_rejected(self):
        with self.assertRaises(PricingError) as caught:
            price_order({"lines": [line("B", -1, "5.00")]}, {"region": "EAST"}, [])
        self.assertEqual(str(caught.exception), "line B has a negative quantity")

    def test_empty_order_is_rejected(self):
        with self.assertRaises(PricingError):
            price_order({"lines": []}, {"region": "EAST"}, [])

    def test_export_prices_without_tax(self):
        total = price_order({"lines": [line("C", 1, "60.00")]}, {"region": "SOUTH"}, [], False)
        self.assertEqual(total, Decimal("60.00"))


if __name__ == "__main__":
    unittest.main()
