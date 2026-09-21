from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from ai_rules.domain.errors import ValidationError
from ai_rules.domain.models import reject_secret_keys


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    reject_secret_keys(data, str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(data, indent=2, sort_keys=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(encoded + "\n", encoding="utf-8")
    os.replace(temporary, path)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValidationError(f"state file does not exist: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValidationError(f"state file must contain an object: {path}")
    reject_secret_keys(data, str(path))
    return data


def write_profile(path: Path, profile_id: str, hosts: tuple[str, ...], capabilities: tuple[str, ...], scope: str) -> None:
    atomic_write_json(
        path,
        {
            "schema_version": 1,
            "profile": profile_id,
            "hosts": list(hosts),
            "scope": scope,
            "capabilities": list(capabilities),
        },
    )


def write_lock(path: Path, lock_data: dict[str, Any]) -> None:
    payload = {"schema_version": 1, **lock_data}
    atomic_write_json(path, payload)
