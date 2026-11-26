import unittest
from decimal import Decimal

from catalog.feed import Product
from catalog.merge import merge_feeds


def product(sku, variant="M", source="primary"):
    return Product(sku, f"Item {sku}", variant, Decimal("1000"), source)


class MergeFeedsTest(unittest.TestCase):
    def test_primary_wins_case_insensitively(self):
        kept = merge_feeds([product("AND-1")],
                           [product("and-1", source="partner"), product("PTR-2", source="partner")])
        self.assertEqual([(item.sku, item.source) for item in kept],
                         [("AND-1", "primary"), ("PTR-2", "partner")])

    def test_variants_are_separate_products(self):
        kept = merge_feeds([product("AND-1", "S"), product("AND-1", "M")], [])
        self.assertEqual([item.variant for item in kept], ["S", "M"])

    def test_order_is_preserved(self):
        kept = merge_feeds([product("B"), product("A")], [product("C", source="partner")])
        self.assertEqual([item.sku for item in kept], ["B", "A", "C"])


if __name__ == "__main__":
    unittest.main()
