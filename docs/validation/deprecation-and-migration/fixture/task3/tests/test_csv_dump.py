import unittest

from tools.csv_dump import dump


class DumpTest(unittest.TestCase):
    def test_sorted_csv(self):
        items = [{"sku": "B2", "name": "Gelas", "qty": 4}, {"sku": "A1", "name": "Sedotan", "qty": 9}]
        self.assertEqual(dump(items), "sku,name,qty\nA1,Sedotan,9\nB2,Gelas,4")


if __name__ == "__main__":
    unittest.main()
