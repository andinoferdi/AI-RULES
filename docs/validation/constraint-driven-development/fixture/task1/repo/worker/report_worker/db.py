"""Reads paid invoices from the reporting replica."""

import os

import psycopg


def fetch_paid_rows(month: str) -> list[dict[str, int]]:
    dsn = os.environ["REPORTING_DSN"]
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT total_cents, paid::int FROM invoices WHERE to_char(issued_at, 'YYYY-MM') = %s",
                (month,),
            )
            columns = [column.name for column in cur.description or []]
            rows = cur.fetchall()
    result = []
    for row in rows:
        record = dict(zip(columns, row))
        if record.get("total_cents") is None:
            continue
        result.append({"total_cents": int(record["total_cents"]), "paid": int(record["paid"])})
    return result
