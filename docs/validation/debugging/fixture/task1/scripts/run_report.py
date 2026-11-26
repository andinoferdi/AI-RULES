"""Print the monthly expense report from the receipt store."""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from expenses import store  # noqa: E402
from expenses.report import format_rupiah, monthly_report  # noqa: E402


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--month", required=True, help="YYYY-MM in office time")
    parser.add_argument("--store", default=str(ROOT / "data" / "store.jsonl"))
    parser.add_argument("--ids", action="store_true", help="also list the receipt ids")
    args = parser.parse_args(argv)

    report = monthly_report(store.load(args.store).values(), args.month)
    print(f"Expense report {report['month']} (WIB)")
    print(f"receipts: {report['count']}")
    print(f"total:    {format_rupiah(report['total'])}")
    for employee, amount in report["by_employee"].items():
        print(f"  {employee:<18} {format_rupiah(amount)}")
    if args.ids:
        print("ids: " + " ".join(report["receipt_ids"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
