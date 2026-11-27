import argparse
import sys
from datetime import date
from typing import List, Optional

from .dates import days_between
from .money import format_rupiah
from .store import load_loans

DEFAULT_DATA = "data/loans.json"


def _cmd_list(args: argparse.Namespace) -> int:
    try:
        loans = load_loans(args.data)
    except FileNotFoundError:
        print(f"File data tidak ditemukan: {args.data}", file=sys.stderr)
        return 1
    today = date.today()
    for loan in loans:
        first_due = loan.installments[0].due_date if loan.installments else today
        age = days_between(first_due, today)
        print(f"{loan.loan_id}  {loan.member_name}  {format_rupiah(loan.principal)}"
              f"  {len(loan.installments)} cicilan  {age} hari")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="koperasi")
    commands = parser.add_subparsers(dest="command", required=True)
    list_parser = commands.add_parser("list", help="show every loan")
    list_parser.add_argument("--data", default=DEFAULT_DATA)
    list_parser.set_defaults(handler=_cmd_list)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    sys.exit(main())
