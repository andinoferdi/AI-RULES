"""Monthly expense report. Months follow office time (WIB)."""
from collections import defaultdict
from decimal import Decimal

from .tz import BUSINESS_TZ


def month_of(receipt) -> str:
    return receipt.submitted_at.astimezone(BUSINESS_TZ).strftime("%Y-%m")


def monthly_report(receipts, month: str) -> dict:
    rows = [receipt for receipt in receipts if month_of(receipt) == month]
    by_employee = defaultdict(Decimal)
    for receipt in rows:
        by_employee[receipt.employee] += receipt.amount
    return {
        "month": month,
        "count": len(rows),
        "total": sum((receipt.amount for receipt in rows), Decimal(0)),
        "by_employee": dict(sorted(by_employee.items())),
        "receipt_ids": sorted(receipt.receipt_id for receipt in rows),
    }


def format_rupiah(amount: Decimal) -> str:
    whole = int(amount.quantize(Decimal(1)))
    return "Rp " + f"{whole:,}".replace(",", ".")
