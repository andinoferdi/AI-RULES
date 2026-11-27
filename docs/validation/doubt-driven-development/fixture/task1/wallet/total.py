"""Print the total of all balances in rupiah, for either schema version."""
import json
import sys
from pathlib import Path


def total_rupiah(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    total = sum(account["balance"] for account in data["accounts"])
    return total // 100 if data["schema_version"] >= 2 else total


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    print(f"total_rupiah={total_rupiah(argv[0])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
