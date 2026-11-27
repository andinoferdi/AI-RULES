import unittest

from ledger import cli, config


class PageTest(unittest.TestCase):
    entries = [{"date": "2026-03-01", "memo": f"entry {i}", "amount": i} for i in range(250)]

    def test_default_size(self):
        self.assertEqual(len(cli.page(self.entries, 1)), config.DEFAULT_PAGE_SIZE)

    def test_size_is_capped(self):
        self.assertEqual(len(cli.page(self.entries, 1, 500)), config.MAX_PAGE_SIZE)

    def test_default_is_twenty(self):
        self.assertEqual(config.DEFAULT_PAGE_SIZE, 20)
