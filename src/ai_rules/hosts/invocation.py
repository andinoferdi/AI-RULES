from __future__ import annotations

import json
import re
import stat
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


def family_members(adapter, scope: Scope, identifier: str, project_root=None, source_dir=None) -> list[str]:
    if identifier != "andino-workflow":
        return []
    portfolio_file = None
    if source_dir is not None:
        candidate = Path(source_dir) / "references/portfolio.json"
        if candidate.is_file():
            portfolio_file = candidate
    if portfolio_file is None and adapter is not None:
        root = adapter.skill_target(scope, project_root)
        if root is not None:
            candidate = root / "andino-workflow/references/portfolio.json"
            if candidate.is_file():
                portfolio_file = candidate
    if portfolio_file is None:
        from ai_rules.release.bundles import packaged_bundle
        bundle = packaged_bundle("andino-workflow")
        if bundle is not None and (bundle / "references/portfolio.json").is_file():
            portfolio_file = bundle / "references/portfolio.json"
    if portfolio_file is not None:
        try:
            data = json.loads(portfolio_file.read_text(encoding="utf-8"))
            return [f"andino-{name}" for name in data.get("members", [])]
        except (ValueError, OSError):
            pass
    if adapter is not None:
        root = adapter.skill_target(scope, project_root)
        if root is not None:
            return sorted(p.name for p in root.glob("andino-*") if p.is_dir() and p.name != "andino-workflow")
    return []


def family_retired(adapter, scope: Scope, identifier: str, project_root=None, source_dir=None) -> list[str]:
    if identifier != "andino-workflow":
        return []
    portfolio_file = None
    if source_dir is not None:
        candidate = Path(source_dir) / "references/portfolio.json"
        if candidate.is_file():
            portfolio_file = candidate
    if portfolio_file is None and adapter is not None:
        root = adapter.skill_target(scope, project_root)
        if root is not None:
            candidate = root / "andino-workflow/references/portfolio.json"
            if candidate.is_file():
                portfolio_file = candidate
    if portfolio_file is None:
        from ai_rules.release.bundles import packaged_bundle
        bundle = packaged_bundle("andino-workflow")
        if bundle is not None and (bundle / "references/portfolio.json").is_file():
            portfolio_file = bundle / "references/portfolio.json"
    if portfolio_file is not None:
        try:
            data = json.loads(portfolio_file.read_text(encoding="utf-8"))
            return [f"andino-{name}" for name in data.get("retired", [])]
        except (ValueError, OSError):
            pass
    return []


def all_invocation_paths(adapter, scope: Scope, identifier: str, project_root=None, source_dir=None) -> list[Path]:
    paths = list(invocation_paths(adapter, scope, identifier, project_root))
    for member_id in family_members(adapter, scope, identifier, project_root, source_dir):
        paths.extend(invocation_paths(adapter, scope, member_id, project_root))
    return paths


def _prune_legacy_and_retired(adapter, scope: Scope, identifier: str, project_root=None, source_dir=None) -> None:
    if adapter is None:
        return
    if adapter.id == "opencode":
        cmd_dir = project_root / ".opencode/commands" if scope == Scope.PROJECT else adapter.home / ".config/opencode/commands"
        if cmd_dir.is_dir():
            for legacy in cmd_dir.glob("manual-*.md"):
                try:
                    legacy.unlink(missing_ok=True)
                except OSError:
                    pass
            for ret in family_retired(adapter, scope, identifier, project_root, source_dir):
                for path in invocation_paths(adapter, scope, ret, project_root):
                    if path.is_file():
                        try:
                            path.unlink(missing_ok=True)
                        except OSError:
                            pass
    elif adapter.id == "antigravity-ide":
        cmd_dir = project_root / ".agents/workflows" if scope == Scope.PROJECT else adapter.home / ".gemini/config/workflows"
        if cmd_dir.is_dir():
            for legacy in cmd_dir.glob("manual-*.md"):
                try:
                    legacy.unlink(missing_ok=True)
                except OSError:
                    pass
            for ret in family_retired(adapter, scope, identifier, project_root, source_dir):
                for path in invocation_paths(adapter, scope, ret, project_root):
                    if path.is_file():
                        try:
                            path.unlink(missing_ok=True)
                        except OSError:
                            pass
        if scope == Scope.GLOBAL:
            global_dir = adapter.home / ".gemini/antigravity/global_workflows"
            if global_dir.is_dir():
                for legacy in global_dir.glob("manual-*.md"):
                    try:
                        legacy.unlink(missing_ok=True)
                    except OSError:
                        pass
                for ret in family_retired(adapter, scope, identifier, project_root, source_dir):
                    path = global_dir / f"{ret}.md"
                    if path.is_file():
                        try:
                            path.unlink(missing_ok=True)
                        except OSError:
                            pass


