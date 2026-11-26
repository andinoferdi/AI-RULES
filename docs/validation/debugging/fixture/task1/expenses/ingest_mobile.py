"""Import receipts pulled from the mobile app (one JSON object per line)."""
import json
from decimal import Decimal

from .models import Receipt
from .timeparse import parse_app_timestamp


def parse_payload(payload: dict) -> Receipt:
    return Receipt(
        receipt_id=payload["receipt_id"],
        employee=payload["employee"],
        vendor=payload["vendor"].strip(),
        amount=Decimal(str(payload["amount"])),
        submitted_at=parse_app_timestamp(payload["submitted_at"]),
        source="mobile",
    )


def read_jsonl(path):
    receipts = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                receipts.append(parse_payload(json.loads(line)))
    return receipts
