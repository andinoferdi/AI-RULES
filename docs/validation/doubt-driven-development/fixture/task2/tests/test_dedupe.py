import unittest

from events.dedupe import dedupe_events


class DedupeTest(unittest.TestCase):
    def test_removes_adjacent_duplicate(self):
        events = [{"id": "EV-1", "n": 1}, {"id": "EV-1", "n": 2}]
        self.assertEqual(len(dedupe_events(events)), 1)


if __name__ == "__main__":
    unittest.main()
