import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def connect(path=":memory:"):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def migrate(conn):
    for sql in sorted((ROOT / "migrations").glob("*.sql")):
        conn.executescript(sql.read_text(encoding="utf-8"))
    return conn
