import unittest
from datetime import datetime, timezone
from decimal import Decimal

from expenses.models import Receipt
from expenses.report import format_rupiah, monthly_report


def receipt(receipt_id, amount, submitted_at):
    return Receipt(receipt_id, "Sari Wulandari", "Hotel Melati", Decimal(amount), submitted_at, "mobile")


class MonthlyReportTest(unittest.TestCase):
    def test_groups_by_office_month(self):
        late_march = receipt("A", "100000", datetime(2026, 3, 31, 16, 30, tzinfo=timezone.utc))  # 23:30 WIB
        first_april = receipt("B", "50000", datetime(2026, 3, 31, 17, 30, tzinfo=timezone.utc))  # 00:30 WIB
        report = monthly_report([late_march, first_april], "2026-03")
        self.assertEqual(report["receipt_ids"], ["A"])
        self.assertEqual(report["total"], Decimal("100000"))

    def test_format_rupiah(self):
        self.assertEqual(format_rupiah(Decimal("48215000")), "Rp 48.215.000")


if __name__ == "__main__":
    unittest.main()
