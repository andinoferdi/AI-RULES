import os
import unittest
from pathlib import Path


module_path = Path(os.environ.get('PAGE_SUBJECT', str(Path(__file__).with_name('subject.py'))))
scope = {}
exec(compile(module_path.read_bytes(), str(module_path), 'exec'), scope)
page = scope['page']


class PaginationContract(unittest.TestCase):
    def test_reported_consecutive_pages(self):
        values = ['A', 'B', 'C', 'D']
        self.assertEqual(page(values, 0, 2), ['A', 'B'])
        self.assertEqual(page(values, 1, 2), ['C', 'D'])

    def test_size_one_progresses(self):
        self.assertEqual(page(['A', 'B', 'C'], 0, 1), ['A'])
        self.assertEqual(page(['A', 'B', 'C'], 1, 1), ['B'])
        self.assertEqual(page(['A', 'B', 'C'], 2, 1), ['C'])

    def test_partial_final_and_exhausted_pages(self):
        self.assertEqual(page(['A', 'B', 'C', 'D', 'E'], 1, 3), ['D', 'E'])
        self.assertEqual(page(['A', 'B', 'C', 'D', 'E'], 2, 3), [])
        self.assertEqual(page([], 0, 2), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
