import unittest

from koperasi.money import format_rupiah, parse_rupiah


class FormatRupiahTest(unittest.TestCase):
    def test_groups_thousands_with_dots(self):
        self.assertEqual(format_rupiah(1250000), "Rp 1.250.000")

    def test_zero(self):
        self.assertEqual(format_rupiah(0), "Rp 0")

    def test_rejects_negative(self):
        with self.assertRaises(ValueError):
            format_rupiah(-1)


class ParseRupiahTest(unittest.TestCase):
    def test_accepts_plain_and_formatted(self):
        self.assertEqual(parse_rupiah("150000"), 150000)
        self.assertEqual(parse_rupiah("Rp 150.000"), 150000)

    def test_rejects_text(self):
        with self.assertRaises(ValueError):
            parse_rupiah("seratus")
