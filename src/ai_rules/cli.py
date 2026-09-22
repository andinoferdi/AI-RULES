from __future__ import annotations

import argparse
import json
import subprocess
import sys
from importlib import resources
from pathlib import Path
from typing import Callable

from ai_rules.capabilities.adapters import StaticCapabilityAdapter
from ai_rules.catalog import load_catalog
from ai_rules.domain.models import ActualState, InstallationPlan
from ai_rules.domain.statuses import InstalledOwnership, ReconciliationAction, Scope, TargetStatus
from ai_rules.execution import Executor
from ai_rules.hosts.adapters import build_host_adapters
from ai_rules.interactive import prompt_confirmation, prompt_selection
from ai_rules.planning import render_plan
from ai_rules.platform import detect_environment, project_state_root, state_root
from ai_rules.profiles import load_profiles
from ai_rules.release import export_git_ref, packaged_bundle
from ai_rules.resolver import ResolveRequest, build_resolver
from ai_rules.state import atomic_write_json, create_snapshot, read_json, read_snapshot, write_profile
from ai_rules.verification import doctor_from_plan, render_doctor


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:  # pragma: no cover - CLI boundary
        print(f"ai-rules: {exc}", file=sys.stderr)
        return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-rules")
    sub = parser.add_subparsers(required=True)

    setup = sub.add_parser("setup")
    add_common_setup_flags(setup)
    setup.set_defaults(func=cmd_setup)

    add = sub.add_parser("add")
    add_common_setup_flags(add)
    add.set_defaults(func=cmd_add)

    remove = sub.add_parser("remove")
    add_common_setup_flags(remove)
    remove.set_defaults(func=cmd_remove)

    doctor = sub.add_parser("doctor")
    add_common_setup_flags(doctor)
    doctor.add_argument("--repair", action="store_true")
    doctor.set_defaults(func=cmd_doctor)

    update = sub.add_parser("update")
    add_common_setup_flags(update)
    update.set_defaults(func=cmd_update)

    snapshot = sub.add_parser("snapshot")
    snapshot.add_argument("--profile-path", type=Path, default=state_root() / "profile.json")
    snapshot.add_argument("--lock-path", type=Path, default=state_root() / "lock.json")
    snapshot.add_argument("--output", type=Path, required=True)
    snapshot.add_argument("--locked", action="store_true")
    snapshot.set_defaults(func=cmd_snapshot)

    restore = sub.add_parser("restore")
    restore.add_argument("snapshot", type=Path)
    restore.add_argument("--dry-run", action="store_true")
    restore.add_argument("--yes", action="store_true")
    restore.add_argument("--state-dir", type=Path, default=state_root())
    restore.add_argument("--project-root", type=Path)
    restore.set_defaults(func=cmd_restore)
    return parser


def add_common_setup_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--host", action="append", dest="hosts", default=[])
    parser.add_argument("--profile", default="minimal")
    parser.add_argument("--capability", action="append", dest="capabilities", default=[])
    parser.add_argument("--scope", choices=[item.value for item in Scope], default=Scope.GLOBAL.value)
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--non-interactive", action="store_true")
    parser.add_argument("--state-dir", type=Path)


def cmd_setup(args: argparse.Namespace) -> int:
    _prepare_args(args)
    interactive = False
    if not args.non_interactive and not args.hosts and not args.capabilities and args.profile == "minimal":
        catalog = load_catalog()
        profiles = load_profiles(catalog)
        selection = prompt_selection(
            host_ids=tuple(catalog.hosts),
            profile_ids=tuple(profiles.profiles),
            capability_ids=tuple(catalog.capabilities),
        )
        if selection is None:
            print("setup cancelled; no changes made")
            return 0
        args.hosts = list(selection.hosts)
        args.profile = selection.profile_id or "custom"
        args.capabilities = list(selection.capabilities)
        interactive = True
    plan = _resolve_from_args(args)
    print(_preflight_text())
    print(render_plan(plan))
    if args.dry_run:
        return 1 if plan.blocked else 0
    if interactive and not args.yes and not prompt_confirmation():
        print("setup cancelled; no changes made")
        return 0
    if interactive:
        args.yes = True
    result = _executor_for_plan(plan, args).execute(plan, dry_run=False, yes=args.yes)
    for item in result.results:
        print(f"{item.capability_id} -> {item.host_id}: {item.status} {item.action} - {item.message}")
    if not args.yes:
        return 0
    _record_managed_installations(plan, result, args)
    capabilities = tuple(args.capabilities) if args.capabilities else tuple(_profile_capabilities(args.profile))
    write_profile(args.state_dir / "profile.json", args.profile, tuple(_hosts(args.hosts)), capabilities, args.scope)
    _write_verified_lock(plan, result, args)
    return 1 if any(item.status in {"FAILED", "SKIPPED", "BLOCKED"} for item in result.results) else 0


