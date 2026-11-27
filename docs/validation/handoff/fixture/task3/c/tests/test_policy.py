import unittest

from retrykit.policy import compute_delay


class PolicyTest(unittest.TestCase):
    def test_grows_exponentially(self):
        self.assertEqual(compute_delay(0), 0.5)
        self.assertEqual(compute_delay(2), 2.0)

    def test_caps(self):
        self.assertEqual(compute_delay(10), 8.0)
