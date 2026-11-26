"""In-memory development store loaded from data/tenants.json."""
import copy
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "tenants.json"
_state: dict = {}


def reset() -> None:
    _state.clear()
    _state.update(copy.deepcopy(json.loads(DATA.read_text(encoding="utf-8"))))


def user(user_id: str) -> dict | None:
    return _state["users"].get(user_id)


def tenant(tenant_id: str) -> dict | None:
    return _state["tenants"].get(tenant_id)


def invoices(tenant_id: str) -> list[dict]:
    return [inv for inv in _state["invoices"] if inv["tenant_id"] == tenant_id]


reset()
