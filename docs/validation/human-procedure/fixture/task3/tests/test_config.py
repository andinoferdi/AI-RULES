import unittest

from app import config


class ProblemsTest(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(config.problems({"LOG_LEVEL": "debug", "PORT": "8081"}), [])

    def test_missing_level(self):
        self.assertEqual(config.problems({"PORT": "8081"}), ["missing LOG_LEVEL"])

    def test_invalid_level(self):
        self.assertEqual(config.problems({"LOG_LEVEL": "loud", "PORT": "1"}),
                         ["invalid LOG_LEVEL"])


if __name__ == "__main__":
    unittest.main()
