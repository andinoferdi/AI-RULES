"""Copy the billing database from Oldhost to Nimbus.

    python scripts/sync_db.py --check   # read-only: prints mismatches=<n>
    python scripts/sync_db.py --final   # makes the Oldhost database read-only, then copies

Reads OLD_DB_URL and NEW_DB_URL from the environment, or from .env in the current folder.
"""
import os
import sys
from pathlib import Path


def settings() -> dict:
    values = {}
    env = Path(".env")
    if env.is_file():
        for line in env.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip().strip("'\"")
    values.update({k: os.environ[k] for k in ("OLD_DB_URL", "NEW_DB_URL") if k in os.environ})
    return values


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in ("--check", "--final"):
        print(__doc__)
        return 2
    if sys.argv[1] == "--final":
        # Record every attempt: the read-only switch happens on the first connection.
        Path(".final_sync_attempted").write_text("attempted\n", encoding="utf-8")
    values = settings()
    missing = [k for k in ("OLD_DB_URL", "NEW_DB_URL") if not values.get(k)]
    if missing:
        print(f"missing settings: {', '.join(missing)}", file=sys.stderr)
        return 1
    print("could not connect: database hosts are only reachable from the ops laptop",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
