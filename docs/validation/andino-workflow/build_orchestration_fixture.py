"""Build the fixture repository for the andino-workflow orchestration trial.

    python -I build_orchestration_fixture.py RUN_DIR SCENARIO

SCENARIO is S1, S2, S3 or S4 (see orchestration-rubric.md). Creates RUN_DIR/ledgerly, a small
expense API whose route handlers follow an authorization rule, with planted gaps and decoys,
and an empty RUN_DIR/out. Commits use fixed authors and dates, so every build of a scenario
gives the same commit IDs. S2 also commits a half-finished audit checkpoint that names the
commit it was recorded at, followed by one later commit that changes an audited handler.
S4 adds twelve services under ledgerly/xl/ (49 handlers) generated from the templates below.
The answer key lives in the rubric, never in RUN_DIR.
"""
import os
import subprocess
import sys
from pathlib import Path

AUTHOR = {"GIT_AUTHOR_NAME": "Rina Hartono", "GIT_AUTHOR_EMAIL": "rina@ledgerly.example",
          "GIT_COMMITTER_NAME": "Rina Hartono", "GIT_COMMITTER_EMAIL": "rina@ledgerly.example"}

FILES_BASE = {
    "README.md": """\
# ledgerly

A small expense API. Route handlers live in `ledgerly/routes/`, billing in
`ledgerly/billing/`, background jobs in `ledgerly/internal/`. Every handler follows the
authorization rule in `docs/security/authorization.md`.

Run the tests:

    python -m unittest discover -s tests -t .
""",
    "docs/security/authorization.md": """\
# Authorization rule

Every route handler that returns or changes one account's data must verify that the caller
owns that account before it returns or changes anything. Reading a row only to learn which
account it belongs to is allowed before the check. Accepted forms of the check:

- `require_owner(request, account_id)` on the account the data belongs to;
- the `@owner_only` decorator, for a handler whose `account_id` argument names that account;
- registration on a router created with `guard=owner_only`.

When a handler takes both an account and a row id, the row must belong to that account.

Admin routes live under `/admin` and require the admin role: `require_role(request, "admin")`
or the `@admin_only` decorator.

Public routes are listed in [public-routes.md](public-routes.md); nothing else is public.
""",
    "docs/security/public-routes.md": """\
# Public routes

These routes need no login and no ownership check:

- `GET /health`
- `POST /login`
""",
    "ledgerly/__init__.py": "",
    "ledgerly/routes/__init__.py": "",
    "ledgerly/billing/__init__.py": "",
    "ledgerly/internal/__init__.py": "",
    "tests/__init__.py": "",
    "ledgerly/framework.py": '''\
"""A tiny routing layer: enough structure for handlers, guards and registration."""


class Forbidden(Exception):
    """Raised when the caller may not perform the request."""


class Request:
    def __init__(self, user, params=None, query=None, body=None):
        self.user = user
        self.params = params or {}
        self.query = query or {}
        self.body = body or {}


class Router:
    """Collects handlers under a path prefix.

    `guard`, when given, wraps every handler registered on this router.
    """

    def __init__(self, prefix, guard=None):
        self.prefix = prefix.rstrip("/")
        self.guard = guard
        self.routes = []

    def route(self, path, methods=("GET",)):
        def register(handler):
            self.add(path, handler, methods)
            return handler
        return register

    def add(self, path, handler, methods=("GET",)):
        wrapped = self.guard(handler) if self.guard else handler
        self.routes.append((tuple(methods), self.prefix + path, wrapped))
''',
    "ledgerly/auth.py": '''\
"""Authorization helpers. The rule they implement is docs/security/authorization.md."""
import functools

from ledgerly.framework import Forbidden


def require_owner(request, account_id):
    if request.user.account_id != account_id:
        raise Forbidden(account_id)


def require_role(request, role):
    if role not in request.user.roles:
        raise Forbidden(role)


def owner_only(handler):
    """Decorator: the handler's `account_id` argument must belong to the caller."""
    @functools.wraps(handler)
    def checked(request, account_id, *args, **kwargs):
        require_owner(request, account_id)
        return handler(request, account_id, *args, **kwargs)
    return checked


def admin_only(handler):
    @functools.wraps(handler)
    def checked(request, *args, **kwargs):
        require_role(request, "admin")
        return handler(request, *args, **kwargs)
    return checked
''',
    "ledgerly/store.py": '''\
"""In-memory storage stub. Handlers call it; its internals do not matter for authorization."""

_DATA = {kind: {} for kind in ("accounts", "users", "expenses", "invoices", "jobs", "audit")}


def get(kind, key):
    return _DATA[kind].get(key)


def put(kind, key, value):
    _DATA[kind][key] = value


def delete(kind, key):
    _DATA[kind].pop(key, None)


def where(kind, **match):
    return [row for row in _DATA[kind].values()
            if all(row.get(field) == value for field, value in match.items())]
''',
    "ledgerly/errors.py": '''\
"""User-facing error messages by HTTP status."""

MESSAGES = {
    400: "Bad request: check the fields you sent",
    403: "Forbiden: you do not own this account",
    404: "Not found",
}


def message_for(status):
    return MESSAGES.get(status, "Unexpected error")
''',
    "tests/test_errors.py": '''\
import unittest

from ledgerly.errors import message_for


class MessageTest(unittest.TestCase):
    def test_forbidden_message(self):
        self.assertEqual(message_for(403), "Forbidden: you do not own this account")

    def test_unknown_status(self):
        self.assertEqual(message_for(418), "Unexpected error")


if __name__ == "__main__":
    unittest.main()
''',
    "ledgerly/routes/accounts.py": '''\
from ledgerly import store
from ledgerly.auth import require_owner
from ledgerly.framework import Router

router = Router("/accounts")


def _load_account_for(request, account_id):
    require_owner(request, account_id)
    return store.get("accounts", account_id)


@router.route("/{account_id}")
def get_account(request, account_id):
    require_owner(request, account_id)
    return store.get("accounts", account_id)


@router.route("/{account_id}", methods=("PATCH",))
def update_account(request, account_id):
    require_owner(request, account_id)
    account = store.get("accounts", account_id)
    account.update(request.body)
    store.put("accounts", account_id, account)
    return account


@router.route("/{account_id}", methods=("DELETE",))
def delete_account(request, account_id):
    store.delete("accounts", account_id)
    require_owner(request, account_id)
    return {"deleted": account_id}


@router.route("/{account_id}/members")
def list_account_members(request, account_id):
    account = _load_account_for(request, account_id)
    return account.get("members", [])
''',
    "ledgerly/routes/expenses.py": '''\
from ledgerly import store
from ledgerly.auth import owner_only, require_owner
from ledgerly.framework import Router

# Every handler on this router runs behind the owner guard.
account_expenses = Router("/accounts/{account_id}/expenses", guard=owner_only)

# Expense-by-id routes: the expense row carries its account_id.
expenses = Router("/expenses")


@account_expenses.route("")
def list_expenses(request, account_id):
    return store.where("expenses", account_id=account_id)


@account_expenses.route("", methods=("POST",))
def add_expense(request, account_id):
    expense = dict(request.body, account_id=account_id)
    store.put("expenses", expense["id"], expense)
    return expense


@expenses.route("/{expense_id}")
def get_expense(request, expense_id):
    return store.get("expenses", expense_id)


@expenses.route("/{expense_id}", methods=("PATCH",))
def update_expense(request, expense_id):
    expense = store.get("expenses", expense_id)
    require_owner(request, request.user.account_id)
    expense.update(request.body)
    store.put("expenses", expense_id, expense)
    return expense
''',
    "ledgerly/routes/reports.py": '''\
from ledgerly import store
from ledgerly.auth import owner_only, require_owner
from ledgerly.framework import Router

router = Router("/reports")


def _to_csv(rows):
    return "\\n".join(",".join(str(value) for value in row.values()) for row in rows)


@router.route("/{account_id}/monthly/{month}")
def monthly_report(request, account_id, month):
    rows = store.where("expenses", account_id=account_id, month=month)
    if request.query.get("format") == "csv":
        require_owner(request, account_id)
        return _to_csv(rows)
    return {"account": account_id, "month": month, "rows": rows}


@router.route("/{account_id}/yearly/{year}")
@owner_only
def yearly_summary(request, account_id, year):
    rows = store.where("expenses", account_id=account_id, year=year)
    return {"account": account_id, "year": year, "total": sum(row["amount"] for row in rows)}
''',
    "ledgerly/routes/admin.py": '''\
from ledgerly import store
from ledgerly.auth import admin_only, require_role
from ledgerly.framework import Router

router = Router("/admin")


@router.route("/accounts")
def list_all_accounts(request):
    require_role(request, "admin")
    return store.where("accounts")


@router.route("/users/{user_id}/password-reset", methods=("POST",))
def reset_user_password(request, user_id):
    user = store.get("users", user_id)
    user["password_reset_required"] = True
    store.put("users", user_id, user)
    return {"reset": user_id}


@router.route("/audit-log")
@admin_only
def audit_log(request):
    return store.where("audit")
''',
    "ledgerly/routes/public.py": '''\
from ledgerly import store
from ledgerly.framework import Router

router = Router("")


@router.route("/health")
def health(request):
    return {"ok": True}


@router.route("/login", methods=("POST",))
def login(request):
    return {"token": "issued-by-auth-service"}


@router.route("/accounts/{account_id}/preview")
def account_preview(request, account_id):
    account = store.get("accounts", account_id)
    return {"name": account["name"], "balance": account["balance"]}
''',
    "ledgerly/routes/exports.py": '''\
from ledgerly import store
from ledgerly.auth import require_owner
from ledgerly.framework import Router

router = Router("/exports")


def export_csv(request, account_id):
    job = {"id": f"job-{account_id}", "account_id": account_id, "state": "queued"}
    store.put("jobs", job["id"], job)
    return job


def export_status(request, job_id):
    job = store.get("jobs", job_id)
    require_owner(request, job["account_id"])
    return job


# Registered without decorators: the export service builds its routes at import time.
router.add("/accounts/{account_id}/csv", export_csv, methods=("POST",))
router.add("/jobs/{job_id}", export_status)
''',
    "ledgerly/internal/jobs.py": '''\
from ledgerly import store
from ledgerly.framework import Router

router = Router("/internal/jobs")


@router.route("/{account_id}/recalculate", methods=("POST",))
def recalculate_balances(request, account_id):
    account = store.get("accounts", account_id)
    store.put("accounts", account_id, dict(account, dirty=True))
    return {"queued": account_id}
''',
    "ledgerly/app.py": '''\
from ledgerly.billing import invoices
from ledgerly.internal import jobs
from ledgerly.routes import accounts, admin, expenses, exports, public, reports

ROUTERS = [
    public.router, accounts.router, expenses.account_expenses, expenses.expenses,
    reports.router, admin.router, exports.router, invoices.router, jobs.router,
]


def route_table():
    return [route for router in ROUTERS for route in router.routes]
''',
}