def cmd_add(args: argparse.Namespace) -> int:
    """Reconcile explicitly selected capabilities and merge them into desired state."""
    _prepare_args(args)
    if not args.capabilities:
        raise ValueError("add requires at least one --capability")
    profile_path = args.state_dir / "profile.json"
    existing = read_json(profile_path) if profile_path.exists() else {}
    merged = tuple(dict.fromkeys((*existing.get("capabilities", ()), *args.capabilities)))
    args.capabilities = list(merged)
    if not args.hosts:
        args.hosts = list(existing.get("hosts", ()))
    args.profile = "custom"
    result = cmd_setup(args)
    if result or args.dry_run or not args.yes:
        return result
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    """Remove only installer-managed first-party targets, preserving unmanaged paths."""
    _prepare_args(args)
    if not args.capabilities:
        raise ValueError("remove requires at least one --capability")
    records = _managed_installation_records(args.state_dir)
    catalog = load_catalog()
    adapters = build_host_adapters(catalog.hosts)
    removed = 0
    for host_id in _hosts(args.hosts):
        root = adapters[host_id].skill_target(Scope(args.scope), args.project_root)
        for capability_id in args.capabilities:
            key = _installation_key(capability_id, host_id, Scope(args.scope))
            record = records.get(key)
            if record is None:
                print(f"{capability_id} -> {host_id}: BLOCKED unmanaged target is preserved")
                continue
            if args.dry_run or not args.yes:
                print(f"{capability_id} -> {host_id}: PREVIEW REMOVE {record.get('path', '')}")
                continue
            path = Path(record["path"]) if record.get("path") else (root / capability_id if root else None)
            if path is not None and path.exists():
                import shutil
                shutil.rmtree(path)
            records.pop(key, None)
            removed += 1
            print(f"{capability_id} -> {host_id}: APPLIED REMOVE")
    if args.dry_run or not args.yes:
        return 0
    atomic_write_json(args.state_dir / "managed-installations.json", {"schema_version": 1, "installations": records})
    if removed:
        profile_path = args.state_dir / "profile.json"
        if profile_path.exists():
            profile = read_json(profile_path)
            remaining = tuple(item for item in profile.get("capabilities", ()) if item not in set(args.capabilities))
            write_profile(profile_path, profile.get("profile", "custom"), tuple(profile.get("hosts", ())), remaining, profile.get("scope", args.scope))
    return 0 if removed or args.dry_run or not args.yes else 1


def cmd_doctor(args: argparse.Namespace) -> int:
    _prepare_args(args)
    plan = _resolve_from_args(args)
    report = doctor_from_plan(plan)
    print(render_doctor(report))
    if args.repair:
        print("doctor --repair uses the same locked target and does not upgrade versions")
        if args.dry_run or not args.yes:
            print("repair dry-run/preview only; pass --yes without --dry-run to apply safe repairs")
        else:
            repair_plan = _repair_only_plan(plan)
            result = _executor_for_plan(repair_plan, args).execute(repair_plan, dry_run=False, yes=True)
            for item in result.results:
                print(f"{item.capability_id} -> {item.host_id}: {item.status} {item.action} - {item.message}")
            _record_managed_installations(repair_plan, result, args)
    return 0 if report.healthy and not plan.blocked else 1


