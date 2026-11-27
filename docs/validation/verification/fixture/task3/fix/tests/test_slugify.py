import unittest

from slugkit import slugify


class SlugifyTest(unittest.TestCase):
    def test_spaces(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_punctuation_collapses(self):
        self.assertEqual(slugify("Q&A -- part 2!"), "q-a-part-2")

    def test_trims_hyphens(self):
        self.assertEqual(slugify("  -Intro-  "), "intro")

    def test_issue_42(self):
        # Issue #42: "Ça va" lost its first letter.
        self.assertEqual(slugify("Ca va"), "ca-va")


if __name__ == "__main__":
    unittest.main()
