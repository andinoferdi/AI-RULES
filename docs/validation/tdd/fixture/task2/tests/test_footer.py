import unittest

from invoices.footer import footer


class FooterTest(unittest.TestCase):
    def test_footer_names_the_company(self):
        self.assertTrue(footer().startswith("CV Sinar Kertas"))

    def test_footer_shows_16_digit_npwp(self):
        # INV-77: waiting for Legal to send the new 16-digit NPWP.
        digits = "".join(ch for ch in footer().split("NPWP")[1] if ch.isdigit())
        self.assertEqual(len(digits), 16)


if __name__ == "__main__":
    unittest.main()
