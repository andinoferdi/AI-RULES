import json
from datetime import date
from pathlib import Path

from invoicekit.models import Invoice

DATA = Path(__file__).resolve().parent.parent / "data" / "invoices.json"


def load(path=DATA):
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        Invoice(r["number"], r["customer"], date.fromisoformat(r["issued"]), r["kind"], r["amount_idr"])
        for r in rows
    ]
