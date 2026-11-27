import unittest

from retrykit.config import MAX_ATTEMPTS


class ConfigTest(unittest.TestCase):
    def test_default_max_attempts(self):
        self.assertEqual(MAX_ATTEMPTS, 5)
