import unittest
from datetime import datetime, timezone

from expenses.timeparse import parse_app_timestamp, parse_local_timestamp
from expenses.tz import BUSINESS_TZ


class LocalTimestampTest(unittest.TestCase):
    def test_csv_time_is_office_time(self):
        self.assertEqual(parse_local_timestamp("2026-03-31 22:40"),
                         datetime(2026, 3, 31, 22, 40, tzinfo=BUSINESS_TZ))


class AppTimestampTest(unittest.TestCase):
    def test_utc_timestamp(self):
        self.assertEqual(parse_app_timestamp("2026-03-31T15:20:00Z"),
                         datetime(2026, 3, 31, 15, 20, tzinfo=timezone.utc))

    def test_drops_fractional_seconds(self):
        """Receipts are stored to the second."""
        self.assertEqual(parse_app_timestamp("2026-03-02T01:02:03.250Z"),
                         datetime(2026, 3, 2, 1, 2, 3, tzinfo=timezone.utc))

    def test_rejects_other_formats(self):
        with self.assertRaises(ValueError):
            parse_app_timestamp("31/03/2026 22:00")


if __name__ == "__main__":
    unittest.main()
