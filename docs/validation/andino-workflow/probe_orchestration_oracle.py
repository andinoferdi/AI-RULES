"""Check the orchestration trial's answer keys by probing every handler of a built fixture.

    python -I probe_orchestration_oracle.py RUN_DIR/ledgerly S1|S4

Calls each handler as a caller who owns account A only: with account B's id, and with account
A's id plus a row of account B. A handler is a GAP when any call returns, or when a blocked call
already changed B's data. Listed public routes are OK by rule. Prints each verdict and the gaps;
the expected result is 7 gaps of 18 for S1 and 14 of 49 for S4 (orchestration-rubric.md).
"""
import copy
import itertools
import re
import sys

repo, scenario = sys.argv[1], sys.argv[2]
sys.path.insert(0, repo)

from ledgerly import store  # noqa: E402
from ledgerly.framework import Forbidden, Request  # noqa: E402

PUBLIC = {"/health", "/login", "/status", "/currencies"}


class User:
    def __init__(self):
        self.id, self.account_id, self.roles = "u1", "A", []


def seed():
    data = {kind: {} for kind in store._DATA}
    for kind in list(data) + ["budgets", "cards", "payees", "subscriptions", "tax_documents",
                              "receipts", "categories", "attachments", "tags", "approvals",
                              "webhooks", "settings"]:
        data.setdefault(kind, {})
        for owner in ("A", "B"):
            data[kind][f"{kind}-{owner}"] = {
                "id": f"{kind}-{owner}", "account_id": owner, "url": f"https://{owner}.example",
                "email": f"{owner}@example", "name": owner, "balance": 1, "members": [],
                "month": "01", "year": "2026", "amount": 1, "language": "id",
                "payout_account": f"acct-{owner}", "state": "open"}
    for owner in ("A", "B"):
        data["accounts"][owner] = dict(data["accounts"][f"accounts-{owner}"], id=owner)
        data["settings"][owner] = dict(data["settings"][f"settings-{owner}"])
        data["users"][f"users-{owner}"]["password_reset_required"] = False
    store._DATA.clear()
    store._DATA.update(data)


def call(handler, params, query):
    request = Request(User(), query=query, body={"name": "x", "id": "new-1"})
    try:
        handler(request, **params)
        return "allowed"
    except (Forbidden, KeyError, TypeError):
        return "blocked"


def verdict(path, handler):
    if path in PUBLIC:
        return "OK(public)"
    names = re.findall(r"{(\w+)}", path)
    row_names = [n for n in names if n not in ("account_id", "month", "year")]
    attacks = []
    if "account_id" in names:
        attacks.append({n: ("B" if n == "account_id" else None) for n in names})
        if row_names:
            attacks.append({n: ("A" if n == "account_id" else None) for n in names})
    else:
        attacks.append({n: None for n in names})
    for template in attacks:
        for query in ({}, {"format": "csv"}, {"dry_run": "1"}):
            seed()
            before = copy.deepcopy(store._DATA)
            params = {}
            for name, value in template.items():
                if value is None:
                    table = {"budget_id": "budgets", "card_id": "cards", "payee_id": "payees",
                             "subscription_id": "subscriptions", "receipt_id": "receipts",
                             "category_id": "categories", "attachment_id": "attachments",
                             "tag_id": "tags", "approval_id": "approvals", "webhook_id": "webhooks",
                             "invoice_id": "invoices", "expense_id": "expenses", "job_id": "jobs",
                             "user_id": "users", "month": None, "year": None}[name]
                    params[name] = f"{table}-B" if table else "01"
                else:
                    params[name] = value
            outcome = call(handler, params, query)
            b_changed = any(
                {k: v for k, v in store._DATA[kind].items() if k.endswith("-B") or k == "B"}
                != {k: v for k, v in before[kind].items() if k.endswith("-B") or k == "B"}
                for kind in store._DATA)
            if outcome == "allowed" or b_changed:
                return f"GAP({outcome}{', B changed' if b_changed else ''}; {params}; {query})"
    return "OK"


if scenario == "S4":
    from ledgerly.xl.routers import ROUTERS
else:
    from ledgerly.routes import accounts, admin, expenses, exports, public, reports
    ROUTERS = [public.router, accounts.router, expenses.account_expenses, expenses.expenses,
               reports.router, admin.router, exports.router]

results = []
for router in ROUTERS:
    for methods, path, handler in router.routes:
        name = getattr(handler, "__name__", "?")
        results.append((handler.__module__.split(".")[-1], name, path, verdict(path, handler)))
for module, name, path, result in results:
    print(f"{module:14} {name:26} {result[:110]}")
gaps = [name for _, name, _, result in results if result.startswith("GAP")]
print(f"\n{len(results)} handlers, {len(gaps)} gaps: {', '.join(gaps)}")
