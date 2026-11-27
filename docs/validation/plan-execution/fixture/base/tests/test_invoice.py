import unittest

from billing.invoice import Invoice, calcualte_total, load_invoices


class LoadInvoicesTest(unittest.TestCase):
    def test_reads_quoted_names_and_credit_notes(self):
        invoices = load_invoices("data/invoices.csv")
        self.assertEqual(len(invoices), 6)
        self.assertEqual(invoices[0], Invoice("INV-1001", "Acme, Inc.", 125000))
        self.assertEqual(invoices[2].customer, 'Toko "Maju" Jaya')
        self.assertEqual(invoices[4].amount_cents, -5000)

    def test_total(self):
        self.assertEqual(calcualte_total(load_invoices("data/invoices.csv")), 201714)
