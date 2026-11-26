"""JSON-lines receipt store with one record per receipt id. Timestamps are stored in UTC."""
import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from .models import Receipt


def _to_record(receipt: Receipt) -> dict:
    return {
        "receipt_id": receipt.receipt_id,
        "employee": receipt.employee,
        "vendor": receipt.vendor,
        "amount": str(receipt.amount),
        "submitted_at": receipt.submitted_at.astimezone(timezone.utc).isoformat(),
        "source": receipt.source,
    }


def _from_record(record: dict) -> Receipt:
    return Receipt(
        receipt_id=record["receipt_id"],
        employee=record["employee"],
        vendor=record["vendor"],
        amount=Decimal(record["amount"]),
        submitted_at=datetime.fromisoformat(record["submitted_at"]),
        source=record["source"],
    )


def load(path) -> dict:
    path = Path(path)
    if not path.exists():
        return {}
    receipts = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                receipt = _from_record(json.loads(line))
                receipts[receipt.receipt_id] = receipt
    return receipts


def save(path, receipts: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for receipt_id in sorted(receipts):
            handle.write(json.dumps(_to_record(receipts[receipt_id]), sort_keys=True) + "\n")


def upsert(existing: dict, incoming, replace: bool = False):
    """Merge incoming receipts. Stored receipts are kept unless replace is True."""
    merged = dict(existing)
    counts = {"added": 0, "replaced": 0, "skipped": 0}
    for receipt in incoming:
        stored = merged.get(receipt.receipt_id)
        if stored is None:
            merged[receipt.receipt_id] = receipt
            counts["added"] += 1
        elif replace and stored != receipt:
            merged[receipt.receipt_id] = receipt
            counts["replaced"] += 1
        else:
            counts["skipped"] += 1
    return merged, counts
