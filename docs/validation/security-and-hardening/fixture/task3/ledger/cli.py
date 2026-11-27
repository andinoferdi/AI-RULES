import argparse
import json
from pathlib import Path

from .config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

DATA = Path(__file__).resolve().parent.parent / "data" / "entries.json"


def page(entries: list, number: int, size: int = DEFAULT_PAGE_SIZE) -> list:
    size = max(1, min(size, MAX_PAGE_SIZE))
    start = (max(number, 1) - 1) * size
    return entries[start:start + size]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Print a page of ledger entries.")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--size", type=int, default=DEFAULT_PAGE_SIZE)
    args = parser.parse_args(argv)
    entries = json.loads(DATA.read_text(encoding="utf-8"))
    for entry in page(entries, args.page, args.size):
        print(f"{entry['date']}  {entry['memo']:<24} {entry['amount']:>12,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
