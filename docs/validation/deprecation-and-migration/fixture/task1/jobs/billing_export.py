"""Monthly billing export.

Owned by the billing team (owner: Rina, #billing). Deployed from their own pipeline as a
copy of this file; changes here reach production only when billing redeploys. Runs at 02:00
on the 1st of every month and writes members.csv for the invoicing system.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from members import db  # noqa: E402


def export(path="members.csv"):
    conn = db.connect()
    rows = conn.execute("SELECT id, name, email FROM members ORDER BY id").fetchall()
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["member_id", "member_name", "email"])
        for row in rows:
            writer.writerow([row["id"], row["name"], row["email"]])
    return len(rows)


if __name__ == "__main__":
    print(f"exported {export(*sys.argv[1:])} members")
