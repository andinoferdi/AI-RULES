from __future__ import annotations

from pathlib import Path

from ai_rules.domain.models import safe_child_path


def state_root(home: Path | None = None) -> Path:
    return (home or Path.home()) / ".ai-rules"


def backup_root(home: Path | None = None) -> Path:
    return state_root(home) / "backups"


def project_state_root(project_root: Path) -> Path:
    return safe_child_path(project_root, ".ai-rules")
