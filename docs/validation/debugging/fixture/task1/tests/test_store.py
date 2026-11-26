import tempfile
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from expenses import store
from expenses.models import Receipt
from expenses.tz import BUSINESS_TZ


def receipt(amount, submitted_at):
    return Receipt("R-9", "Agus Pratama", "Hotel Melati", Decimal(amount), submitted_at, "mobile")


class StoreTest(unittest.TestCase):
    def test_round_trip_keeps_the_instant(self):
        original = receipt("120000", datetime(2026, 3, 31, 23, 10, tzinfo=BUSINESS_TZ))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "store.jsonl"
            store.save(path, {original.receipt_id: original})
            loaded = store.load(path)["R-9"]
        self.assertEqual(loaded.submitted_at, original.submitted_at)
        self.assertEqual(loaded.submitted_at.utcoffset().total_seconds(), 0)

    def test_existing_receipts_are_kept_unless_replaced(self):
        old = receipt("120000", datetime(2026, 3, 1, 1, 0, tzinfo=timezone.utc))
        new = receipt("150000", datetime(2026, 3, 1, 1, 0, tzinfo=timezone.utc))
        merged, counts = store.upsert({"R-9": old}, [new])
        self.assertEqual(merged["R-9"].amount, Decimal("120000"))
        self.assertEqual(counts, {"added": 0, "replaced": 0, "skipped": 1})
        merged, counts = store.upsert({"R-9": old}, [new], replace=True)
        self.assertEqual(merged["R-9"].amount, Decimal("150000"))
        self.assertEqual(counts, {"added": 0, "replaced": 1, "skipped": 0})


if __name__ == "__main__":
    unittest.main()
