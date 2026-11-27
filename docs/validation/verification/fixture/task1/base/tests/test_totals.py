import unittest
from decimal import Decimal

from invoicekit import money, subtotal


class TotalsTest(unittest.TestCase):
    def test_subtotal(self):
        self.assertEqual(subtotal([(2, "10.00"), (1, "5.50")]), Decimal("25.50"))

    def test_empty_subtotal(self):
        self.assertEqual(subtotal([]), Decimal("0"))

    def test_money_rounds_half_up(self):
        self.assertEqual(money(Decimal("2.005")), Decimal("2.01"))


if __name__ == "__main__":
    unittest.main()
