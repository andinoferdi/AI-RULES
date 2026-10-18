import unittest
from subject import page


class PaginationBoundaries(unittest.TestCase):
    def test_size_one_advances(self):
        items = ['A', 'B', 'C']
        self.assertEqual([page(items, index, 1) for index in range(3)],
                         [['A'], ['B'], ['C']])

    def test_partial_and_empty_pages(self):
        items = ['A', 'B', 'C', 'D', 'E']
        self.assertEqual([page(items, index, 2) for index in range(4)],
                         [['A', 'B'], ['C', 'D'], ['E'], []])
        self.assertEqual(items, ['A', 'B', 'C', 'D', 'E'])

    def test_size_three_pages_are_consecutive(self):
        items = ['A', 'B', 'C', 'D']
        self.assertEqual(page(items, 0, 3), ['A', 'B', 'C'])
        self.assertEqual(page(items, 1, 3), ['D'])

    def test_empty_collection(self):
        self.assertEqual(page([], 0, 2), [])


if __name__ == '__main__':
    unittest.main()
