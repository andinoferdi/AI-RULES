import unittest

from render import log
from render.templates import render

CONTEXT = {"name": "Ayu", "item": 7, "amount": "120.00"}


class RenderTest(unittest.TestCase):
    def test_locale_strings(self):
        self.assertTrue(render("welcome", "id", CONTEXT, "r1").startswith("Halo Ayu,"))
        self.assertTrue(render("welcome", "nl", CONTEXT, "r2").startswith("Hallo Ayu,"))
        self.assertTrue(render("welcome", "en", CONTEXT, "r3").startswith("Hello Ayu,"))

    def test_same_output_for_every_request(self):
        first = render("invoice", "en", CONTEXT, "r4")
        self.assertEqual(first, render("invoice", "en", CONTEXT, "r5"))
        self.assertIn("Amount 120.00", first)
        self.assertIn("https://lumen.example/invoice", first)

    def test_render_is_logged_with_request_id(self):
        render("digest", "id", CONTEXT, "trace-42")
        self.assertIn('"request_id": "trace-42"', log.RECENT[-1])


if __name__ == "__main__":
    unittest.main()
