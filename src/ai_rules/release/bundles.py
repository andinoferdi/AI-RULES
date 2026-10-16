from __future__ import annotations

import subprocess
import re
import stat
import zipfile
from importlib import resources
from pathlib import Path, PurePosixPath

from ai_rules.domain.errors import ValidationError
from ai_rules.execution import copy_tree_atomic


def packaged_bundle(capability_id: str) -> Path | None:
    """Return an embedded release bundle when the executable ships one.

    Source-mode intentionally returns ``None`` until the release builder stages
    bundles.  That keeps Git acquisition a developer-mode fallback rather than
    a fresh-machine runtime dependency.
    """
    candidate = resources.files("ai_rules.release.data").joinpath("bundles", capability_id)
    try:
        path = Path(str(candidate))
    except TypeError:
        return None
    return path if (path / "SKILL.md").is_file() else None


def validate_subpath(value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise ValidationError("unsafe source subpath")
    parts = value.split('/')
    reserved = re.compile(r'^(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)', re.I)
    if any(part.lower() in ('', '.', '..', '.git') or part.endswith((' ', '.'))
           or reserved.match(part) or any(ord(c) < 32 or c in '<>"|?*' for c in part)
           for part in parts):
        raise ValidationError("unsafe source subpath")
    return value


def export_git_ref(ref: str, destination: Path, repo_root: Path | None = None,
                   subpath: str | None = None) -> None:
    subpath = validate_subpath(subpath)
    tree_ref = f"{ref}:{subpath}" if subpath else ref
    destination.mkdir(parents=True, exist_ok=True)
    archive_path = destination.with_suffix(".zip")
    completed = subprocess.run(
        ["git", "-c", "core.autocrlf=false", "-c", "core.eol=lf",
         "archive", "--format=zip", f"--output={archive_path}", tree_ref],
        cwd=repo_root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise ValidationError(f"failed to archive {ref}: {completed.stderr.strip()}")
    with zipfile.ZipFile(archive_path) as archive:
        for entry in archive.infolist():
            validate_subpath(entry.filename.rstrip('/'))
            mode = entry.external_attr >> 16
            if mode and stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR):
                raise ValidationError(f"non-regular source entry: {entry.filename}")
            if PurePosixPath(entry.filename).is_absolute():
                raise ValidationError("unsafe archive path")
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
