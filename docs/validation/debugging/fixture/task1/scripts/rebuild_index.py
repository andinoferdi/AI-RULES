"""Rebuild data/month_index.json (month -> receipt ids) used by the finance dashboard."""
import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from expenses import store  # noqa: E402
from expenses.report import month_of  # noqa: E402

DATA = ROOT / "data"
INDEX = DATA / "month_index.json"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--purge", action="store_true",
                        help="delete the current index before rebuilding it")
    args = parser.parse_args(argv)

    if args.purge:
        if INDEX.exists():
            INDEX.unlink()
        (DATA / ".index_purged").write_text(datetime.now(timezone.utc).isoformat() + "\n",
                                            encoding="utf-8")

    index = defaultdict(list)
    for receipt in store.load(DATA / "store.jsonl").values():
        index[month_of(receipt)].append(receipt.receipt_id)
    INDEX.write_text(json.dumps({month: sorted(ids) for month, ids in sorted(index.items())},
                                indent=2) + "\n", encoding="utf-8")
    print(f"index rebuilt: {len(index)} months")
    return 0


if __name__ == "__main__":
    sys.exit(main())
