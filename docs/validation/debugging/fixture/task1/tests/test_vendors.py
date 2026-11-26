import unittest

from expenses.vendors import normalize_vendor


class NormalizeVendorTest(unittest.TestCase):
    def test_collapses_whitespace(self):
        self.assertEqual(normalize_vendor("  warung   sederhana "), "Warung Sederhana")

    def test_keeps_legal_prefix(self):
        self.assertEqual(normalize_vendor("PT SINAR LOGISTIK"), "PT Sinar Logistik")


if __name__ == "__main__":
    unittest.main()
