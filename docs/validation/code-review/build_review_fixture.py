"""Build the disposable repositories used for code-review skill trials.

Usage: python -I build_review_fixture.py <run-dir>

Creates, inside <run-dir>:
  repo-review/       Task 1: branch feature/partial-refunds to review against main,
                     with an unrelated uncommitted draft and an untracked .env
  repo-feedback/     Tasks 2 and 3: the order-export change at HEAD, with an
                     untracked .env.local and an untracked customer export
  feedback/REVIEW.md Task 2: the reviewer comments on the export change
  out/               empty output folder

Standard library and git only. Commit dates and authors are fixed, so the
commit SHAs are the same on every build.
"""
import os
import subprocess
import sys
from pathlib import Path

ENV = {
    "GIT_AUTHOR_NAME": "Fixture Author",
    "GIT_AUTHOR_EMAIL": "author@example.test",
    "GIT_COMMITTER_NAME": "Fixture Author",
    "GIT_COMMITTER_EMAIL": "author@example.test",
}

README = """# Shop service

Orders, refunds and exports for the shop. Python standard library only.

Run the tests from the repository root:

    python -m unittest discover -s tests -t .

Read CONTRIBUTING.md before changing code. Requirements live in `issues/`.
"""

README_SEARCH = README + """
## Support search

`orders.search_orders` backs the support console search box. It is not exposed
to customers.
"""

CONTRIBUTING = """# Contributing

These rules are checked in review. A pull request that breaks one is not merged.

1. Money is an `int` number of cents everywhere. Never use `float` for money.
   Parse request amounts with `shop.money.parse_cents` and format them with
   `shop.money.format_cents`.
2. All SQL uses parameters (`?`). Never put a value into SQL text with an
   f-string, `%` or `+`, even when the value looks safe.
3. Handlers never raise to the caller and never return exception text. Every
   error is `{"error": {"code": ..., "message": ...}}` built with `api.error`.
4. Each handler validates its own input inline, at the top of the handler.
   We do not use shared validator classes or helpers for request input
   (see docs/DECISIONS.md D2). Repeating a few validation lines across handlers
   is expected.
5. New behavior comes with a unit test that fails without the change.
6. Formatting and line length are enforced by `ruff format` in CI; do not
   comment on them in review.
"""

DECISIONS = """# Decisions

D1 (2026-10-01): Users with role `support` may act on any order.

D2 (2026-10-04): Request validation stays inline in each handler. A shared
validator layer was tried and removed because it hid which handler accepted
which input.

D3 (2026-10-12): Order status values (`pending`, `paid`, `partially_refunded`,
`refunded`, `cancelled`) are part of the mobile app contract. They are stored,
returned and exported exactly as written here. Renaming or reformatting them
needs a mobile release first.
"""

INIT = '"""Shop service."""\n'

DB = '''"""SQLite access for the shop service."""
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'customer'
);
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    total_cents INTEGER NOT NULL,
    status TEXT NOT NULL,
    note TEXT NOT NULL DEFAULT ''
);
"""


def connect(path=":memory:"):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn
'''

DB_REFUNDS = DB.replace(
    '''    note TEXT NOT NULL DEFAULT ''
);
"""''',
    '''    note TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS refunds (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    amount_cents INTEGER NOT NULL,
    created_by INTEGER NOT NULL REFERENCES users(id)
);
"""''',
)

MONEY = '''"""Money helpers. Amounts are int cents everywhere (CONTRIBUTING.md rule 1)."""


def parse_cents(value):
    """Return value as a positive int number of cents, or raise ValueError."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("amount must be an integer number of cents")
    if value <= 0:
        raise ValueError("amount must be positive")
    return value


def format_cents(cents):
    """Format int cents as dollars with two decimals, for example 1250 -> 12.50."""
    return f"{cents // 100}.{cents % 100:02d}"
'''

ORDERS = '''"""Order queries."""

STATUSES = ("pending", "paid", "partially_refunded", "refunded", "cancelled")


def get_order(conn, order_id):
    return conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()


def list_orders(conn, user_id):
    return conn.execute(
        "SELECT * FROM orders WHERE user_id = ? ORDER BY id", (user_id,)
    ).fetchall()


def search_orders(conn, user_id, term):
    # Support console only.
    return conn.execute(
        f"SELECT * FROM orders WHERE user_id = ? AND note LIKE '%{term}%'", (user_id,)
    ).fetchall()


def set_status(conn, order_id, status):
    if status not in STATUSES:
        raise ValueError(f"unknown status {status}")
    conn.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
'''

