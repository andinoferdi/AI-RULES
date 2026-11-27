"""Apply or revert the SQL migrations in migrations/.

    python scripts/migrate.py status | up | down

`up` applies every pending NNNN_*.up.sql in order. `down` runs the .down.sql of the last
applied migration only. Applied versions are kept in the schema_migrations table.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from members import db  # noqa: E402

MIGRATIONS = Path(__file__).resolve().parent.parent / "migrations"


def available():
    return sorted(p.name[: -len(".up.sql")] for p in MIGRATIONS.glob("*.up.sql"))


def applied(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version TEXT PRIMARY KEY)")
    return [r[0] for r in conn.execute("SELECT version FROM schema_migrations ORDER BY version")]


def main(argv):
    command = argv[1] if len(argv) > 1 else "status"
    conn = db.connect()
    done = applied(conn)
    if command == "status":
        for version in available():
            print(("applied  " if version in done else "pending  ") + version)
        return 0
    if command == "up":
        for version in available():
            if version in done:
                continue
            conn.executescript((MIGRATIONS / f"{version}.up.sql").read_text(encoding="utf-8"))
            conn.execute("INSERT INTO schema_migrations VALUES (?)", (version,))
            conn.commit()
            print(f"applied {version}")
        return 0
    if command == "down":
        if not done:
            print("nothing to revert")
            return 0
        version = done[-1]
        down = MIGRATIONS / f"{version}.down.sql"
        if not down.exists():
            print(f"no down migration for {version}", file=sys.stderr)
            return 1
        conn.executescript(down.read_text(encoding="utf-8"))
        conn.execute("DELETE FROM schema_migrations WHERE version = ?", (version,))
        conn.commit()
        print(f"reverted {version}")
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
