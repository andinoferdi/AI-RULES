import unittest

from slugkit import slugify


class SlugifyTest(unittest.TestCase):
    def test_spaces(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_punctuation_collapses(self):
        self.assertEqual(slugify("Q&A -- part 2!"), "q-a-part-2")

    def test_trims_hyphens(self):
        self.assertEqual(slugify("  -Intro-  "), "intro")


if __name__ == "__main__":
    unittest.main()
