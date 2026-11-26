import unittest

from helpers import remove, run_cli, write_data


class ListCommandTest(unittest.TestCase):
    def test_lists_each_loan(self):
        path = write_data([{
            "loan_id": "L-1", "member_id": "A-1", "member_name": "Ani", "principal": 500000,
            "installments": [{"number": 1, "due_date": "2026-01-05", "amount": 250000}],
        }])
        self.addCleanup(remove, path)
        code, out, err = run_cli(["list", "--data", path])
        self.assertEqual(code, 0)
        self.assertIn("L-1  Ani  Rp 500.000  1 cicilan", out)
        self.assertEqual(err, "")

    def test_missing_data_file(self):
        code, out, err = run_cli(["list", "--data", "missing.json"])
        self.assertEqual(code, 1)
        self.assertEqual(err.strip(), "File data tidak ditemukan: missing.json")
