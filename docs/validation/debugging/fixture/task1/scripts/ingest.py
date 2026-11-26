"""Import a CSV upload or a mobile inbox file into the receipt store."""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from expenses import store  # noqa: E402
from expenses.ingest_csv import read_csv  # noqa: E402
from expenses.ingest_mobile import read_jsonl  # noqa: E402


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=["csv", "mobile"], required=True)
    parser.add_argument("--file", required=True)
    parser.add_argument("--store", default=str(ROOT / "data" / "store.jsonl"))
    parser.add_argument("--replace", action="store_true",
                        help="re-import receipts that are already in the store")
    args = parser.parse_args(argv)

    incoming = read_csv(args.file) if args.source == "csv" else read_jsonl(args.file)
    merged, counts = store.upsert(store.load(args.store), incoming, replace=args.replace)
    store.save(args.store, merged)
    print(f"ingested {counts['added']} new, {counts['replaced']} replaced, "
          f"{counts['skipped']} already stored")
    return 0


if __name__ == "__main__":
    sys.exit(main())
