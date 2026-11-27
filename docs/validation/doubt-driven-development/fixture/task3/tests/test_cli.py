import unittest

from notify.cli import build_parser


class CliTest(unittest.TestCase):
    def test_test_alert_flag(self):
        args = build_parser().parse_args(["--test-alert", "--channel", "sms"])
        self.assertTrue(args.test_alert)
        self.assertEqual(args.channel, "sms")


if __name__ == "__main__":
    unittest.main()
