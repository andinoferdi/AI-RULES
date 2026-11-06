"""Render, detect and reconcile the agent-defaults block in global instruction files."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tomllib
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping

from ai_rules.domain.models import Host
from ai_rules.state import atomic_write_json, read_json

from .text import DOMAIN_HINTS, MCP_NOTES, MCP_UNKNOWN, TEXT

START = "<!-- ai-rules:global-defaults:start -->"
END = "<!-- ai-rules:global-defaults:end -->"
LANGUAGES = ("id", "en")
STATE_FILE = "agent-defaults.json"
BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"(?:\r?\n)?", re.S)
WRITES = {"INSTALL", "UPDATE", "REPLACE"}
RECORDED = WRITES | {"ADOPT", "CURRENT"}
OPENCODE_NOTE = "OpenCode will read this file instead of falling back to ~/.claude/CLAUDE.md"


@dataclass(frozen=True)
class DefaultsTarget:
    path: Path
    hosts: tuple[str, ...]
    language: str
    block: str
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class DefaultsResult:
    path: Path
    hosts: tuple[str, ...]
    status: str
    message: str = ""


def expand(path: str, home: Path) -> Path:
    return Path(path.replace("~", str(home), 1))


def render_block(language: str, skills: frozenset[str], mcp_servers: tuple[str, ...]) -> str:
    if language not in LANGUAGES:
        raise ValueError(f"unsupported agent-defaults language: {language}")
    t = TEXT[language]
    lines = [START, t["title"], "", t["intro"], ""]
    lines += [t["slots"], "", t["slots_intro"], "",
              t["slot_skills"], t["slot_tools"], t["slot_mode"], t["slot_task"], t["slot_context"],
              t["slot_done"], t["slot_constraints"], t["slots_free"], ""]
    lines += [t["flow"], "", t["workflow"] if "andino-workflow" in skills else t["workflow_generic"],
              t["direct"], t["debug"], t["verify"], ""]
    lines += [t["skills"], "", t["named"], t["conflict"]]
    if "ponytail" in skills:
        lines.append(t["ponytail"])
    if "search-first" in skills:
        lines.append(t["search_first"])
    hints = [text[language] for required, text in DOMAIN_HINTS if all(name in skills for name in required)]
    if hints:
        lines += [t["domain_intro"], *hints]
    lines += ["", t["mcp"], "", t["builtin"]]
    if mcp_servers:
        lines.append(t["mcp_intro"])
        lines += [f"  - `{name}`: {MCP_NOTES.get(name, MCP_UNKNOWN)[language]}" for name in sorted(mcp_servers)]
    else:
        lines.append(t["mcp_none"])
    lines += [t["mcp_named"], t["mcp_missing"], t["mcp_install"], t["mcp_data"], ""]
    lines += [t["subagent"], "", t["sub_delegation"] if "andino-delegation" in skills else t["sub_generic"],
              t["sub_approve"], t["sub_limits"], t["sub_retry"], ""]
    lines += [t["communication"], "", t["focus"] if "focus" in skills else t["focus_generic"],
              t["ask"], t["report"], ""]
    lines += [t["permissions"], "", t["perm"], t["perm_destructive"], t["perm_secrets"], END]
    return "\n".join(lines) + "\n"


def detect_skills(skill_root: Path | None) -> frozenset[str]:
    if skill_root is None or not skill_root.is_dir():
        return frozenset()
    return frozenset(child.name for child in skill_root.iterdir() if (child / "SKILL.md").is_file())


def detect_mcp_servers(host: Host, home: Path) -> tuple[tuple[str, ...], str | None]:
    if not host.mcp_config_path or not host.mcp_config_key:
        return (), None
    path = expand(host.mcp_config_path, home)
    if not path.is_file():
        return (), None
    try:
        raw = path.read_text(encoding="utf-8")
        data = tomllib.loads(raw) if host.mcp_config_format == "toml" else json.loads(raw)
    except (OSError, ValueError) as exc:  # JSONDecodeError and TOMLDecodeError are ValueErrors
        return (), f"MCP config unreadable, listed none: {path} ({exc.__class__.__name__})"
    section = data.get(host.mcp_config_key, {}) if isinstance(data, dict) else {}
    if isinstance(section, dict) and set(section) == {"servers"} and isinstance(section["servers"], dict):
        section = section["servers"]  # OpenCode shape observed on the user's machine
    if not isinstance(section, dict):
        return (), None
    return tuple(sorted(name for name, value in section.items() if isinstance(value, dict))), None


def read_state(state_dir: Path) -> dict:
    path = state_dir / STATE_FILE
    if not path.exists():
        return {"schema_version": 1, "files": {}}
    data = read_json(path)
    data.setdefault("files", {})
    return data


def plan_targets(
    hosts: Iterable[Host],
    home: Path,
    language: str | None,
    planned_skills: Mapping[str, Iterable[str]],
    recorded: Mapping[str, dict],
) -> tuple[DefaultsTarget, ...]:
    groups: dict[Path, list[Host]] = {}
    for host in hosts:
        if host.global_instructions_path:
            groups.setdefault(expand(host.global_instructions_path, home), []).append(host)
    targets = []
    for path, members in groups.items():
        skills: set[str] = set()
        servers: set[str] = set()
        warnings: list[str] = []
        for host in members:
            root = expand(host.global_skill_path, home) if host.global_skill_path else None
            skills |= detect_skills(root)
            skills |= set(planned_skills.get(host.id, ()))
            names, warning = detect_mcp_servers(host, home)
            servers |= set(names)
            if warning and warning not in warnings:
                warnings.append(warning)
        resolved = language or recorded.get(str(path), {}).get("language") or "id"
        targets.append(DefaultsTarget(path, tuple(host.id for host in members), resolved,
                                      render_block(resolved, frozenset(skills), tuple(sorted(servers))),
                                      tuple(warnings)))
    return tuple(targets)


def _normalize(block: str) -> str:
    return block.replace("\r\n", "\n").rstrip("\n") + "\n"


def _sha(block: str) -> str:
    return hashlib.sha256(_normalize(block).encode("utf-8")).hexdigest()


def _read(path: Path) -> str | None:
    return path.read_bytes().decode("utf-8") if path.is_file() else None


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.ai-rules-tmp")
    temporary.write_bytes(text.encode("utf-8"))
    os.replace(temporary, path)


def _backup(path: Path, state_dir: Path) -> Path:
    token = f"{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}"
    digest = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:12]
    backup = state_dir / "backups" / token / "agent-defaults" / f"{digest}-{path.name}"
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup)
    return backup


def _decide(target: DefaultsTarget, existing: str | None, record: dict | None,
            replace_unmanaged: bool, block: str, newline: str) -> tuple[str, str, str | None]:
    """Return (status, message, new_text) for one target file."""
    matches = list(BLOCK_RE.finditer(existing or ""))
    if len(matches) > 1:
        return "CONFLICT", "multiple managed blocks; preserved", None
    if not matches:
        body = existing or ""
        new_text = block if not body.strip() else body.rstrip("\r\n") + newline * 2 + block
        if record is None:
            return "INSTALL", "", new_text
        if replace_unmanaged:
            return "REPLACE", "reinstalled a block that was removed by hand", new_text
        return ("CONFLICT", "managed block was removed by hand; use --replace-agent-defaults to reinstall "
                "or remove --agent-defaults to forget it", None)
    match = matches[0]
    current = match.group(0)
    new_text = existing[:match.start()] + block + existing[match.end():]
    if record and _sha(current) == record.get("sha256"):
        if _normalize(current) == target.block:
            return "CURRENT", "", None
        return "UPDATE", "", new_text
    if record is None and _normalize(current) == target.block:
        return "ADOPT", "", None
    if replace_unmanaged:
        return "REPLACE", "", new_text
    if record:
        return "CONFLICT", "edited locally; preserved", None
    return "CONFLICT", "unrecorded block differs; rerun with --replace-agent-defaults (backup kept)", None


def reconcile(targets: Iterable[DefaultsTarget], state_dir: Path, *, apply: bool,
              replace_unmanaged: bool, home: Path) -> tuple[DefaultsResult, ...]:
    state = read_state(state_dir)
    results = []
    for target in targets:
        existing = _read(target.path)
        newline = "\r\n" if existing and "\r\n" in existing else "\n"
        block = target.block.replace("\n", newline)
        record = state["files"].get(str(target.path))
        status, message, new_text = _decide(target, existing, record, replace_unmanaged, block, newline)
        notes = [message] if message else []
        if "opencode" in target.hosts and existing is None and (home / ".claude/CLAUDE.md").is_file():
            notes.append(OPENCODE_NOTE)
        notes.extend(target.warnings)
        if apply and status in WRITES:
            backup = _backup(target.path, state_dir) if existing is not None else None
            _write(target.path, new_text)
            written = list(BLOCK_RE.finditer(_read(target.path) or ""))
            if len(written) != 1 or _sha(written[0].group(0)) != _sha(target.block):
                status = "FAILED"
                notes.append(f"written block did not verify; backup: {backup}")
            elif backup is not None:
                notes.append(f"backup: {backup}")
        if apply and status in RECORDED:
            state["files"][str(target.path)] = {
                "hosts": list(target.hosts),
                "language": target.language,
                "sha256": _sha(target.block),
                "created": record["created"] if record else existing is None,
            }
        results.append(DefaultsResult(target.path, target.hosts, status, "; ".join(notes)))
    if apply:
        atomic_write_json(state_dir / STATE_FILE, state)
    return tuple(results)


def remove(state_dir: Path, *, paths: set[Path] | None, apply: bool) -> tuple[DefaultsResult, ...]:
    state = read_state(state_dir)
    results = []
    for key, record in list(state["files"].items()):
        path = Path(key)
        if paths is not None and path not in paths:
            continue
        hosts = tuple(record.get("hosts", ()))
        existing = _read(path)
        matches = list(BLOCK_RE.finditer(existing or ""))
        if not matches:
            if apply:
                state["files"].pop(key)
            results.append(DefaultsResult(path, hosts, "ABSENT", "no managed block; record dropped"))
            continue
        match = matches[0]
        if len(matches) > 1 or _sha(match.group(0)) != record.get("sha256"):
            results.append(DefaultsResult(path, hosts, "CONFLICT", "edited locally; preserved"))
            continue
        newline = "\r\n" if "\r\n" in existing else "\n"
        before = existing[:match.start()].rstrip("\r\n")
        after = existing[match.end():].lstrip("\r\n")
        text = before + (newline * 2 if before and after else "") + after + (newline if before and not after else "")
        if apply:
            if not text.strip() and record.get("created"):
                path.unlink()
            else:
                _write(path, text)
            state["files"].pop(key)
        results.append(DefaultsResult(path, hosts, "REMOVED"))
    if apply:
        atomic_write_json(state_dir / STATE_FILE, state)
    return tuple(results)


def check(targets: Iterable[DefaultsTarget], state_dir: Path) -> tuple[DefaultsResult, ...]:
    files = read_state(state_dir)["files"]
    results = []
    for target in targets:
        record = files.get(str(target.path))
        if record is None:
            continue
        matches = list(BLOCK_RE.finditer(_read(target.path) or ""))
        if len(matches) != 1:
            status, message = "FAILED", "managed block missing"
        elif _sha(matches[0].group(0)) != record.get("sha256"):
            status, message = "FAILED", "edited locally"
        elif _normalize(matches[0].group(0)) != target.block:
            status, message = "UPDATE_AVAILABLE", "run ai-rules update to refresh skills/MCP list"
        else:
            status, message = "VERIFIED", ""
        results.append(DefaultsResult(target.path, target.hosts, status, message))
    return tuple(results)


def format_result(result: DefaultsResult, *, preview: bool) -> str:
    line = f"agent-defaults -> {', '.join(result.hosts)}: {'PREVIEW ' if preview else ''}{result.status} {result.path}"
    return line + (f" - {result.message}" if result.message else "")
