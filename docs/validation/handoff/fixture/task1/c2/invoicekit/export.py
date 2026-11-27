"""Command line: python -m invoicekit.export --out invoices.csv"""
import argparse
from pathlib import Path

from invoicekit.csv_export import write_csv
from invoicekit.store import load


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    with args.out.open("w", encoding="utf-8", newline="") as fh:
        write_csv(load(), fh)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
