import unittest

from orders.billing import issue_invoices
from orders.seed import seeded_database
from orders.summary import tenant_summary


class SummaryTest(unittest.TestCase):
    def setUp(self):
        self.db = seeded_database()

    def test_rows_and_totals(self):
        rows = tenant_summary(self.db, "acme")
        self.assertEqual(len(rows), 300)
        for row in rows:
            self.assertEqual(row["total_cents"], sum(l["amount_cents"] for l in row["lines"]))
            self.assertTrue(row["customer"].startswith("Acme customer"))

    def test_newest_first(self):
        stamps = [(r["placed_at"], r["order_id"]) for r in tenant_summary(self.db, "acme")]
        self.assertEqual(stamps, sorted(stamps, reverse=True))

    def test_tenants_are_isolated(self):
        acme = {r["order_id"] for r in tenant_summary(self.db, "acme")}
        globex = {r["order_id"] for r in tenant_summary(self.db, "globex")}
        self.assertEqual(len(globex), 40)
        self.assertFalse(acme & globex)

    def test_invoices_see_new_orders(self):
        before = len(issue_invoices(self.db, "globex"))
        self.db.conn.execute("INSERT INTO orders VALUES (9999, 'globex', 41, "
                             "'2026-11-30T09:00:00Z', 'open')")
        self.db.conn.execute("INSERT INTO order_items VALUES (99999, 9999, 1, 1)")
        self.assertEqual(len(issue_invoices(self.db, "globex")), before + 1)


if __name__ == "__main__":
    unittest.main()