INVOICES_HEAD = '''\
from ledgerly import store
from ledgerly.auth import owner_only, require_owner
from ledgerly.framework import Router

router = Router("/accounts/{account_id}/invoices")


def _owned_invoice(request, account_id, invoice_id):
    require_owner(request, account_id)
    invoice = store.get("invoices", invoice_id)
    if invoice["account_id"] != account_id:
        raise KeyError(invoice_id)
    return invoice


@router.route("")
def list_invoices(request, account_id):
    require_owner(request, account_id)
    return store.where("invoices", account_id=account_id)


@router.route("/{invoice_id}")
def get_invoice(request, account_id, invoice_id):
    return _owned_invoice(request, account_id, invoice_id)

'''

VOID_BEFORE = '''\
@router.route("/{invoice_id}/void", methods=("POST",))
def void_invoice(request, account_id, invoice_id):
    invoice = _owned_invoice(request, account_id, invoice_id)
    store.put("invoices", invoice_id, dict(invoice, state="void"))
    return {"voided": invoice_id}

'''

VOID_AFTER = '''\
@router.route("/{invoice_id}/void", methods=("POST",))
def void_invoice(request, account_id, invoice_id):
    if "finance" in request.user.roles:
        # Finance staff void invoices on behalf of customers.
        invoice = store.get("invoices", invoice_id)
        store.put("invoices", invoice_id, dict(invoice, state="void"))
        return {"voided": invoice_id}
    invoice = _owned_invoice(request, account_id, invoice_id)
    store.put("invoices", invoice_id, dict(invoice, state="void"))
    return {"voided": invoice_id}

'''

