import random

from .db import Database

SCHEMA = """
CREATE TABLE customers (id INTEGER PRIMARY KEY, tenant TEXT, name TEXT);
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price_cents INTEGER);
CREATE TABLE orders (id INTEGER PRIMARY KEY, tenant TEXT, customer_id INTEGER,
                     placed_at TEXT, status TEXT);
CREATE TABLE order_items (id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER,
                          quantity INTEGER);
"""


def seeded_database(orders_per_tenant=None):
    orders_per_tenant = orders_per_tenant or {"acme": 300, "globex": 40}
    rng = random.Random(20261126)
    db = Database()
    db.executescript(SCHEMA)
    conn = db.conn
    for pid in range(1, 201):
        conn.execute("INSERT INTO products VALUES (?, ?, ?)",
                     (pid, f"Product {pid:03d}", rng.randint(500, 250000)))
    cid = 0
    oid = 0
    item_id = 0
    for tenant, count in orders_per_tenant.items():
        customers = []
        for n in range(40):
            cid += 1
            conn.execute("INSERT INTO customers VALUES (?, ?, ?)",
                         (cid, tenant, f"{tenant.title()} customer {n + 1:02d}"))
            customers.append(cid)
        for n in range(count):
            oid += 1
            day = 1 + n % 28
            placed = f"2026-11-{day:02d}T{8 + n % 10:02d}:{n % 60:02d}:00Z"
            status = "open" if n % 3 else "invoiced"
            conn.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
                         (oid, tenant, rng.choice(customers), placed, status))
            for _ in range(rng.randint(1, 5)):
                item_id += 1
                conn.execute("INSERT INTO order_items VALUES (?, ?, ?, ?)",
                             (item_id, oid, rng.randint(1, 200), rng.randint(1, 4)))
    conn.commit()
    db.query_count = 0
    return db
