import unittest
from datetime import date

from invoicekit.store import load


class StoreTest(unittest.TestCase):
    def test_loads_all_rows(self):
        self.assertEqual(len(load()), 5)

    def test_parses_dates(self):
        self.assertEqual(load()[0].issued, date(2026, 11, 3))

    def test_amounts_are_integers(self):
        self.assertTrue(all(isinstance(i.amount_idr, int) for i in load()))