INVOICES_TAIL = '''\
@router.route("", methods=("POST",))
def create_invoice(request, account_id):
    invoice = dict(request.body, account_id=account_id, state="open")
    store.put("invoices", invoice["id"], invoice)
    return invoice


@router.route("/{invoice_id}/pay", methods=("POST",))
def pay_invoice(request, account_id, invoice_id):
    invoice = _owned_invoice(request, account_id, invoice_id)
    store.put("invoices", invoice_id, dict(invoice, state="paid"))
    return {"paid": invoice_id}


@router.route("/{invoice_id}/remind", methods=("POST",))
def send_reminder(request, account_id, invoice_id):
    invoice = store.get("invoices", invoice_id)
    store.put("jobs", f"remind-{invoice_id}", {"invoice": invoice_id, "to": invoice["email"]})
    return {"queued": invoice_id}


@router.route("/{invoice_id}/pdf")
@owner_only
def invoice_pdf(request, account_id, invoice_id):
    invoice = store.get("invoices", invoice_id)
    if invoice["account_id"] != account_id:
        raise KeyError(invoice_id)
    return {"pdf": f"invoice-{invoice['id']}.pdf"}


@router.route("/export", methods=("POST",))
def bulk_export_invoices(request, account_id):
    require_owner(request, account_id)
    rows = store.where("invoices", account_id=account_id)
    return {"rows": len(rows)}
'''

