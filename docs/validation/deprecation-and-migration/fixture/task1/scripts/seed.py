"""Create data/members.db with 40,000 deterministic demo members."""
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from members import db  # noqa: E402

FIRST = ["Ayu", "Bima", "Citra", "Dimas", "Eka", "Fajar", "Gita", "Hadi", "Intan", "Joko"]
LAST = ["Santoso", "Wijaya", "Lestari", "Pratama", "Siregar", "Nasution", "Halim", "Putri"]


def main():
    path = db.DEFAULT_PATH
    if path.exists():
        print(f"{path} exists; refusing to overwrite", file=sys.stderr)
        return 1
    path.parent.mkdir(exist_ok=True)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "migrate.py"), "up"], check=True)
    rng = random.Random(7)
    conn = db.connect()
    rows = []
    for i in range(1, 40001):
        name = f"{rng.choice(FIRST)} {rng.choice(LAST)}"
        joined = f"20{rng.randint(19, 26)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}"
        rows.append((i, name, f"member{i}@example.test", joined))
    conn.executemany("INSERT INTO members VALUES (?, ?, ?, ?)", rows)
    conn.commit()
    print(f"seeded {len(rows)} members into {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
