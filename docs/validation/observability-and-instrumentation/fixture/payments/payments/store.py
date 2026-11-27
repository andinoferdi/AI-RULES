"""Invoice store: var/invoices.json, a dict keyed by invoice id."""
import json

from payments.paths import VAR

INVOICES = VAR / "invoices.json"


def load():
    return json.loads(INVOICES.read_text(encoding="utf-8"))


def save(invoices):
    INVOICES.write_text(json.dumps(invoices, indent=1), encoding="utf-8")