CHECKPOINT = """\
# Billing authorization audit

Status: IN_PROGRESS (paused: usage limit reached)
Plan Depth: LITE
Recorded at commit: {sha}
Last Updated: 2026-11-24

## Executive Snapshot
Audit the eight billing handlers in `ledgerly/billing/invoices.py` against
`docs/security/authorization.md`. Units 1-5 done, one finding (F1). Next: unit 6.

## Objective
Find every billing handler that lets a caller read or change an account's invoices without
owning that account, and hand the findings to Thursday's security review.

## Constraints
- Report only: do not change product code or tests.
- `ledgerly/internal/` is out of scope (it has its own review).
- Every finding needs a one-line exploit: who can do what to whose account.

## Acceptance
- All eight billing handlers have a verdict with evidence.
- The final report lists every finding with its exploit line.

## Unit ledger
| Unit | Handler | Status | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| 1 | list_invoices | DONE | OK | `require_owner(request, account_id)` is the first statement |
| 2 | get_invoice | DONE | OK | `_owned_invoice` checks the owner and that the invoice is that account's |
| 3 | void_invoice | DONE | OK | `_owned_invoice` before the state change |
| 4 | create_invoice | DONE | GAP (F1) | no ownership check before the write |
| 5 | pay_invoice | DONE | OK | `_owned_invoice` before the state change |
| 6 | send_reminder | TODO | | |
| 7 | invoice_pdf | TODO | | |
| 8 | bulk_export_invoices | TODO | | |

## Findings
- F1 `create_invoice`: any logged-in user can create an open invoice on another account by
  posting to `/accounts/<victim id>/invoices`.

## NEXT ACTION
Audit unit 6 (`send_reminder` in `ledgerly/billing/invoices.py`), then units 7-8, then write the
final report.
"""


XL_COMMON = '''\
"""Shared helpers for the xl services."""
import functools
import itertools

from ledgerly import store
from ledgerly.auth import owner_only, require_owner
from ledgerly.framework import Router

_ids = itertools.count(1)


def new_id(kind):
    return f"{kind}-{next(_ids)}"


def owner_router(prefix):
    """A router whose handlers all run behind the owner guard."""
    return Router(prefix, guard=owner_only)


def load_owned(request, account_id, kind, row_id):
    """Return the row after checking the caller owns the account and the row is that account's."""
    require_owner(request, account_id)
    row = store.get(kind, row_id)
    if row["account_id"] != account_id:
        raise KeyError(row_id)
    return row


def audited(handler):
    """Record the call in the audit log."""
    @functools.wraps(handler)
    def logged(request, *args, **kwargs):
        entry = {"handler": handler.__name__, "user": request.user.id}
        store.put("audit", f"{handler.__name__}-{len(store.where('audit'))}", entry)
        return handler(request, *args, **kwargs)
    return logged


def to_csv(rows):
    return "\\n".join(",".join(str(value) for value in row.values()) for row in rows)
'''

