from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ai_rules.capabilities.adapters import StaticCapabilityAdapter
from ai_rules.catalog import load_catalog
from ai_rules.domain.statuses import Scope
from ai_rules.execution import Executor
from ai_rules.planning import render_plan
from ai_rules.platform import detect_environment, state_root
from ai_rules.profiles import load_profiles
from ai_rules.resolver import ResolveRequest, build_resolver
from ai_rules.state import create_snapshot, read_snapshot, write_profile
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
    result = Executor(args.state_dir).execute(plan, dry_run=False, yes=args.yes)
    for item in result.results:
        print(f"{item.capability_id} -> {item.host_id}: {item.status} {item.action} - {item.message}")
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
    resolver = build_resolver(catalog, profiles, StaticCapabilityAdapter())
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


def _preflight_text() -> str:
    env = detect_environment()
    commands = ", ".join(f"{name}={'yes' if present else 'no'}" for name, present in env.commands.items())
    return f"Preflight os={env.os} arch={env.architecture} python={env.python} commands=[{commands}]"
