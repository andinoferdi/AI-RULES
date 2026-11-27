import sqlite3

SCHEMA = """
create table if not exists users (
    id text primary key, tenant_id text not null, name text not null, token text not null unique
);
create table if not exists invoices (
    id integer primary key, tenant_id text not null, number text not null, amount integer not null
);
create table if not exists attachments (
    id integer primary key autoincrement, invoice_id integer not null, tenant_id text not null,
    filename text not null, path text not null, etag text not null
);
"""

_conn: sqlite3.Connection | None = None


def connect(path: str = ":memory:") -> sqlite3.Connection:
    global _conn
    _conn = sqlite3.connect(path)
    _conn.row_factory = sqlite3.Row
    _conn.executescript(SCHEMA)
    return _conn


def conn() -> sqlite3.Connection:
    if _conn is None:
        raise RuntimeError("database not connected")
    return _conn
