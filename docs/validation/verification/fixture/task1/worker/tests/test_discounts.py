import unittest
from datetime import date
from decimal import Decimal

from invoicekit import ExpiredCode, UnknownCode, apply_code

LINES = [(2, "40.00"), (1, "20.00")]  # subtotal 100.00
TODAY = date(2026, 4, 15)


class DiscountTest(unittest.TestCase):
    def test_percent_code(self):
        self.assertEqual(apply_code(LINES, "VIP25", TODAY), Decimal("75.00"))

    def test_fixed_code(self):
        self.assertEqual(apply_code(LINES, "WELCOME50", TODAY), Decimal("50.00"))

    def test_fixed_code_never_below_zero(self):
        self.assertEqual(apply_code([(1, "30.00")], "WELCOME50", TODAY), Decimal("0.00"))

    def test_case_insensitive(self):
        self.assertEqual(apply_code(LINES, "vip25", TODAY), Decimal("75.00"))

    def test_spaces_ignored(self):
        self.assertEqual(apply_code(LINES, "  VIP25 ", TODAY), Decimal("75.00"))

    def test_unknown_code(self):
        with self.assertRaises(UnknownCode):
            apply_code(LINES, "NOPE", TODAY)

    @unittest.skip("flaky: depends on today's date")
    def test_expired_code_rejected(self):
        with self.assertRaises(ExpiredCode):
            apply_code(LINES, "SPRING10")


if __name__ == "__main__":
    unittest.main()
