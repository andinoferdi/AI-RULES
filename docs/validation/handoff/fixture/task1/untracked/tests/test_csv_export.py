import io
import unittest

from invoicekit.csv_export import write_csv
from invoicekit.store import load


def export():
    fh = io.StringIO()
    write_csv(load(), fh)
    return fh.getvalue().splitlines()


class CsvExportTest(unittest.TestCase):
    def test_header_order_matches_spec(self):
        self.assertEqual(export()[0], "number;issued;customer;kind;amount_idr")

    def test_uses_semicolons(self):
        self.assertIn("INV-2611-001;", export()[1])

    def test_amount_is_whole_rupiah(self):
        self.assertTrue(export()[1].endswith(";1250000"))

    def test_quotes_only_when_needed(self):
        rows = export()
        self.assertIn('"CV Maju; Bersama"', rows[2])
        self.assertNotIn('"PT Sinar Jaya"', rows[1])

    def test_iso_dates(self):
        self.assertIn("2026-11-03", export()[1])

    @unittest.skip("waiting for Budi: should credit notes be negative? (spec, Credit notes)")
    def test_credit_note_amount(self):
        pass
