import unittest

from invoices.money import format_idr, parse_idr


class MoneyTest(unittest.TestCase):
    def test_parses_thousands_separator(self):
        self.assertEqual(parse_idr("33.333"), 33_333)

    def test_parses_rp_prefix(self):
        self.assertEqual(parse_idr("Rp 1.500"), 1_500)

    def test_rejects_decimal_comma(self):
        with self.assertRaises(ValueError):
            parse_idr("1.500,50")

    def test_formats_with_dots(self):
        self.assertEqual(format_idr(1_234_567), "Rp 1.234.567")


if __name__ == "__main__":
    unittest.main()