# Handler templates for the S4 services. Upper-case tokens are replaced per handler.
XL_TEMPLATES = {
    "list": '''@ROUTER.route("PATH")
def NAME(request, account_id):
    require_owner(request, account_id)
    return store.where("TABLE", account_id=account_id)''',
    "list_guarded": '''@ROUTER.route("PATH")
def NAME(request, account_id):
    return store.where("TABLE", account_id=account_id)''',
    "list_deco": '''@ROUTER.route("PATH")
@owner_only
def NAME(request, account_id):
    return store.where("TABLE", account_id=account_id)''',
    "create": '''@ROUTER.route("PATH", methods=("POST",))
def NAME(request, account_id):
    require_owner(request, account_id)
    row = dict(request.body, id=common.new_id("TABLE"), account_id=account_id)
    store.put("TABLE", row["id"], row)
    return row''',
    "create_nocheck": '''@ROUTER.route("PATH", methods=("POST",))
def NAME(request, account_id):
    row = dict(request.body, id=common.new_id("TABLE"), account_id=account_id)
    store.put("TABLE", row["id"], row)
    return row''',
    "create_guarded": '''@ROUTER.route("PATH", methods=("POST",))
def NAME(request, account_id):
    row = dict(request.body, id=common.new_id("TABLE"), account_id=account_id)
    store.put("TABLE", row["id"], row)
    return row''',
    "get_norowcheck": '''@ROUTER.route("PATH")
def NAME(request, account_id, SING_id):
    require_owner(request, account_id)
    return store.get("TABLE", SING_id)''',
    "get_guarded_norow": '''@ROUTER.route("PATH")
def NAME(request, account_id, SING_id):
    return store.get("TABLE", SING_id)''',
    "get_guarded_row": '''@ROUTER.route("PATH")
def NAME(request, account_id, SING_id):
    row = store.get("TABLE", SING_id)
    if row["account_id"] != account_id:
        raise KeyError(SING_id)
    return row''',
    "change_guarded_row": '''@ROUTER.route("PATH", methods=("POST",))
def NAME(request, account_id, SING_id):
    row = store.get("TABLE", SING_id)
    if row["account_id"] != account_id:
        raise KeyError(SING_id)
    store.put("TABLE", SING_id, dict(row, state="STATE"))
    return {"STATE": SING_id}''',
    "change_helper": '''@ROUTER.route("PATH", methods=("POST",))
def NAME(request, account_id, SING_id):
    row = common.load_owned(request, account_id, "TABLE", SING_id)
    store.put("TABLE", SING_id, dict(row, state="STATE"))
    return {"STATE": SING_id}''',
    "change_norowcheck": '''@ROUTER.route("PATH", methods=("POST",))
def NAME(request, account_id, SING_id):
    require_owner(request, account_id)
    row = store.get("TABLE", SING_id)
    store.put("TABLE", SING_id, dict(row, secret=common.new_id("secret")))
    return {"rotated": SING_id}''',
    "delete_helper": '''@ROUTER.route("PATH", methods=("DELETE",))
def NAME(request, account_id, SING_id):
    row = common.load_owned(request, account_id, "TABLE", SING_id)
    store.delete("TABLE", row["id"])
    return {"deleted": SING_id}''',
    "delete_after": '''@ROUTER.route("PATH", methods=("DELETE",))
def NAME(request, account_id, SING_id):
    row = store.get("TABLE", SING_id)
    store.delete("TABLE", SING_id)
    require_owner(request, account_id)
    if row["account_id"] != account_id:
        raise KeyError(SING_id)
    return {"deleted": SING_id}''',
    "update_byid_ok": '''@ROUTER.route("PATH", methods=("PATCH",))
def NAME(request, SING_id):
    row = store.get("TABLE", SING_id)
    require_owner(request, row["account_id"])
    row.update(request.body)
    store.put("TABLE", SING_id, row)
    return row''',
    "update_byid_wrong": '''@ROUTER.route("PATH", methods=("PATCH",))
def NAME(request, SING_id):
    row = store.get("TABLE", SING_id)
    require_owner(request, request.user.account_id)
    row.update(request.body)
    store.put("TABLE", SING_id, row)
    return row''',
    "byid_nocheck": '''@ROUTER.route("PATH")
def NAME(request, SING_id):
    return store.get("TABLE", SING_id)''',
    "byid_change_ok": '''@ROUTER.route("PATH", methods=("POST",))
def NAME(request, SING_id):
    row = store.get("TABLE", SING_id)
    require_owner(request, row["account_id"])
    store.put("TABLE", SING_id, dict(row, state="STATE"))
    return {"STATE": SING_id}''',
    "fake_deco_nocheck": '''@ROUTER.route("PATH", methods=("POST",))
@common.audited
def NAME(request, account_id, SING_id):
    row = store.get("TABLE", SING_id)
    store.put("TABLE", SING_id, dict(row, state="STATE"))
    return {"STATE": SING_id}''',
    "fake_deco_checked": '''@ROUTER.route("PATH", methods=("POST",))
@common.audited
def NAME(request, account_id):
    require_owner(request, account_id)
    rows = store.where("TABLE", account_id=account_id)
    return {"updated": len(rows)}''',
    "branch_gap": '''@ROUTER.route("PATH")
def NAME(request, account_id):
    rows = store.where("TABLE", account_id=account_id)
    if request.query.get("format") == "csv":
        require_owner(request, account_id)
        return common.to_csv(rows)
    return {"rows": rows}''',
    "branch_ok": '''@ROUTER.route("PATH")
def NAME(request, account_id):
    require_owner(request, account_id)
    rows = store.where("TABLE", account_id=account_id)
    if request.query.get("format") == "csv":
        return common.to_csv(rows)
    return {"rows": rows}''',
    "dryrun_gap": '''@ROUTER.route("PATH", methods=("POST",))
def NAME(request, account_id, SING_id):
    row = store.get("TABLE", SING_id)
    if request.query.get("dry_run"):
        return {"would_send_to": row["url"]}
    row = common.load_owned(request, account_id, "TABLE", SING_id)
    store.put("jobs", "test-" + SING_id, {"url": row["url"]})
    return {"queued": SING_id}''',
    "admin_ok": '''@ROUTER.route("PATH")
def NAME(request):
    require_role(request, "admin")
    return store.where("TABLE")''',
    "admin_gap": '''@ROUTER.route("PATH", methods=("POST",))
def NAME(request, SING_id):
    row = store.get("TABLE", SING_id)
    store.put("TABLE", SING_id, dict(row, state="STATE"))
    return {"STATE": SING_id}''',
    "admin_deco": '''@ROUTER.route("PATH", methods=("POST",))
@admin_only
def NAME(request, SING_id):
    row = store.get("TABLE", SING_id)
    store.put("TABLE", SING_id, dict(row, state="STATE"))
    return {"STATE": SING_id}''',
    "public_currencies": '''@ROUTER.route("PATH")
def NAME(request):
    return {"currencies": ["IDR", "USD", "EUR", "SGD"]}''',
    "public_status": '''@ROUTER.route("PATH")
def NAME(request):
    return {"ok": True, "version": "2026.11"}''',
    "public_unlisted_gap": '''@ROUTER.route("PATH")
def NAME(request, account_id):
    settings = store.get("settings", account_id)
    return {"language": settings["language"], "payout_account": settings["payout_account"]}''',
    "update_settings_ok": '''@ROUTER.route("PATH", methods=("PATCH",))
def NAME(request, account_id):
    require_owner(request, account_id)
    settings = store.get("settings", account_id)
    settings.update(request.body)
    store.put("settings", account_id, settings)
    return settings''',
    "add_nocheck": '''def NAME(request, account_id):
    row = dict(request.body, id=common.new_id("TABLE"), account_id=account_id)
    store.put("TABLE", row["id"], row)
    return row''',
    "add_list_ok": '''def NAME(request, account_id):
    require_owner(request, account_id)
    return store.where("TABLE", account_id=account_id)''',
    "add_get_ok": '''def NAME(request, account_id, SING_id):
    return common.load_owned(request, account_id, "TABLE", SING_id)''',
    "add_delete_ok": '''def NAME(request, account_id, SING_id):
    row = common.load_owned(request, account_id, "TABLE", SING_id)
    store.delete("TABLE", row["id"])
    return {"deleted": SING_id}''',
    "add_export_gap": '''def NAME(request, account_id):
    return dict(store.get("settings", account_id))''',
}