def cmd_update(args: argparse.Namespace) -> int:
    _prepare_args(args)
    plan = _resolve_from_args(args)
    print("AI-RULES update preview")
    print(render_plan(plan))
    if args.dry_run or not args.yes:
        return 1 if plan.blocked else 0
    result = _executor_for_plan(plan, args).execute(plan, dry_run=False, yes=True)
    for item in result.results:
        print(f"{item.capability_id} -> {item.host_id}: {item.status} {item.action} - {item.message}")
    _record_managed_installations(plan, result, args)
    _write_verified_lock(plan, result, args)
    return 1 if any(item.status in {"FAILED", "SKIPPED", "BLOCKED"} for item in result.results) else 0


def cmd_snapshot(args: argparse.Namespace) -> int:
    create_snapshot(args.profile_path, args.lock_path, args.output, locked=args.locked)
    print(f"snapshot written: {args.output}")
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    snapshot = read_snapshot(args.snapshot)
    profile = snapshot.get("profile", {})
    print("AI-RULES restore preview")
    print(f"profile={profile.get('profile')} hosts={profile.get('hosts', [])} capabilities={profile.get('capabilities', [])}")
    catalog = load_catalog()
    for host_id in profile.get("hosts", []):
        if host_id not in catalog.hosts:
            print(f"incompatible host: {host_id}")
    for capability_id in profile.get("capabilities", []):
        if capability_id not in catalog.capabilities:
            print(f"incompatible capability: {capability_id}")
    incompatible = any(host_id not in catalog.hosts for host_id in profile.get("hosts", ())) or any(
        capability_id not in catalog.capabilities for capability_id in profile.get("capabilities", ())
    )
    if incompatible:
        return 1 if args.yes and not args.dry_run else 0
    if args.dry_run or not args.yes:
        print("restore preview only; pass --yes without --dry-run to reconcile the snapshot")
        return 0
    restore_args = argparse.Namespace(
        hosts=list(profile.get("hosts", ())),
        profile=profile.get("profile", "custom"),
        capabilities=list(profile.get("capabilities", ())),
        scope=profile.get("scope", Scope.GLOBAL.value),
        project_root=args.project_root,
        dry_run=False,
        yes=True,
        non_interactive=True,
        state_dir=args.state_dir,
    )
    return cmd_setup(restore_args)


def _resolve_from_args(args: argparse.Namespace):
    catalog = load_catalog()
    profiles = load_profiles(catalog)
    resolver = build_resolver(catalog, profiles, StaticCapabilityAdapter(state=_actual_state(catalog, args)))
    hosts = tuple(_hosts(args.hosts))
    profile_id = None if args.capabilities else args.profile
    return resolver.resolve(
        ResolveRequest(
            hosts=hosts,
            scope=Scope(args.scope),
            profile_id=profile_id,
            capabilities=tuple(args.capabilities),
        )
    )


def _prepare_args(args: argparse.Namespace) -> None:
    """Resolve state location and reject a project mutation without its root."""
    scope = Scope(args.scope)
    if scope == Scope.PROJECT and args.project_root is None:
        raise ValueError("--project-root is required for project scope")
    if args.state_dir is None:
        args.state_dir = project_state_root(args.project_root) if scope == Scope.PROJECT else state_root()


def _hosts(hosts: list[str]) -> list[str]:
    return hosts or ["codex"]


def _profile_capabilities(profile_id: str) -> list[str]:
    catalog = load_catalog()
    profiles = load_profiles(catalog)
    return list(profiles.require(profile_id).capabilities)


def _executor_for_plan(plan, args: argparse.Namespace) -> Executor:
    catalog = load_catalog()
    adapters = build_host_adapters(catalog.hosts)
    roots: dict[str, Path] = {}
    bundles: dict[str, Path] = {}
    manifest = _release_manifest()
    for target in plan.targets:
        host_root = adapters[target.host_id].skill_target(target.scope, args.project_root)
        if host_root is not None:
            roots[target.host_id] = host_root
        capability = catalog.require_capability(target.capability_id)
        release = manifest.get("first_party", {}).get(capability.id)
        if release is None:
            continue
        bundle = packaged_bundle(capability.id)
        if bundle is None:
            bundle = args.state_dir / "bundles" / capability.id
            export_git_ref(release["commit"], bundle, repo_root=Path.cwd())
        bundles[capability.id] = bundle
    return Executor(args.state_dir, first_party_bundles=bundles, host_skill_roots=roots)


