import re
import tempfile
import unittest
from pathlib import Path

import build


class BuildTests(unittest.TestCase):
    def test_pages_have_footer_and_links_resolve(self):
        with tempfile.TemporaryDirectory() as temp:
            out = build.build(Path(temp))
            pages = list(out.rglob("*.html"))
            self.assertEqual(len(pages), 2)
            for page in pages:
                text = page.read_text(encoding="utf-8")
                self.assertIn("<footer>", text)
                for href in re.findall(r'href="([^"]+)"', text):
                    self.assertTrue((page.parent / href).resolve().exists(), f"{page.name}: {href}")


if __name__ == "__main__":
    unittest.main()