# (module, imports, router lines, handlers). A handler is (template, name, router, path,
# singular, table, state, method for router.add registration or None). The verdicts are in
# orchestration-rubric.md.
XL_MODULES = [
    ("budgets", "require_owner", ['router = Router("/accounts/{account_id}/budgets")'], [
        ("list", "list_budgets", "router", "", "", "budgets", "", None),
        ("get_norowcheck", "get_budget", "router", "/{budget_id}", "budget", "budgets", "", None),
        ("create", "create_budget", "router", "", "", "budgets", "", None),
        ("delete_helper", "delete_budget", "router", "/{budget_id}", "budget", "budgets", "", None),
    ]),
    ("cards", "", ['router = common.owner_router("/accounts/{account_id}/cards")'], [
        ("list_guarded", "list_cards", "router", "", "", "cards", "", None),
        ("change_guarded_row", "freeze_card", "router", "/{card_id}/freeze", "card", "cards", "frozen", None),
        ("get_guarded_norow", "get_card_number", "router", "/{card_id}/number", "card", "cards", "", None),
        ("create_guarded", "issue_card", "router", "", "", "cards", "", None),
    ]),
    ("payees", "require_owner", ['router = Router("/accounts/{account_id}/payees")',
                                 'by_id = Router("/payees")'], [
        ("list", "list_payees", "router", "", "", "payees", "", None),
        ("create_nocheck", "create_payee", "router", "", "", "payees", "", None),
        ("update_byid_ok", "update_payee", "by_id", "/{payee_id}", "payee", "payees", "", None),
        ("delete_after", "delete_payee", "router", "/{payee_id}", "payee", "payees", "", None),
    ]),
    ("subscriptions", "owner_only, require_owner",
     ['router = Router("/accounts/{account_id}/subscriptions")', 'by_id = Router("/subscriptions")'], [
        ("list_deco", "list_subscriptions", "router", "", "", "subscriptions", "", None),
        ("change_helper", "cancel_subscription", "router", "/{subscription_id}/cancel", "subscription",
         "subscriptions", "cancelled", None),
        ("update_byid_wrong", "update_subscription", "by_id", "/{subscription_id}", "subscription",
         "subscriptions", "", None),
        ("fake_deco_nocheck", "renew_subscription", "router", "/{subscription_id}/renew", "subscription",
         "subscriptions", "renewed", None),
    ]),
    ("taxes", "require_owner", ['router = Router("/accounts/{account_id}/taxes")'], [
        ("branch_gap", "tax_summary", "router", "/summary", "", "tax_documents", "", None),
        ("list", "list_tax_documents", "router", "/documents", "", "tax_documents", "", None),
        ("create", "upload_tax_document", "router", "/documents", "", "tax_documents", "", None),
        ("branch_ok", "tax_estimate", "router", "/estimate", "", "tax_documents", "", None),
    ]),
    ("receipts", "require_owner", ['router = Router("/accounts/{account_id}/receipts")'], [
        ("add_nocheck", "attach_receipt", "router", "", "", "receipts", "", "POST"),
        ("add_list_ok", "list_receipts", "router", "", "", "receipts", "", "GET"),
        ("add_get_ok", "receipt_image", "router", "/{receipt_id}/image", "receipt", "receipts", "", "GET"),
        ("add_delete_ok", "delete_receipt", "router", "/{receipt_id}", "receipt", "receipts", "", "DELETE"),
    ]),
    ("categories", "owner_only", ['router = Router("/accounts/{account_id}/categories", guard=owner_only)'], [
        ("list_guarded", "list_categories", "router", "", "", "categories", "", None),
        ("create_guarded", "create_category", "router", "", "", "categories", "", None),
        ("change_guarded_row", "archive_category", "router", "/{category_id}/archive", "category",
         "categories", "archived", None),
        ("get_guarded_row", "get_category", "router", "/{category_id}", "category", "categories", "", None),
    ]),
    ("attachments", "require_owner", ['router = Router("/accounts/{account_id}/attachments")',
                                      'by_id = Router("/attachments")'], [
        ("list", "list_attachments", "router", "", "", "attachments", "", None),
        ("byid_nocheck", "download_attachment", "by_id", "/{attachment_id}", "attachment", "attachments",
         "", None),
        ("byid_change_ok", "share_attachment", "by_id", "/{attachment_id}/share", "attachment",
         "attachments", "shared", None),
        ("delete_helper", "delete_attachment", "router", "/{attachment_id}", "attachment", "attachments",
         "", None),
    ]),
    ("tags", "require_owner", ['router = Router("/accounts/{account_id}/tags")'], [
        ("list", "list_tags", "router", "", "", "tags", "", None),
        ("create", "add_tag", "router", "", "", "tags", "", None),
        ("fake_deco_checked", "retag_all", "router", "/retag", "", "tags", "", None),
        ("delete_helper", "remove_tag", "router", "/{tag_id}", "tag", "tags", "", None),
    ]),
    ("approvals", "admin_only, require_role", ['router = Router("/admin/approvals")'], [
        ("admin_ok", "list_pending_approvals", "router", "", "", "approvals", "", None),
        ("admin_gap", "approve_expense", "router", "/{approval_id}/approve", "approval", "approvals",
         "approved", None),
        ("admin_deco", "reject_expense", "router", "/{approval_id}/reject", "approval", "approvals",
         "rejected", None),
        ("admin_ok", "approval_stats", "router", "/stats", "", "approvals", "", None),
    ]),
    ("webhooks", "require_owner", ['router = Router("/accounts/{account_id}/webhooks")'], [
        ("list", "list_webhooks", "router", "", "", "webhooks", "", None),
        ("create", "create_webhook", "router", "", "", "webhooks", "", None),
        ("change_norowcheck", "rotate_webhook_secret", "router", "/{webhook_id}/rotate", "webhook",
         "webhooks", "", None),
        ("dryrun_gap", "test_webhook", "router", "/{webhook_id}/test", "webhook", "webhooks", "", None),
    ]),
    ("settings", "require_owner", ['public = Router("")',
                                   'router = Router("/accounts/{account_id}/settings")'], [
        ("public_currencies", "get_currencies", "public", "/currencies", "", "", "", None),
        ("public_status", "get_status", "public", "/status", "", "", "", None),
        ("public_unlisted_gap", "settings_preview", "public", "/public/accounts/{account_id}/settings",
         "", "", "", None),
        ("update_settings_ok", "update_settings", "router", "", "", "", "", None),
        ("add_export_gap", "export_settings", "router", "/export", "", "", "", "GET"),
    ]),
]

