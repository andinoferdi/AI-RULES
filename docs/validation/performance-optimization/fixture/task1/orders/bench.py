import argparse
import hashlib
import json
import time

from .seed import seeded_database
from .summary import tenant_summary


def main():
    parser = argparse.ArgumentParser(description="Time tenant_summary on the seeded database.")
    parser.add_argument("--tenant", default="acme")
    parser.add_argument("--runs", type=int, default=5)
    args = parser.parse_args()
    db = seeded_database()
    for run in range(1, args.runs + 1):
        db.query_count = 0
        start = time.perf_counter()
        rows = tenant_summary(db, args.tenant)
        elapsed_ms = (time.perf_counter() - start) * 1000
        digest = hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()[:16]
        print(f"run={run} elapsed_ms={elapsed_ms:.1f} queries={db.query_count} "
              f"rows={len(rows)} checksum={digest}")


if __name__ == "__main__":
    main()
