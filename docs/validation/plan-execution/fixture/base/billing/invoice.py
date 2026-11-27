"""Invoice rows loaded from data/invoices.csv."""
import csv
import os
from dataclasses import dataclass

from billing.money import parse_amount


@dataclass(frozen=True)
class Invoice:
    number: str
    customer: str
    amount_cents: int


def load_invoices(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return [Invoice(row["number"], row["customer"], parse_amount(row["amount"]))
                for row in csv.DictReader(handle)]


def calcualte_total(invoices):
    return sum(inv.amount_cents for inv in invoices)