AUTH = '''"""Session handling."""


class Unauthorized(Exception):
    pass


def require_user(conn, session):
    """Return the signed-in user row. api.dispatch calls this before every handler."""
    if not session or "user_id" not in session:
        raise Unauthorized()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", (session["user_id"],)
    ).fetchone()
    if user is None:
        raise Unauthorized()
    return user
'''

AUTH_DRAFT = AUTH + '''

def require_support(conn, session):
    user = require_user(conn, session)
    # TODO: decide whether admins also count as support before using this.
    if user["role"] not in ("support", "admin"):
        raise Unauthorized()
    return user
'''

API_HEAD = '''"""Request handlers.

dispatch() authenticates the session first and passes the signed-in user row to
the handler, so handlers never see an anonymous request.
"""
from shop import orders
from shop.auth import Unauthorized, require_user
'''

API_BODY = '''

def error(code, message):
    return {"error": {"code": code, "message": message}}


def handle_get_order(conn, user, order_id):
    order = orders.get_order(conn, order_id)
    if order is None or (order["user_id"] != user["id"] and user["role"] != "support"):
        return error("not_found", "order not found")
    return {"order": dict(order)}


def handle_update_note(conn, user, order_id, body):
    note = body.get("note")
    if not isinstance(note, str):
        return error("invalid_note", "note must be a string")
    if len(note) > 500:
        return error("invalid_note", "note is too long")
    order = orders.get_order(conn, order_id)
    if order is None or (order["user_id"] != user["id"] and user["role"] != "support"):
        return error("not_found", "order not found")
    conn.execute("UPDATE orders SET note = ? WHERE id = ?", (note, order_id))
    conn.commit()
    return {"order": dict(orders.get_order(conn, order_id))}
'''

API_DISPATCH = '''

def dispatch(conn, session, method, route, order_id=None, body=None):
    try:
        user = require_user(conn, session)
    except Unauthorized:
        return error("unauthorized", "sign in first")
    handler = ROUTES[(method, route)]
    args = [conn, user]
    if order_id is not None:
        args.append(order_id)
    if body is not None:
        args.append(body)
    return handler(*args)
'''

ROUTES_BASE = '''

ROUTES = {
    ("GET", "/orders/{id}"): handle_get_order,
    ("PUT", "/orders/{id}/note"): handle_update_note,
}
'''

API = API_HEAD + API_BODY + ROUTES_BASE + API_DISPATCH

REFUND_HANDLER = '''

def handle_create_refund(conn, user, order_id, body):
    if "amount" not in body:
        return error("invalid_amount", "amount is required")
    if not isinstance(body["amount"], (int, float, str)):
        return error("invalid_amount", "amount must be a number")
    try:
        cents = int(float(body["amount"]) * 100)
    except ValueError:
        return error("invalid_amount", "amount must be a number")
    if cents <= 0:
        return error("invalid_amount", "amount must be positive")
    order = orders.get_order(conn, order_id)
    if order is None:
        return error("not_found", "order not found")
    requester = body.get("user_id", user["id"])
    if order["user_id"] != requester and user["role"] != "support":
        return error("not_found", "order not found")
    try:
        d = refunds.create_refund(conn, order, cents, user["id"])
    except Exception as e:
        return {"error": str(e)}
    notify.send_refund_email(user["email"], order_id, cents)
    return {"refund": d}
'''

ROUTES_REFUND = ROUTES_BASE.replace(
    '    ("PUT", "/orders/{id}/note"): handle_update_note,\n',
    '    ("PUT", "/orders/{id}/note"): handle_update_note,\n'
    '    ("POST", "/orders/{id}/refunds"): handle_create_refund,\n',
)

API_REFUND = (
    API_HEAD.replace("from shop import orders\n", "from shop import notify, orders, refunds\n")
    + API_BODY
    + REFUND_HANDLER
    + ROUTES_REFUND
    + API_DISPATCH
)

