import unittest

from web.routes import handle


class RoutesTest(unittest.TestCase):
    def test_v1_quote(self):
        self.assertEqual(handle("/v1/quote", {"sku": "KOPI-250", "qty": "2"}),
                         (200, {"sku": "KOPI-250", "qty": 2, "total": 97000}))

    def test_v2_quote(self):
        self.assertEqual(handle("/v2/quote", {"sku": "GULA-500", "qty": "1"}),
                         (200, {"sku": "GULA-500", "qty": 1, "total": "12500.50",
                                "currency": "IDR"}))

    def test_v2_unknown(self):
        self.assertEqual(handle("/v2/quote", {"sku": "TEH-100", "qty": "1"})[0], 404)


if __name__ == "__main__":
    unittest.main()
