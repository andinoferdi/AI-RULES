"""Monthly invoice run (cron, 1st of the month, 03:00).

Owned by finance ops (Wulan). Lines whose quote is empty are skipped: discontinued items
stay on old standing orders and must not be billed.
"""
import csv
import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "config" / "reports.json").read_text(encoding="utf-8"))


def _engine():
    module_name, func_name = CONFIG["quote_engine"].rsplit(":", 1)
    return getattr(importlib.import_module(module_name), func_name)


def invoice_totals(orders_csv):
    quote = _engine()
    totals = {}
    with open(orders_csv, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            amount = quote(row["sku"], int(row["qty"]))
            if not amount:
                continue
            totals[row["customer"]] = totals.get(row["customer"], 0) + amount
    return totals


if __name__ == "__main__":
    totals = invoice_totals(sys.argv[1])
    for customer in sorted(totals):
        print(f"{customer}: Rp {totals[customer]:,}".replace(",", "."))
    print(f"TOTAL: Rp {sum(totals.values()):,}".replace(",", "."))
