import io
import unittest

from billing.cli import main


class TotalCommandTest(unittest.TestCase):
    def test_total_of_sample_data(self):
        out = io.StringIO()
        self.assertEqual(main(["total", "--data", "data/invoices.csv"], out=out), 0)
        self.assertEqual(out.getvalue(), "201714\n")
