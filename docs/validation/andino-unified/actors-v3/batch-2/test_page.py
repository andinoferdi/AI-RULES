import os
import runpy
import unittest

page = runpy.run_path(os.environ.get('PAGE_SUBJECT', 'subject.py'))['page']


class PaginationContract(unittest.TestCase):
    def test_consecutive_zero_based_pages(self):
        items = ['A', 'B', 'C', 'D']
        self.assertEqual(page(items, 0, 2), ['A', 'B'])
        self.assertEqual(page(items, 1, 2), ['C', 'D'])
        self.assertEqual(page(items, 2, 2), [])


if __name__ == '__main__':
    unittest.main()
