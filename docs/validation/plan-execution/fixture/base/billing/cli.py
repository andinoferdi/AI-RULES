"""Command line for the billing tools.

    python -m billing.cli total [--data PATH]
"""
import argparse
import sys

from billing.invoice import calcualte_total, load_invoices

DEFAULT_DATA = "data/invoices.csv"


def main(argv=None, out=None):
    out = out or sys.stdout
    parser = argparse.ArgumentParser(prog="billing")
    commands = parser.add_subparsers(dest="command", required=True)
    total = commands.add_parser("total", help="print the total in cents")
    total.add_argument("--data", default=DEFAULT_DATA)
    args = parser.parse_args(argv)
    if args.command == "total":
        print(calcualte_total(load_invoices(args.data)), file=out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