def _actual_state(
    catalog,
    args: argparse.Namespace,
    external_probe: Callable[[str, str], bool] | None = None,
) -> dict[tuple[str, str, str], ActualState]:
    records = _managed_installation_records(args.state_dir)
    adapters = build_host_adapters(catalog.hosts)
    result: dict[tuple[str, str, str], ActualState] = {}
    scope = Scope(args.scope)
    probe = external_probe or _external_config_present
    for host_id in _hosts(args.hosts):
        adapter = adapters[host_id]
        root = adapter.skill_target(scope, args.project_root)
        if root is None:
            continue
        for capability_id in catalog.capabilities:
            capability = catalog.require_capability(capability_id)
            key = _installation_key(capability_id, host_id, scope)
            if capability.ownership.value == "EXTERNAL":
                record = records.get(key)
                present = probe(capability_id, host_id)
                if present:
                    result[(capability_id, host_id, scope.value)] = ActualState(
                        exists=True,
                        ownership=(InstalledOwnership.MANAGED_BY_AI_RULES if record else InstalledOwnership.EXTERNAL_EXISTING),
                        installed_version=record.get("version") if record else None,
                        healthy=record is not None and capability_id != "context7",
                    )
                elif record:
                    result[(capability_id, host_id, scope.value)] = ActualState(
                        exists=True,
                        ownership=InstalledOwnership.MANAGED_BY_AI_RULES,
                        installed_version=record.get("version"),
                        config_drift=True,
                    )
                continue
            target = root / capability_id
            if not target.exists():
                aliases = adapter.skill_discovery_roots(scope, args.project_root)[1:]
                if any((alias / capability_id).exists() for alias in aliases):
                    result[(capability_id, host_id, scope.value)] = ActualState(
                        exists=True, ownership=InstalledOwnership.EXTERNAL_EXISTING
                    )
                elif record := records.get(key):
                    result[(capability_id, host_id, scope.value)] = ActualState(
                        exists=True,
                        ownership=InstalledOwnership.MANAGED_BY_AI_RULES,
                        installed_version=record.get("version"),
                        healthy=False,
                        artifact_drift=True,
                    )
                continue
            record = records.get(key)
            if record is None:
                result[(capability_id, host_id, scope.value)] = ActualState(
                    exists=True, ownership=InstalledOwnership.UNKNOWN_ORIGIN
                )
                continue
            result[(capability_id, host_id, scope.value)] = ActualState(
                exists=True,
                ownership=InstalledOwnership.MANAGED_BY_AI_RULES,
                installed_version=record.get("version"),
                healthy=(target / "SKILL.md").is_file(),
                artifact_drift=not (target / "SKILL.md").is_file(),
            )
    return result


