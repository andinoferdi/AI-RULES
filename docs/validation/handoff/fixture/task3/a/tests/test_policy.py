import unittest

from retrykit.policy import backoff


class PolicyTest(unittest.TestCase):
    def test_grows_exponentially(self):
        self.assertEqual(backoff(0), 0.5)
        self.assertEqual(backoff(2), 2.0)

    def test_caps(self):
        self.assertEqual(backoff(10), 8.0)
