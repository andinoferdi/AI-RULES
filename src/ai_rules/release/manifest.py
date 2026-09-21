from __future__ import annotations

import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_release_manifest(output_path: Path, first_party: dict[str, str], assets: dict[str, Path] | None = None) -> None:
    payload = {
        "schema_version": 1,
        "first_party": first_party,
        "assets": {name: {"path": str(path), "sha256": sha256_file(path)} for name, path in (assets or {}).items()},
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
