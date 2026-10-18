import unittest
from subject import page


class PaginationContract(unittest.TestCase):
    def test_reported_consecutive_pages(self):
        items = ['A', 'B', 'C', 'D']
        self.assertEqual(page(items, 0, 2), ['A', 'B'])
        self.assertEqual(page(items, 1, 2), ['C', 'D'])


if __name__ == '__main__':
    unittest.main()
