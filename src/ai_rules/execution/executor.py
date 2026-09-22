from __future__ import annotations

import json
import hashlib
import shutil
import subprocess
import uuid
from datetime import datetime, timezone
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

from ai_rules.domain.models import InstallationPlan, Operation
from ai_rules.domain.statuses import ReconciliationAction
from ai_rules.evidence.redaction import redact


@dataclass(frozen=True)
class OperationResult:
    capability_id: str
    host_id: str
    action: str
    status: str
    message: str


@dataclass(frozen=True)
class ExecutionResult:
    dry_run: bool
    results: tuple[OperationResult, ...]


class Executor:
    def __init__(
        self,
        state_dir: Path,
        first_party_bundles: dict[str, Path] | None = None,
        host_skill_roots: dict[str, Path] | None = None,
    ):
        self.state_dir = state_dir
        self.first_party_bundles = first_party_bundles or {}
        self.host_skill_roots = host_skill_roots or {}

    def execute(self, plan: InstallationPlan, dry_run: bool = True, yes: bool = False) -> ExecutionResult:
        results: list[OperationResult] = []
        for target in plan.targets:
            if target.action == ReconciliationAction.BLOCK:
                results.append(
                    OperationResult(target.capability_id, target.host_id, target.action.value, "SKIPPED", target.reason)
                )
                continue
            if target.action == ReconciliationAction.NO_OP:
                results.append(OperationResult(target.capability_id, target.host_id, target.action.value, "VERIFIED", target.reason))
                continue
            if target.action == ReconciliationAction.MANUAL_ACTION:
                results.append(
                    OperationResult(target.capability_id, target.host_id, target.action.value, "MANUAL_ACTION_REQUIRED", target.reason)
                )
                continue
            for operation in target.operations:
                try:
                    results.append(self._execute_operation(operation, dry_run=dry_run, yes=yes))
                except Exception as exc:
                    results.append(
                        OperationResult(
                            operation.capability_id,
                            operation.host_id,
                            operation.action.value,
                            "FAILED",
                            str(exc),
                        )
                    )
        return ExecutionResult(dry_run=dry_run, results=tuple(results))

    def _execute_operation(self, operation: Operation, dry_run: bool, yes: bool) -> OperationResult:
        if dry_run:
            return OperationResult(operation.capability_id, operation.host_id, operation.action.value, "PLANNED", operation.reason)
        if not yes:
            return OperationResult(operation.capability_id, operation.host_id, operation.action.value, "BLOCKED", "confirmation required")
        if operation.kind == "run_command":
            if not operation.argv:
                raise ValueError("external command operation is missing argv")
            completed = subprocess.run(operation.argv, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if completed.returncode:
                detail = (completed.stderr or completed.stdout).strip()
                raise RuntimeError(f"command exited {completed.returncode}: {detail}")
        installed_path = None if operation.action == ReconciliationAction.ADOPT else self._install_first_party_bundle(operation)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        evidence_path = self.state_dir / "last-operation.json"
        payload = asdict(operation)
        if installed_path is not None:
            payload["installed_path"] = str(installed_path)
        evidence_path.write_text(redact(json.dumps(payload, indent=2, default=str)), encoding="utf-8")
        message = f"installed {installed_path}; recorded {evidence_path}" if installed_path else f"recorded {evidence_path}"
        return OperationResult(operation.capability_id, operation.host_id, operation.action.value, "APPLIED", message)

    def _install_first_party_bundle(self, operation: Operation) -> Path | None:
        bundle = self.first_party_bundles.get(operation.capability_id)
        skill_root = self.host_skill_roots.get(operation.host_id)
        if bundle is None or skill_root is None:
            return None
        if not (bundle / "SKILL.md").is_file():
            raise ValueError(f"first-party bundle is missing SKILL.md: {bundle}")
        target = skill_root / operation.capability_id
        copy_tree_atomic(bundle, target, self.state_dir / "backups")
        return target


def tree_identity(root: Path) -> str:
    """Return a deterministic digest of every regular file in a bundle tree."""
    if not root.is_dir():
        raise ValueError(f"bundle tree is not a directory: {root}")
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise ValueError(f"bundle tree contains unsupported symlink: {relative}")
        if path.is_dir():
            digest.update(f"D\0{relative}\0".encode("utf-8"))
            continue
        if not path.is_file():
            raise ValueError(f"bundle tree contains unsupported entry: {relative}")
        digest.update(f"F\0{relative}\0".encode("utf-8"))
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    return digest.hexdigest()


def copy_tree_atomic(
    source: Path,
    target: Path,
    backup_dir: Path | None = None,
    verify: Callable[[Path], bool] | None = None,
) -> None:
    """Stage, back up, replace, and verify a directory with rollback on failure."""
    verify = verify or _is_valid_skill_tree
    if not verify(source):
        raise ValueError(f"source bundle verification failed: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    token = f"{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}"
    temporary = target.with_name(f".{target.name}.staged-{token}")
    previous = target.with_name(f".{target.name}.previous-{token}")
    try:
        shutil.copytree(source, temporary)
        if not verify(temporary):
            raise RuntimeError(f"staged bundle verification failed: {temporary}")
        if not target.exists():
            temporary.replace(target)
            if not verify(target):
                raise RuntimeError(f"installed bundle verification failed: {target}")
            return
        if backup_dir is None:
            raise ValueError("backup directory is required when replacing an existing target")
        backup = backup_dir / token / target.name
        backup.parent.mkdir(parents=True, exist_ok=False)
        shutil.copytree(target, backup)
        (backup.parent / "transaction.json").write_text(
            json.dumps({"transaction_id": token, "target": str(target), "backup": str(backup)}, indent=2),
            encoding="utf-8",
        )
        target.replace(previous)
        temporary.replace(target)
        if not verify(target):
            raise RuntimeError(f"installed bundle verification failed: {target}")
        shutil.rmtree(previous)
    except Exception as exc:
        if previous.exists():
            if target.exists():
                shutil.rmtree(target)
            previous.replace(target)
            raise RuntimeError(f"replacement failed and was rolled back: {exc}") from exc
        raise
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def _is_valid_skill_tree(path: Path) -> bool:
    return (path / "SKILL.md").is_file()