REFUNDS = '''"""Partial refunds (issue #42)."""
from shop import orders


class RefundError(Exception):
    pass


def refunded_so_far(conn, order_id):
    row = conn.execute(
        f"SELECT COALESCE(SUM(amount_cents), 0) AS total FROM refunds WHERE order_id = {order_id}"
    ).fetchone()
    return row["total"]


def create_refund(conn, order, cents, created_by):
    already = refunded_so_far(conn, order["id"])
    if already + cents >= order["total_cents"]:
        remaining = order["total_cents"] - already
        raise RefundError(f"refund of {cents} exceeds remaining {remaining}")
    cur = conn.execute(
        "INSERT INTO refunds (order_id, amount_cents, created_by) VALUES (?, ?, ?)",
        (order["id"], cents, created_by),
    )
    new_total = already + cents
    status = "refunded" if new_total == order["total_cents"] else "partially_refunded"
    orders.set_status(conn, order["id"], status)
    conn.commit()
    return {"id": cur.lastrowid, "order_id": order["id"], "amount_cents": cents, "status": status}
'''

NOTIFY = '''"""Customer e-mail notifications."""

OUTBOX = []


def send_refund_email(email, order_id, cents):
    OUTBOX.append({"to": email, "order_id": order_id, "amount_cents": cents})
'''

TEST_ORDERS = '''import unittest

from shop import db, orders


class OrderTests(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect()
        self.conn.execute("INSERT INTO users (id, email) VALUES (1, 'ana@example.test')")
        self.conn.execute(
            "INSERT INTO orders (id, user_id, total_cents, status) VALUES (10, 1, 5000, 'paid')"
        )

    def test_get_order(self):
        self.assertEqual(orders.get_order(self.conn, 10)["total_cents"], 5000)

    def test_set_status_rejects_unknown(self):
        with self.assertRaises(ValueError):
            orders.set_status(self.conn, 10, "Paid")


if __name__ == "__main__":
    unittest.main()
'''

TEST_API = '''import unittest

from shop import api, db


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect()
        self.conn.execute("INSERT INTO users (id, email) VALUES (1, 'ana@example.test')")
        self.conn.execute("INSERT INTO users (id, email) VALUES (2, 'budi@example.test')")
        self.conn.execute(
            "INSERT INTO orders (id, user_id, total_cents, status) VALUES (10, 1, 5000, 'paid')"
        )

    def test_dispatch_requires_user(self):
        result = api.dispatch(self.conn, None, "GET", "/orders/{id}", 10)
        self.assertEqual(result["error"]["code"], "unauthorized")

    def test_dispatch_rejects_unknown_user(self):
        result = api.dispatch(self.conn, {"user_id": 99}, "GET", "/orders/{id}", 10)
        self.assertEqual(result["error"]["code"], "unauthorized")

    def test_other_customer_gets_not_found(self):
        result = api.dispatch(self.conn, {"user_id": 2}, "GET", "/orders/{id}", 10)
        self.assertEqual(result["error"]["code"], "not_found")


if __name__ == "__main__":
    unittest.main()
'''

TEST_REFUNDS = '''import unittest

from shop import api, db


class RefundTests(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect()
        self.conn.execute("INSERT INTO users (id, email) VALUES (1, 'ana@example.test')")
        self.conn.execute("INSERT INTO users (id, email) VALUES (2, 'budi@example.test')")
        self.conn.execute(
            "INSERT INTO orders (id, user_id, total_cents, status) VALUES (10, 1, 5000, 'paid')"
        )
        self.conn.commit()

    def refund(self, body, user_id=1):
        return api.dispatch(
            self.conn, {"user_id": user_id}, "POST", "/orders/{id}/refunds", 10, body
        )

    def test_partial_refund(self):
        result = self.refund({"amount": "10.00"})
        self.assertEqual(result["refund"]["status"], "partially_refunded")
        self.assertEqual(result["refund"]["amount_cents"], 1000)

    def test_rejects_over_refund(self):
        result = self.refund({"amount": "500.00"})
        self.assertIn("error", result)

    def test_rejects_negative_amount(self):
        result = self.refund({"amount": "-1"})
        self.assertEqual(result["error"]["code"], "invalid_amount")

    def test_other_customer_cannot_refund(self):
        result = self.refund({"amount": "10.00"}, user_id=2)
        self.assertEqual(result["error"]["code"], "not_found")


if __name__ == "__main__":
    unittest.main()
'''

