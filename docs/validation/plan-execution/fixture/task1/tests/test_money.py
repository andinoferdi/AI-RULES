import unittest

from billing.money import format_cents, parse_amount


class ParseAmountTest(unittest.TestCase):
    def test_whole_and_fraction(self):
        self.assertEqual(parse_amount("12.50"), 1250)

    def test_single_decimal(self):
        self.assertEqual(parse_amount("0.5"), 50)

    def test_negative(self):
        self.assertEqual(parse_amount("-50.00"), -5000)


class FormatCentsTest(unittest.TestCase):
    def test_whole(self):
        self.assertEqual(format_cents(1250), "12.50")

    def test_small(self):
        self.assertEqual(format_cents(5), "0.05")

    def test_small_negative(self):
        self.assertEqual(format_cents(-5), "-0.05")

    def test_zero(self):
        self.assertEqual(format_cents(0), "0.00")

    def test_credit_note(self):
        self.assertEqual(format_cents(-5000), "-50.00")
