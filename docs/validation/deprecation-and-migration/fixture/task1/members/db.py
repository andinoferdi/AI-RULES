import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = ROOT / "data" / "members.db"


def connect(path=None):
    conn = sqlite3.connect(str(path or os.environ.get("MEMBERS_DB") or DEFAULT_PATH))
    conn.row_factory = sqlite3.Row
    return conn
