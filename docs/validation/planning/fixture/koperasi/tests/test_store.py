import unittest
from datetime import date

from koperasi.models import Installment, Loan
from koperasi.store import load_loans, save_loans

from helpers import remove, write_data


class StoreTest(unittest.TestCase):
    def test_round_trip(self):
        path = write_data([])
        self.addCleanup(remove, path)
        loans = [Loan("L-9", "A-1", "Ani", 500000,
                      [Installment(1, date(2026, 1, 5), 250000)])]
        save_loans(path, loans)
        self.assertEqual(load_loans(path), loans)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            load_loans("does-not-exist.json")
