from __future__ import annotations

from pathlib import Path

from .store import atomic_write_json, read_json


def create_snapshot(profile_path: Path, lock_path: Path | None, output_path: Path, locked: bool = False) -> None:
    snapshot = {
        "schema_version": 1,
        "mode": "locked" if locked else "desired",
        "profile": read_json(profile_path),
    }
    if locked and lock_path is not None and lock_path.exists():
        snapshot["lock"] = read_json(lock_path)
    atomic_write_json(output_path, snapshot)


def read_snapshot(snapshot_path: Path) -> dict:
    return read_json(snapshot_path)
