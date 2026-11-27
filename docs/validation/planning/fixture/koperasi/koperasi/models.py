from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Installment:
    number: int
    due_date: date
    amount: int  # whole rupiah


@dataclass
class Loan:
    loan_id: str
    member_id: str
    member_name: str
    principal: int  # whole rupiah
    installments: List[Installment] = field(default_factory=list)
