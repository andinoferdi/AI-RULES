import unittest

from retrykit.client import call_with_retry


class ClientTest(unittest.TestCase):
    def test_retries_then_succeeds(self):
        calls, sleeps = [], []

        def flaky():
            calls.append(1)
            if len(calls) < 3:
                raise ConnectionError
            return "ok"

        self.assertEqual(call_with_retry(flaky, sleep=sleeps.append), "ok")
        self.assertEqual(len(sleeps), 2)

    def test_raises_after_max(self):
        sleeps = []

        def down():
            raise ConnectionError

        with self.assertRaises(ConnectionError):
            call_with_retry(down, attempts=4, sleep=sleeps.append)
        self.assertEqual(len(sleeps), 3)
