from __future__ import annotations

import json
import re
from dataclasses import replace
from pathlib import Path

from ai_rules.domain.models import InstallationPlan, Operation
from ai_rules.domain.statuses import ReconciliationAction, ReconciliationAssessment, Scope, TargetStatus


def invocation_path(adapter, scope: Scope, identifier: str, project_root=None) -> Path | None:
    if adapter.id == "opencode":
        root = project_root / ".opencode/commands" if scope == Scope.PROJECT else adapter.home / ".config/opencode/commands"
    elif adapter.id == "antigravity-ide":
        root = project_root / ".agents/workflows" if scope == Scope.PROJECT else adapter.home / ".gemini/config/workflows"
    else:
        return None
    return root / f"{identifier}.md"


def invocation_ready(path: Path | None) -> bool:
    if path is None:
        return True
    if not path.is_file():
        return False
    body = path.read_text(encoding="utf-8-sig")
    return bool(re.match(r"\A---\r?\n[\s\S]*?\r?\n---\r?\n\s*\S", body)
                and re.search(r"^description:\s*\S", body, re.M))


def invocation_paths(adapter, scope, identifier, project_root=None):
    primary = invocation_path(adapter, scope, identifier, project_root)
    if primary is None:
        return ()
    if adapter.id == "antigravity-ide" and scope == Scope.GLOBAL:
        return (primary, adapter.home / ".gemini/antigravity/global_workflows" / f"{identifier}.md")
    return (primary,)


def install_invocation(adapter, scope: Scope, identifier: str, project_root=None) -> Path | None:
    paths = invocation_paths(adapter, scope, identifier, project_root)
    for path in paths:
        _install_file(adapter, scope, identifier, project_root, path)
    return paths[0] if paths else None


def _install_file(adapter, scope, identifier, project_root, path):
    if path is None:
        return None
    if path.exists():
        if not invocation_ready(path):
            raise ValueError(f"Existing invocation file is invalid; preserved: {path}")
        return path
    skill = adapter.skill_target(scope, project_root) / identifier / "SKILL.md"
    if not skill.is_file():
        raise ValueError(f"Cannot register invocation without installed skill: {skill}")
    description = json.dumps(f"Use the {identifier} skill", ensure_ascii=False)
    body = (f"---\ndescription: {description}\n---\n\n"
            f"Read `{skill.as_posix()}` and follow the {identifier} skill. "
            "Resolve its references relative to the skill directory.\n")
    if adapter.id == "opencode":
        body += "\nUser request: $ARGUMENTS\n"
    else:
        body += "\nApply the skill to the user's request in this conversation.\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(body)
    except FileExistsError:
        if not invocation_ready(path):
            raise ValueError(f"Invocation file changed during setup; preserved: {path}")
    return path


def reconcile_invocations(plan, catalog, adapters, project_root=None):
    targets = []
    for target in plan.targets:
        if (catalog.require_capability(target.capability_id).ownership.value != "FIRST_PARTY"
                or target.action in {ReconciliationAction.BLOCK, ReconciliationAction.MANUAL_ACTION}):
            targets.append(target)
            continue
        paths = invocation_paths(adapters[target.host_id], target.scope, target.capability_id, project_root)
        invalid = next((path for path in paths if path.exists() and not invocation_ready(path)), None)
        missing = next((path for path in paths if not invocation_ready(path)), None)
        if invalid is not None:
            target = replace(target, action=ReconciliationAction.BLOCK, status=TargetStatus.BLOCKED,
                             reason=f"Existing invocation file is invalid; preserved: {invalid}", operations=())
        elif missing is not None and target.action == ReconciliationAction.NO_OP:
            path = missing
            reason = f"register missing /{target.capability_id} invocation: {path}"
            target = replace(target, action=ReconciliationAction.RECONFIGURE, status=TargetStatus.PLANNED,
                             assessment=ReconciliationAssessment.RECONFIGURE_REQUIRED, reason=reason,
                             operations=(Operation(kind="register_skill_invocation", capability_id=target.capability_id,
                                                   host_id=target.host_id, scope=target.scope,
                                                   action=ReconciliationAction.RECONFIGURE, target=str(path),
                                                   source="installed-skill", reason=reason, reversible=True),))
        targets.append(target)
    return InstallationPlan(plan.schema_version, plan.profile_id, tuple(targets))
