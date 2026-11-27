from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Invoice:
    number: str
    customer: str
    issued: date
    kind: str  # "invoice" or "credit_note"
    amount_idr: int

    def amount_text(self) -> str:
        """Whole rupiah, no separators, as Budi's import macro expects."""
        return str(self.amount_idr)
