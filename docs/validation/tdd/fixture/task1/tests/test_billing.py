import unittest
from datetime import datetime, timedelta

from garage.billing import fee_for_stay

ENTRY = datetime(2026, 11, 2, 8, 0)


class FeeTest(unittest.TestCase):
    def test_first_hour(self):
        self.assertEqual(fee_for_stay(ENTRY, ENTRY + timedelta(minutes=40)), 5_000)

    def test_started_hours_after_the_first(self):
        self.assertEqual(fee_for_stay(ENTRY, ENTRY + timedelta(hours=2, minutes=10)), 12_000)

    def test_daily_cap(self):
        self.assertEqual(fee_for_stay(ENTRY, ENTRY + timedelta(hours=20)), 40_000)

    def test_second_day_starts_a_new_cap(self):
        self.assertEqual(fee_for_stay(ENTRY, ENTRY + timedelta(hours=25)), 45_000)

    def test_exit_before_entry_is_rejected(self):
        with self.assertRaises(ValueError):
            fee_for_stay(ENTRY, ENTRY - timedelta(minutes=1))

    def test_unknown_vehicle_is_rejected(self):
        with self.assertRaises(ValueError):
            fee_for_stay(ENTRY, ENTRY + timedelta(hours=1), "truck")


if __name__ == "__main__":
    unittest.main()
