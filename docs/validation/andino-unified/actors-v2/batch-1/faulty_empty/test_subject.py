import unittest

from subject import sum_invoice


class InvoiceContract(unittest.TestCase):
    def test_integer_invoice(self):
        self.assertEqual(sum_invoice([10, 5]), 15)

    def test_empty_invoice(self):
        self.assertEqual(sum_invoice([]), 0)


if __name__ == "__main__":
    unittest.main()
