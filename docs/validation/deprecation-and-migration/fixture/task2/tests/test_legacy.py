import unittest

from pricing.legacy import quote


class LegacyQuoteTest(unittest.TestCase):
    def test_whole_rupiah(self):
        self.assertEqual(quote("KOPI-250", 2), 97000)

    def test_rounds_half_up(self):
        self.assertEqual(quote("GULA-500", 1), 12501)

    def test_unknown_sku_is_none(self):
        self.assertIsNone(quote("TEH-100", 3))


if __name__ == "__main__":
    unittest.main()
