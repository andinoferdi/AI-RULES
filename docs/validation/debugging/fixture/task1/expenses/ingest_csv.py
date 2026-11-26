"""Import receipts from the finance portal's CSV export."""
import csv
from decimal import Decimal

from .models import Receipt
from .timeparse import parse_local_timestamp
from .vendors import normalize_vendor


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return [
            Receipt(
                receipt_id=row["receipt_id"].strip(),
                employee=row["employee"].strip(),
                vendor=normalize_vendor(row["vendor"]),
                amount=Decimal(row["amount"]),
                submitted_at=parse_local_timestamp(row["submitted_at"]),
                source="csv",
            )
            for row in csv.DictReader(handle)
        ]
