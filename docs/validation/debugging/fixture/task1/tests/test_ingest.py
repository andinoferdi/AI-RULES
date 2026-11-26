import tempfile
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from expenses.ingest_csv import read_csv
from expenses.ingest_mobile import parse_payload
from expenses.tz import BUSINESS_TZ


class MobileIngestTest(unittest.TestCase):
    def test_payload_from_app_4(self):
        receipt = parse_payload({
            "receipt_id": "R-1",
            "employee": "Sari Wulandari",
            "vendor": "Taksi Kota",
            "amount": 85000,
            "submitted_at": "2026-03-10T02:15:00Z",
            "app_version": "4.9.3",
        })
        self.assertEqual(receipt.submitted_at, datetime(2026, 3, 10, 2, 15, tzinfo=timezone.utc))
        self.assertEqual(receipt.amount, Decimal("85000"))
        self.assertEqual(receipt.source, "mobile")


class CsvIngestTest(unittest.TestCase):
    def test_reads_office_time(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "upload.csv"
            path.write_text(
                "receipt_id,employee,vendor,amount,submitted_at\n"
                "C-1,Budi Santoso,  warung   sederhana ,45000,2026-03-31 21:15\n",
                encoding="utf-8",
            )
            [receipt] = read_csv(path)
        self.assertEqual(receipt.submitted_at, datetime(2026, 3, 31, 21, 15, tzinfo=BUSINESS_TZ))
        self.assertEqual(receipt.vendor, "Warung Sederhana")


if __name__ == "__main__":
    unittest.main()
