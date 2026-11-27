import unittest
from datetime import date

from invoicekit.legacy_pdf import title
from invoicekit.models import Invoice


class OldPdfTest(unittest.TestCase):
    def test_title(self):
        invoice = Invoice("INV-1", "X", date(2026, 1, 1), "invoice", 1)
        self.assertEqual(title(invoice), "Invoice INV-1")
