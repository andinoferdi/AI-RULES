import unittest

from blog.slug import slugify


class SlugTest(unittest.TestCase):
    def test_existing_slugs_stay_stable(self):
        cases = {
            "Café Résumé: 5 Ways We Cut Planning Time — and What Didn't Work":
                "cafe-resume-5-ways-we-cut-planning-time-and-what-didnt-work",
            "Hello,   World!": "hello-world",
            "  --Already-Slugged--  ": "already-slugged",
            "snake_case_title": "snakecasetitle",
            "日本語だけ": "post",
        }
        for title, slug in cases.items():
            self.assertEqual(slugify(title), slug)

    def test_long_titles_cut_at_a_word(self):
        slug = slugify("word " * 40)
        self.assertLessEqual(len(slug), 80)
        self.assertFalse(slug.endswith("-"))
        self.assertTrue(slug.endswith("word"))


if __name__ == "__main__":
    unittest.main()