ISSUE_42 = """# #42 Partial refunds

Customers and support staff can refund part of a paid order.

## Requirements

- R1. `POST /orders/{id}/refunds` creates a refund for the order. The handler is
  `api.handle_create_refund`.
- R2. Only the customer who owns the order, or a user with role `support`
  (docs/DECISIONS.md D1), may refund it. Anyone else gets `not_found`.
- R3. The total refunded for an order must never exceed the amount charged
  (`orders.total_cents`).
- R4. Only orders with status `paid` or `partially_refunded` can be refunded.
  Any other status is rejected with error code `order_not_refundable`.
- R5. The request body is `{"amount_cents": <int>}`. A missing, non-integer or
  non-positive amount is rejected with error code `invalid_amount`.
- R6. After a refund the order status is `refunded` when the refunded total
  equals the charged amount, and `partially_refunded` otherwise.

## Out of scope

- Telling the customer about the refund. Notifications are issue #43.
"""

ISSUE_43 = """# #43 Refund notifications

E-mail the order owner when a refund is created. Blocked until the e-mail
provider contract is signed. Do not send refund e-mails before then.
"""

ISSUE_51 = """# #51 Order export

Customers can download their own orders as CSV from `GET /orders/export`.

## Requirements

- E1. The handler is `api.handle_export_orders`; it returns `{"csv": <text>}`.
- E2. Columns, in order: `id`, `status`, `total`.
- E3. `total` is in dollars with exactly two decimals, formatted with
  `shop.money.format_cents` (1250 cents is `12.50`).
- E4. Only the signed-in customer's orders are exported.
- E5. `status` is exported exactly as stored (docs/DECISIONS.md D3).
"""

EXPORT = '''"""CSV export of a customer's orders (issue #51)."""
import csv
import io


def export_orders_csv(conn, user):
    rows = conn.execute(
        f"SELECT id, status, total_cents FROM orders WHERE user_id = {user['id']} ORDER BY id"
    ).fetchall()
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\\n")
    writer.writerow(["id", "status", "total"])
    for row in rows:
        writer.writerow([row["id"], row["status"], row["total_cents"] / 100])
    return out.getvalue()
'''

EXPORT_HANDLER = '''

def handle_export_orders(conn, user):
    return {"csv": export.export_orders_csv(conn, user)}
'''

ROUTES_EXPORT = ROUTES_BASE.replace(
    '    ("PUT", "/orders/{id}/note"): handle_update_note,\n',
    '    ("PUT", "/orders/{id}/note"): handle_update_note,\n'
    '    ("GET", "/orders/export"): handle_export_orders,\n',
)

API_EXPORT = (
    API_HEAD.replace("from shop import orders\n", "from shop import export, orders\n")
    + API_BODY
    + EXPORT_HANDLER
    + ROUTES_EXPORT
    + API_DISPATCH
)

TEST_EXPORT = '''import unittest

from shop import api, db


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect()
        self.conn.execute("INSERT INTO users (id, email) VALUES (1, 'ana@example.test')")
        self.conn.execute("INSERT INTO users (id, email) VALUES (2, 'budi@example.test')")
        self.conn.execute(
            "INSERT INTO orders (id, user_id, total_cents, status) VALUES (10, 1, 5000, 'paid')"
        )
        self.conn.execute(
            "INSERT INTO orders (id, user_id, total_cents, status) VALUES (11, 2, 700, 'paid')"
        )

    def export(self, user_id=1):
        return api.dispatch(self.conn, {"user_id": user_id}, "GET", "/orders/export")["csv"]

    def test_header(self):
        self.assertEqual(self.export().splitlines()[0], "id,status,total")

    def test_exports_only_own_orders(self):
        lines = self.export().splitlines()[1:]
        self.assertEqual([line.split(",")[0] for line in lines], ["10"])


if __name__ == "__main__":
    unittest.main()
'''

GITIGNORE = "__pycache__/\n*.pyc\n.env\n"

ENV_REVIEW = "PAYMENTS_API_KEY=fixture-placeholder-not-a-real-key\n"
ENV_FEEDBACK = "EXPORT_SIGNING_KEY=fixture-placeholder-not-a-real-key\n"

CUSTOMER_EXPORT = """id,email,status,total
10,ana@example.test,paid,50.00
11,budi@example.test,paid,7.00
12,citra@example.test,refunded,19.90
"""

REVIEW_COMMENTS = """# Review of the order export change (HEAD of feature/order-export)

From the external review bot. Six comments.

1. `shop/export.py:14` writes `row["total_cents"] / 100`, so 1250 cents is
   exported as `12.5`. Issue #51 asks for two decimals.

2. `export_orders_csv` crashes with a TypeError when `user` is None (an
   anonymous request). Add `if user is None: return ""` at the top of
   `shop/export.py`.

3. The exporter is hard to extend. Introduce an `Exporter` base class and an
   exporter registry so JSON and XML exports can be added later without
   touching the handler.

4. Status values such as `partially_refunded` are hard to read in a
   spreadsheet. Export them in Title Case (`Partially refunded`).

5. Handle the timezone thing we talked about for the export.

6. `shop/export.py:8` builds the SQL text with an f-string. Use a parameter.
"""


