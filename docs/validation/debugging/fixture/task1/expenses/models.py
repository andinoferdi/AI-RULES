from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Receipt:
    receipt_id: str
    employee: str
    vendor: str
    amount: Decimal  # rupiah
    submitted_at: datetime  # always timezone-aware
    source: str  # "csv" or "mobile"
