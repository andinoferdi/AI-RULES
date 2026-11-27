"""Dry-run pending migrations against last night's production snapshot.

Restores the snapshot into a throwaway database, applies every unapplied migration inside a
transaction that is rolled back, and prints each statement with the lock it takes and the
row count of the table it touches. Exits 1 when a statement takes an ACCESS EXCLUSIVE lock on
a table above LOCK_ROW_LIMIT rows.
"""
import os
import sys

LOCK_ROW_LIMIT = 1_000_000


def main() -> int:
    url = os.environ.get("SNAPSHOT_URL")
    if not url:
        print("SNAPSHOT_URL is not set. Connect to the VPN and source ~/.ledgerly-snapshot.",
              file=sys.stderr)
        return 2
    print(f"restoring snapshot from {url} ...")
    # Restore, apply, report: omitted from this excerpt of the repository.
    return 0


if __name__ == "__main__":
    sys.exit(main())