def _external_config_present(capability_id: str, host_id: str) -> bool:
    commands = {
        ("superpowers", "antigravity-cli"): ("agy", "plugin", "list"),
        ("context7", "codex"): ("codex", "mcp", "list"),
        ("context7", "claude-code"): ("claude", "mcp", "list"),
        ("context7", "opencode"): ("opencode", "mcp", "list"),
        ("context7", "antigravity-cli"): ("agy", "mcp", "list"),
    }
    command = commands.get((capability_id, host_id))
    if command is None:
        return False
    try:
        completed = subprocess.run(command, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return completed.returncode == 0 and capability_id.lower() in completed.stdout.lower()


def _record_managed_installations(plan, result, args: argparse.Namespace) -> None:
    records = _managed_installation_records(args.state_dir)
    applied = {(item.capability_id, item.host_id, item.action) for item in result.results if item.status == "APPLIED"}
    catalog = load_catalog()
    adapters = build_host_adapters(catalog.hosts)
    for target in plan.targets:
        if (target.capability_id, target.host_id, target.action.value) not in applied:
            continue
        key = _installation_key(target.capability_id, target.host_id, target.scope)
        if target.capability_id in _release_manifest().get("first_party", {}):
            root = adapters[target.host_id].skill_target(target.scope, args.project_root)
            if root is None:
                continue
            records[key] = {
                "capability": target.capability_id,
                "host": target.host_id,
                "scope": target.scope.value,
                "version": target.target_version,
                "path": str(root / target.capability_id),
                "kind": "first-party-skill",
            }
        else:
            records[key] = {
                "capability": target.capability_id,
                "host": target.host_id,
                "scope": target.scope.value,
                "version": target.target_version,
                "kind": "external-operation",
                "target": next((operation.target for operation in target.operations), target.strategy_id),
            }
    atomic_write_json(args.state_dir / "managed-installations.json", {"schema_version": 1, "installations": records})


def _managed_installation_records(state_dir: Path) -> dict[str, dict]:
    path = state_dir / "managed-installations.json"
    if not path.exists():
        return {}
    return dict(read_json(path).get("installations", {}))


def _write_verified_lock(plan, result, args: argparse.Namespace) -> None:
    """Persist per-target post-execution evidence, never equating APPLIED with verified."""
    if not result.results:
        return
    result_by_key = {(item.capability_id, item.host_id, item.action): item for item in result.results}
    catalog = load_catalog()
    adapters = build_host_adapters(catalog.hosts)
    targets = []
    for target in plan.targets:
        item = result_by_key.get((target.capability_id, target.host_id, target.action.value))
        if item is None:
            targets.append({
                "capability": target.capability_id,
                "host": target.host_id,
                "scope": target.scope.value,
                "status": "SKIPPED",
                "assessment": target.assessment.value,
                "verification": {"outcome": "NOT_RUN", "reason": "operation was not executed"},
            })
            continue
        capability = catalog.require_capability(target.capability_id)
        verification: dict[str, str]
        status = item.status
        if item.status == "APPLIED" and capability.ownership.value == "FIRST_PARTY":
            root = adapters[target.host_id].skill_target(target.scope, args.project_root)
            skill_file = root / target.capability_id / "SKILL.md" if root is not None else None
            if skill_file is not None and skill_file.is_file():
                status = TargetStatus.VERIFIED.value
                verification = {"outcome": "PASS", "check": "artifact", "path": str(skill_file)}
            else:
                status = TargetStatus.FAILED.value
                verification = {"outcome": "FAIL", "check": "artifact", "reason": "installed skill artifact is absent"}
        elif item.status == "APPLIED":
            status = TargetStatus.PARTIALLY_VERIFIED.value
            verification = {"outcome": "NOT_RUN", "reason": "external configuration applied; runtime health requires a separate check"}
        else:
            verification = {"outcome": "NOT_RUN", "reason": item.message}
        targets.append(
            {
                "capability": target.capability_id,
                "host": target.host_id,
                "scope": target.scope.value,
                "action": target.action.value,
                "target_version": target.target_version,
                "assessment": target.assessment.value,
                "status": status,
                "strategy": target.strategy_id,
                "source": next((operation.source for operation in target.operations), None),
                "update_policy": capability.update_policy.model.value,
                "version_observability": capability.update_policy.version_observability.value,
                "exact_replay_supported": capability.update_policy.exact_pin_supported,
                "verification": verification,
            }
        )
    overall = "verified" if targets and all(target["status"] == TargetStatus.VERIFIED.value for target in targets) else "partially_verified"
    atomic_write_json(
        args.state_dir / "lock.json",
        {"schema_version": 2, "status": overall, "profile": plan.profile_id, "targets": targets},
    )


def _installation_key(capability_id: str, host_id: str, scope: Scope) -> str:
    return f"{capability_id}:{host_id}:{scope.value}"


def _repair_only_plan(plan: InstallationPlan) -> InstallationPlan:
    return InstallationPlan(
        schema_version=plan.schema_version,
        profile_id=plan.profile_id,
        targets=tuple(target for target in plan.targets if target.action == ReconciliationAction.REPAIR),
    )


def _release_manifest() -> dict:
    with resources.files("ai_rules.release.data").joinpath("release_manifest.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _preflight_text() -> str:
    env = detect_environment()
    commands = ", ".join(f"{name}={'yes' if present else 'no'}" for name, present in env.commands.items())
    return f"Preflight os={env.os} arch={env.architecture} python={env.python} commands=[{commands}]"
