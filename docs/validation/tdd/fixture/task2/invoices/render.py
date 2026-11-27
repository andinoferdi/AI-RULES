"""Read an invoice CSV and print it.

    python -m invoices.render INV-2026-0412
"""
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

from invoices.footer import footer
from invoices.money import format_idr, parse_idr
from invoices.tax import ppn

DATA = Path(__file__).resolve().parent.parent / "data" / "invoices"


@dataclass
class Invoice:
    number: str
    lines: list[tuple[str, int, int]]

    @property
    def subtotal(self) -> int:
        return sum(quantity * price for _, quantity, price in self.lines)

    @property
    def tax(self) -> int:
        return ppn([(quantity, price) for _, quantity, price in self.lines])

    @property
    def total(self) -> int:
        return self.subtotal + self.tax


def load(number: str, folder: Path = DATA) -> Invoice:
    with open(folder / f"{number}.csv", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return Invoice(number, [(row["item"], int(row["qty"]), parse_idr(row["unit_price"]))
                            for row in rows])


def render(invoice: Invoice) -> str:
    out = [f"Invoice {invoice.number}"]
    for item, quantity, price in invoice.lines:
        out.append(f"  {item:<20} {quantity:>3} x {format_idr(price):>12}")
    out.append(f"  {'Subtotal':<26} {format_idr(invoice.subtotal):>14}")
    out.append(f"  {'PPN 11%':<26} {format_idr(invoice.tax):>14}")
    out.append(f"  {'Total':<26} {format_idr(invoice.total):>14}")
    out.append(footer())
    return "\n".join(out)


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: python -m invoices.render INVOICE-NUMBER", file=sys.stderr)
        return 2
    print(render(load(argv[0])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