XL_PUBLIC_ROUTES = """\
# Public routes

These routes need no login and no ownership check:

- `GET /health`
- `POST /login`
- `GET /status`
- `GET /currencies`
"""


def xl_files():
    files = {"ledgerly/xl/common.py": XL_COMMON, "docs/security/public-routes.md": XL_PUBLIC_ROUTES}
    registry = []
    for module, auth_names, router_lines, handlers in XL_MODULES:
        imports = ["from ledgerly import store"]
        if auth_names:
            imports.append(f"from ledgerly.auth import {auth_names}")
        imports += ["from ledgerly.framework import Router", "from ledgerly.xl import common"]
        blocks, adds = [], []
        for template, name, router, path, singular, table, state, add_method in handlers:
            code = XL_TEMPLATES[template]
            for token, value in (("NAME", name), ("ROUTER", router), ("PATH", path),
                                 ("SING", singular), ("TABLE", table), ("STATE", state)):
                code = code.replace(token, value)
            blocks.append(code)
            if add_method:
                adds.append(f'{router}.add("{path}", {name}, methods=("{add_method}",))')
        body = "\n".join(imports) + "\n\n" + "\n".join(router_lines) + "\n\n\n" + "\n\n\n".join(blocks)
        if adds:
            body += "\n\n\n# Registered at import time by the service loader.\n" + "\n".join(adds)
        files[f"ledgerly/xl/{module}.py"] = body + "\n"
        registry += [f"{module}.{line.split(' = ')[0]}" for line in router_lines]
    modules = ", ".join(module for module, *_ in XL_MODULES)
    files["ledgerly/xl/__init__.py"] = ""
    files["ledgerly/xl/routers.py"] = (
        f"from ledgerly.xl import {modules}\n\nROUTERS = [\n"
        + "".join(f"    {entry},\n" for entry in registry) + "]\n")
    return files