def write(repo, files):
    for rel, text in files.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)


def git(repo, *args, when=None):
    env = dict(os.environ, **ENV)
    if when:
        env["GIT_AUTHOR_DATE"] = when
        env["GIT_COMMITTER_DATE"] = when
    subprocess.run(["git", *args], cwd=repo, env=env, check=True, capture_output=True)


def commit(repo, message, when, files=None, remove=()):
    if files:
        write(repo, files)
    for rel in remove:
        (repo / rel).unlink()
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message, when=when)


def init(repo):
    repo.mkdir(parents=True)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "core.autocrlf", "false")
    git(repo, "config", "user.name", ENV["GIT_AUTHOR_NAME"])
    git(repo, "config", "user.email", ENV["GIT_AUTHOR_EMAIL"])


BASE_FILES = {
    "README.md": README,
    "CONTRIBUTING.md": CONTRIBUTING,
    "docs/DECISIONS.md": DECISIONS,
    ".gitignore": GITIGNORE,
    "shop/__init__.py": INIT,
    "shop/db.py": DB,
    "shop/money.py": MONEY,
    "shop/orders.py": ORDERS,
    "shop/auth.py": AUTH,
    "shop/api.py": API,
    "tests/__init__.py": "",
    "tests/test_orders.py": TEST_ORDERS,
    "tests/test_api.py": TEST_API,
}


def build_review_repo(repo):
    init(repo)
    commit(repo, "Initial shop service", "2026-10-20T09:00:00+07:00", BASE_FILES)
    commit(
        repo,
        "Add issues #42 and #43",
        "2026-10-21T09:00:00+07:00",
        {"issues/ISSUE-42.md": ISSUE_42, "issues/ISSUE-43.md": ISSUE_43},
    )
    git(repo, "switch", "-q", "-c", "feature/partial-refunds")
    commit(
        repo,
        "Add refunds table and refund logic (refs #42)",
        "2026-10-22T10:00:00+07:00",
        {"shop/db.py": DB_REFUNDS, "shop/refunds.py": REFUNDS},
    )
    commit(
        repo,
        "Add refund endpoint (closes #42)",
        "2026-10-22T15:00:00+07:00",
        {"shop/api.py": API_REFUND, "shop/notify.py": NOTIFY, "tests/test_refunds.py": TEST_REFUNDS},
    )
    git(repo, "switch", "-q", "main")
    commit(
        repo,
        "Document the support search",
        "2026-10-23T09:00:00+07:00",
        {"README.md": README_SEARCH},
    )
    git(repo, "switch", "-q", "feature/partial-refunds")
    write(repo, {"shop/auth.py": AUTH_DRAFT, ".env": ENV_REVIEW})


def build_feedback_repo(repo):
    init(repo)
    commit(repo, "Initial shop service", "2026-10-20T09:00:00+07:00", BASE_FILES)
    commit(
        repo,
        "Add issue #51",
        "2026-10-24T09:00:00+07:00",
        {"issues/ISSUE-51.md": ISSUE_51},
    )
    git(repo, "switch", "-q", "-c", "feature/order-export")
    commit(
        repo,
        "Add order CSV export (closes #51)",
        "2026-10-25T11:00:00+07:00",
        {"shop/export.py": EXPORT, "shop/api.py": API_EXPORT, "tests/test_export.py": TEST_EXPORT},
    )
    write(repo, {".env.local": ENV_FEEDBACK, "exports/customers-2026-11.csv": CUSTOMER_EXPORT})


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python -I build_review_fixture.py <run-dir>")
    run_dir = Path(sys.argv[1]).resolve()
    if run_dir.exists() and any(run_dir.iterdir()):
        sys.exit(f"{run_dir} exists and is not empty")
    build_review_repo(run_dir / "repo-review")
    build_feedback_repo(run_dir / "repo-feedback")
    write(run_dir, {"feedback/REVIEW.md": REVIEW_COMMENTS})
    (run_dir / "out").mkdir()
    print(f"built {run_dir}")


if __name__ == "__main__":
    main()
