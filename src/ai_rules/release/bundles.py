from __future__ import annotations

import subprocess
import zipfile
from pathlib import Path

from ai_rules.domain.errors import ValidationError
from ai_rules.execution import copy_tree_atomic


def export_git_ref(ref: str, destination: Path, repo_root: Path | None = None) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    archive_path = destination.with_suffix(".zip")
    completed = subprocess.run(
        ["git", "archive", "--format=zip", f"--output={archive_path}", ref],
        cwd=repo_root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise ValidationError(f"failed to archive {ref}: {completed.stderr.strip()}")
    with zipfile.ZipFile(archive_path) as archive:
        archive.extractall(destination)
    archive_path.unlink(missing_ok=True)
    skill_file = destination / "SKILL.md"
    if not skill_file.exists():
        raise ValidationError(f"exported runtime ref has no SKILL.md: {ref}")


def install_first_party_bundle(bundle_root: Path, target_skill_root: Path, capability_id: str, backup_root: Path | None = None) -> Path:
    if not (bundle_root / "SKILL.md").exists():
        raise ValidationError(f"bundle root is missing SKILL.md: {bundle_root}")
    target = target_skill_root / capability_id
    copy_tree_atomic(bundle_root, target, backup_root)
    return target
