import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


def parse():
    page = Page()
    page.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    return page


class PageTest(unittest.TestCase):
    def test_hero_image_has_alt_text(self):
        images = [a for t, a in parse().tags if t == "img"]
        self.assertTrue(images[0].get("alt"))

    def test_three_quotes_in_carousel(self):
        self.assertEqual(sum(1 for t, _ in parse().tags if t == "blockquote"), 3)

    def test_signup_link(self):
        links = [a.get("href") for t, a in parse().tags if t == "a"]
        self.assertIn("/signup", links)

    def test_carousel_and_analytics_started(self):
        source = (ROOT / "index.html").read_text(encoding="utf-8")
        source += "".join(p.read_text(encoding="utf-8") for p in (ROOT / "js").glob("*.js"))
        self.assertIn("Carousel.init(", source)
        self.assertIn('Analytics.track("landing_view")', source)


if __name__ == "__main__":
    unittest.main()
