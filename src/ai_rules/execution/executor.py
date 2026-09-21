from __future__ import annotations

import json
import shutil
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
    def __init__(self, state_dir: Path):
        self.state_dir = state_dir

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
                results.append(self._execute_operation(operation, dry_run=dry_run, yes=yes))
        return ExecutionResult(dry_run=dry_run, results=tuple(results))

    def _execute_operation(self, operation: Operation, dry_run: bool, yes: bool) -> OperationResult:
        if dry_run:
            return OperationResult(operation.capability_id, operation.host_id, operation.action.value, "PLANNED", operation.reason)
        if not yes:
            return OperationResult(operation.capability_id, operation.host_id, operation.action.value, "BLOCKED", "confirmation required")
        self.state_dir.mkdir(parents=True, exist_ok=True)
        evidence_path = self.state_dir / "last-operation.json"
        payload = asdict(operation)
        evidence_path.write_text(redact(json.dumps(payload, indent=2, default=str)), encoding="utf-8")
        return OperationResult(operation.capability_id, operation.host_id, operation.action.value, "APPLIED", f"recorded {evidence_path}")


def copy_tree_atomic(source: Path, target: Path, backup_dir: Path | None = None) -> None:
    if target.exists() and backup_dir:
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(target, backup_dir / target.name, dirs_exist_ok=True)
    temporary = target.with_name(f".{target.name}.tmp")
    if temporary.exists():
        shutil.rmtree(temporary)
    shutil.copytree(source, temporary)
    if target.exists():
        shutil.rmtree(target)
    temporary.replace(target)
