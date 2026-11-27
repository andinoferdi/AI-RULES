from . import store


def membership(user_id: str | None, tenant_id: str) -> dict | None:
    """Return the user record when the user belongs to the tenant, else None."""
    if user_id is None:
        return None
    record = store.user(user_id)
    if record is None or record["tenant_id"] != tenant_id:
        return None
    return record


def is_manager(record: dict | None) -> bool:
    return record is not None and record["role"] in ("owner", "admin")
