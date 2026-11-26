import unittest

from notes.export import to_markdown


class ToMarkdownTest(unittest.TestCase):
    def test_oldest_first(self):
        notes = [
            {"title": "Second", "body": "b", "created": "2026-11-02"},
            {"title": "First", "body": " a \n", "created": "2026-11-01"},
        ]
        self.assertEqual(to_markdown(notes), "## First\n\na\n\n## Second\n\nb\n")


if __name__ == "__main__":
    unittest.main()
