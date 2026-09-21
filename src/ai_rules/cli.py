from __future__ import annotations

import argparse
import json
import sys
from importlib import resources
from pathlib import Path

from ai_rules.capabilities.adapters import StaticCapabilityAdapter
from ai_rules.catalog import load_catalog
from ai_rules.domain.models import ActualState, InstallationPlan
from ai_rules.domain.statuses import InstalledOwnership, ReconciliationAction, Scope
from ai_rules.execution import Executor
from ai_rules.hosts.adapters import build_host_adapters
from ai_rules.planning import render_plan
from ai_rules.platform import detect_environment, state_root
from ai_rules.profiles import load_profiles
from ai_rules.release import export_git_ref
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
    restore.add_argument("--dry-run", action="store_true", default=True)
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
    parser.add_argument("--state-dir", type=Path, default=state_root())


def cmd_setup(args: argparse.Namespace) -> int:
    plan = _resolve_from_args(args)
    print(_preflight_text())
    print(render_plan(plan))
    if args.dry_run:
        return 1 if plan.blocked else 0
    result = _executor_for_plan(plan, args).execute(plan, dry_run=False, yes=args.yes)
    for item in result.results:
        print(f"{item.capability_id} -> {item.host_id}: {item.status} {item.action} - {item.message}")
    if not args.yes:
        return 0
    _record_managed_first_party_installations(plan, result, args)
    capabilities = tuple(args.capabilities) if args.capabilities else tuple(_profile_capabilities(args.profile))
    write_profile(args.state_dir / "profile.json", args.profile, tuple(_hosts(args.hosts)), capabilities, args.scope)
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
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
            _record_managed_first_party_installations(repair_plan, result, args)
    return 0 if not plan.blocked else 1


def cmd_update(args: argparse.Namespace) -> int:
    plan = _resolve_from_args(args)
    print("AI-RULES update preview")
    print(render_plan(plan))
    return 1 if plan.blocked else 0


def cmd_snapshot(args: argparse.Namespace) -> int:
    create_snapshot(args.profile_path, args.lock_path, args.output, locked=args.locked)
    print(f"snapshot written: {args.output}")
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    snapshot = read_snapshot(args.snapshot)
    profile = snapshot.get("profile", {})
    print("AI-RULES restore dry-run")
    print(f"profile={profile.get('profile')} hosts={profile.get('hosts', [])} capabilities={profile.get('capabilities', [])}")
    print("restore requires setup confirmation before mutation")
    return 0


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
        bundle = args.state_dir / "bundles" / capability.id
        export_git_ref(release["commit"], bundle, repo_root=Path.cwd())
        bundles[capability.id] = bundle
    return Executor(args.state_dir, first_party_bundles=bundles, host_skill_roots=roots)


def _actual_state(catalog, args: argparse.Namespace) -> dict[tuple[str, str, str], ActualState]:
    records = _managed_installation_records(args.state_dir)
    adapters = build_host_adapters(catalog.hosts)
    result: dict[tuple[str, str, str], ActualState] = {}
    scope = Scope(args.scope)
    for host_id in _hosts(args.hosts):
        root = adapters[host_id].skill_target(scope, args.project_root)
        if root is None:
            continue
        for capability_id in catalog.capabilities:
            target = root / capability_id
            key = _installation_key(capability_id, host_id, scope)
            if not target.exists():
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


def _record_managed_first_party_installations(plan, result, args: argparse.Namespace) -> None:
    records = _managed_installation_records(args.state_dir)
    applied = {(item.capability_id, item.host_id, item.action) for item in result.results if item.status == "APPLIED"}
    catalog = load_catalog()
    adapters = build_host_adapters(catalog.hosts)
    for target in plan.targets:
        if (target.capability_id, target.host_id, target.action.value) not in applied:
            continue
        if target.capability_id not in _release_manifest().get("first_party", {}):
            continue
        root = adapters[target.host_id].skill_target(target.scope, args.project_root)
        if root is None:
            continue
        records[_installation_key(target.capability_id, target.host_id, target.scope)] = {
            "capability": target.capability_id,
            "host": target.host_id,
            "scope": target.scope.value,
            "version": target.target_version,
            "path": str(root / target.capability_id),
        }
    atomic_write_json(args.state_dir / "managed-installations.json", {"schema_version": 1, "installations": records})


def _managed_installation_records(state_dir: Path) -> dict[str, dict]:
    path = state_dir / "managed-installations.json"
    if not path.exists():
        return {}
    return dict(read_json(path).get("installations", {}))


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
