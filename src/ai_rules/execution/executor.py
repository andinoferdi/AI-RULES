from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

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
        installed_path = self._install_first_party_bundle(operation)
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


def copy_tree_atomic(source: Path, target: Path, backup_dir: Path | None = None) -> None:
    if target.exists() and backup_dir:
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(target, backup_dir / target.name, dirs_exist_ok=True)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.tmp")
    if temporary.exists():
        shutil.rmtree(temporary)
    shutil.copytree(source, temporary)
    if target.exists():
        shutil.rmtree(target)
    temporary.replace(target)