def install_invocation(adapter, scope: Scope, identifier: str, project_root=None, source_dir=None) -> Path | None:
    paths = invocation_paths(adapter, scope, identifier, project_root)
    for path in paths:
        _install_file(adapter, scope, identifier, project_root, path)
    if identifier == "andino-workflow":
        for member_id in family_members(adapter, scope, identifier, project_root, source_dir):
            skill_target = adapter.skill_target(scope, project_root) if adapter is not None else None
            if skill_target is not None and not (skill_target / member_id / "SKILL.md").is_file():
                continue
            for path in invocation_paths(adapter, scope, member_id, project_root):
                _install_file(adapter, scope, member_id, project_root, path)
        _prune_legacy_and_retired(adapter, scope, identifier, project_root, source_dir)
    return paths[0] if paths else None


def invocation_body(adapter, scope: Scope, identifier: str, project_root=None) -> str:
    root = adapter.skill_target(scope, project_root) if adapter is not None else None
    skill = root / identifier / "SKILL.md" if root is not None else None
    description = json.dumps(f"Use the {identifier} skill", ensure_ascii=False)
    if skill is not None and skill.is_file():
        try:
            text = skill.read_text(encoding="utf-8-sig")
            fm = re.match(r"\A---\r?\n([\s\S]*?)\r?\n---", text)
            if fm:
                m = re.search(r"^description:\s*(.+)$", fm.group(1), re.MULTILINE)
                if m:
                    val = m.group(1).strip()
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1].strip()
                    if val:
                        description = json.dumps(val, ensure_ascii=False)
        except OSError:
            pass
    posix_path = skill.as_posix() if skill is not None else f"{identifier}/SKILL.md"
    body = (f"---\ndescription: {description}\n---\n\n"
            f"Read `{posix_path}` and follow the {identifier} skill. "
            "Resolve its references relative to the skill directory.\n")
    if adapter is not None and adapter.id == "opencode":
        body += "\nUser request: $ARGUMENTS\n"
    else:
        body += "\nApply the skill to the user's request in this conversation.\n"
    return body


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
    body = invocation_body(adapter, scope, identifier, project_root)
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
        root = adapters[target.host_id].skill_target(target.scope, project_root)
        skill = root / target.capability_id if root is not None else None
        if (target.host_id in {"antigravity-cli", "antigravity-ide"} and skill is not None
                and skill.is_dir()
                and hasattr(stat, "IO_REPARSE_TAG_MOUNT_POINT")
                and getattr(skill.lstat(), "st_reparse_tag", None) == stat.IO_REPARSE_TAG_MOUNT_POINT):
            targets.append(replace(target, action=ReconciliationAction.BLOCK, status=TargetStatus.BLOCKED,
                                   reason=f"Antigravity skill discovery skips this Windows junction: {skill}. "
                                          "Back up the link and replace it with a regular skill directory; "
                                          "preserve its shared source, then rerun setup.", operations=()))
            continue
        paths = all_invocation_paths(adapters[target.host_id], target.scope, target.capability_id, project_root)
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