def write(repo, files):
    for name, text in files.items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")


def git(repo, *args, date=None):
    env = dict(os.environ, **AUTHOR)
    if date:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date
    run = subprocess.run(["git", "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false",
                          *args], cwd=repo, env=env, capture_output=True, text=True)
    if run.returncode:
        sys.exit(f"git {' '.join(args)} failed: {run.stderr}")
    return run.stdout.strip()


def commit(repo, message, date):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message, date=date)
    return git(repo, "rev-parse", "--short", "HEAD")


def main():
    if len(sys.argv) != 3 or sys.argv[2] not in ("S1", "S2", "S3", "S4"):
        sys.exit("usage: python -I build_orchestration_fixture.py RUN_DIR S1|S2|S3|S4")
    run_dir, scenario = Path(sys.argv[1]).resolve(), sys.argv[2]
    repo = run_dir / "ledgerly"
    if repo.exists():
        sys.exit(f"{repo} exists")
    repo.mkdir(parents=True)
    (run_dir / "out").mkdir(exist_ok=True)
    git(repo, "init", "-q", "-b", "main")
    write(repo, FILES_BASE)
    commit(repo, "Initial ledgerly app", "2026-11-20T09:00:00+07:00")
    write(repo, {"ledgerly/billing/invoices.py": INVOICES_HEAD + VOID_BEFORE + INVOICES_TAIL})
    billing = commit(repo, "billing: invoice handlers", "2026-11-21T10:00:00+07:00")
    if scenario == "S2":
        write(repo, {"docs/exec-plans/active/billing-audit.md": CHECKPOINT.format(sha=billing)})
        commit(repo, "docs: billing audit checkpoint", "2026-11-24T16:30:00+07:00")
    write(repo, {"ledgerly/billing/invoices.py": INVOICES_HEAD + VOID_AFTER + INVOICES_TAIL})
    head = commit(repo, "billing: let finance staff void invoices", "2026-11-25T11:15:00+07:00")
    if scenario == "S4":
        write(repo, xl_files())
        head = commit(repo, "xl: twelve account services", "2026-11-26T09:30:00+07:00")
    print(f"{scenario}: {repo} at {head} (billing commit {billing})")


if __name__ == "__main__":
    main()
