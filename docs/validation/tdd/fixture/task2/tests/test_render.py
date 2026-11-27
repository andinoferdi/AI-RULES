import unittest

from invoices.render import load, render


class RenderTest(unittest.TestCase):
    def test_invoice_0398_totals(self):
        invoice = load("INV-2026-0398")
        self.assertEqual(invoice.subtotal, 510_000)
        self.assertEqual(invoice.tax, 56_100)
        self.assertEqual(invoice.total, 566_100)

    def test_rendered_invoice_lists_items_and_total(self):
        text = render(load("INV-2026-0398"))
        self.assertIn("Kertas HVS F4", text)
        self.assertIn("Rp 566.100", text)


if __name__ == "__main__":
    unittest.main()
