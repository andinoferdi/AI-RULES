import json
import os
import tempfile
from typing import List

from .dates import parse_iso_date
from .models import Installment, Loan


def load_loans(path: str) -> List[Loan]:
    """Read every loan from the JSON data file. Raises FileNotFoundError."""
    with open(path, encoding="utf-8") as handle:
        raw = json.load(handle)
    loans = []
    for item in raw["loans"]:
        installments = [
            Installment(
                number=inst["number"],
                due_date=parse_iso_date(inst["due_date"]),
                amount=inst["amount"],
            )
            for inst in item["installments"]
        ]
        loans.append(Loan(
            loan_id=item["loan_id"],
            member_id=item["member_id"],
            member_name=item["member_name"],
            principal=item["principal"],
            installments=installments,
        ))
    return loans


def save_loans(path: str, loans: List[Loan]) -> None:
    """Write every loan back, replacing the file atomically."""
    raw = {"loans": [
        {
            "loan_id": loan.loan_id,
            "member_id": loan.member_id,
            "member_name": loan.member_name,
            "principal": loan.principal,
            "installments": [
                {"number": inst.number, "due_date": inst.due_date.isoformat(),
                 "amount": inst.amount}
                for inst in loan.installments
            ],
        }
        for loan in loans
    ]}
    directory = os.path.dirname(os.path.abspath(path))
    fd, temp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(raw, handle, indent=2, ensure_ascii=False)
    os.replace(temp_path, path)
