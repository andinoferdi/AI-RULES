import json
from pathlib import Path

SEED = Path(__file__).resolve().parent.parent / "data" / "seed.json"


def load(conn) -> None:
    data = json.loads(SEED.read_text(encoding="utf-8"))
    conn.executemany("insert into users values (:id, :tenant_id, :name, :token)", data["users"])
    conn.executemany("insert into invoices values (:id, :tenant_id, :number, :amount)",
                     data["invoices"])
    conn.commit()
