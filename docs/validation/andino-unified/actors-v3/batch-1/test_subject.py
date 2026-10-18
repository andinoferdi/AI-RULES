import unittest
from subject import sum_invoice

class Contract(unittest.TestCase):
    def test_known_invoice(self):
        self.assertEqual(sum_invoice([10, 5]), 15)

    def test_empty_invoice(self):
        self.assertEqual(sum_invoice([]), 0)
