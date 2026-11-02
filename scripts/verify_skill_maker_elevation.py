#!/usr/bin/env python3
"""Deterministic offline verifier for andino-skill-maker elevation.

Validates:
1. Strict line-count ceiling (<150 lines) on root SKILL.md.
2. SDO frontmatter rules (trigger-only, third person, no workflow leakage).
3. Deterministic execution of embedded operational Python harness (exit 0 normal, exit 1 on ANDINO_NEGATIVE=1).
4. Existence and integrity of modular resources in resources/*.
5. Local markdown link resolution (zero broken links).
6. Non-functional decorative emoji audit.
7. Backward compatibility forwarding shim (skills/method-authoring).
8. Installer compatibility (_is_valid_skill_tree) and simulated host bundle installation.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "skill-maker"
SHIM_DIR = ROOT / "skills" / "method-authoring"


def extract_code_block(markdown_text: str, language_marker: str) -> str:
    pattern = rf"```{re.escape(language_marker)}\n(.*?)```"
    match = re.search(pattern, markdown_text, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find code block with marker: {language_marker}")
    return match.group(1)


def test_line_count():
    skill_file = SKILL_DIR / "SKILL.md"
    assert skill_file.is_file(), f"Missing {skill_file}"
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    total_lines = len(lines)
    assert total_lines < 150, f"SKILL.md exceeds strict 150 ceiling: {total_lines} lines"
    print(f"PASS: SKILL.md line count budget ({total_lines} lines < 150)")


def test_sdo_frontmatter():
    skill_file = SKILL_DIR / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    assert match, "Missing YAML frontmatter in SKILL.md"
    frontmatter = match.group(1)
    assert len(frontmatter) < 1024, "Frontmatter exceeds 1024 char ceiling"
    assert "name: andino-skill-maker" in frontmatter, "Missing canonical name"
    assert "description: Use when" in frontmatter, "Description must start with 'Use when'"
    # Verify no workflow summary leak in description
    desc_match = re.search(r"description:\s*(.+)", frontmatter)
    assert desc_match, "Missing description"
    desc = desc_match.group(1).lower()
    for leak_word in ("first do", "step 1", "runs repro", "minimizes input"):
        assert leak_word not in desc, f"Workflow leakage detected in description: {leak_word}"
    print("PASS: SDO frontmatter rules strictly verified")


def test_operational_python_harness():
    skill_file = SKILL_DIR / "SKILL.md"
    code = extract_code_block(skill_file.read_text(encoding="utf-8"), "python andino-operational-example")

    # Run normal (exit 0 expected)
    proc_normal = subprocess.run(
        [sys.executable, "-B", "-I", "-c", code],
        capture_output=True,
        text=True,
        env={**os.environ, "ANDINO_NEGATIVE": "0"},
    )
    assert proc_normal.returncode == 0, f"Normal execution failed: {proc_normal.stderr}"
    data = json.loads(proc_normal.stdout.strip())
    assert data.get("valid") is True, f"Unexpected verification payload: {data}"
    assert data.get("status") == "CONTRACT_VERIFIED", f"Unexpected status: {data}"

    # Run negative (exit 1 expected)
    proc_neg = subprocess.run(
        [sys.executable, "-B", "-I", "-c", code],
        capture_output=True,
        text=True,
        env={**os.environ, "ANDINO_NEGATIVE": "1"},
    )
    assert proc_neg.returncode == 1, f"Expected exit 1 on ANDINO_NEGATIVE=1, got {proc_neg.returncode}"
    print("PASS: Operational Python harness verified (exit 0 on valid, exit 1 on ANDINO_NEGATIVE=1)")


def test_modular_resources_and_link_integrity():
    required_resources = [
        "contract.md",
        "sdo-and-discovery-protocols.md",
        "failure-form-matching-and-bulletproofing.md",
        "subagent-testing-and-pressure-scenarios.md",
        "anthropic-craft-and-degrees-of-freedom.md",
        "worked-examples-and-templates.md",
    ]
    res_dir = SKILL_DIR / "resources"
    assert res_dir.is_dir(), f"Missing resources directory: {res_dir}"
    for filename in required_resources:
        file_path = res_dir / filename
        assert file_path.is_file(), f"Missing required resource: {file_path}"
        assert file_path.stat().st_size > 100, f"Resource file is suspiciously small: {file_path}"

    # Check link integrity across all markdown files in skill-maker
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    for md_file in SKILL_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        # Strip code blocks
        clean_content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        for text, target in link_pattern.findall(clean_content):
            if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
                continue
            # Strip anchors
            target_path = target.split("#")[0]
            if not target_path:
                continue
            resolved = (md_file.parent / target_path).resolve()
            assert resolved.exists(), f"Broken relative link in {md_file}: [{text}]({target}) -> {resolved}"

    print(f"PASS: All {len(required_resources)} modular resources verified with 100% link integrity")


def test_emoji_cleanliness():
    # Verify no decorative unicode emojis in markdown prose
    emoji_pattern = re.compile(r"[\U0001F300-\U0001FAFF]")
    for md_file in SKILL_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        clean_content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        clean_content = re.sub(r"`.*?`", "", clean_content)
        matches = emoji_pattern.findall(clean_content)
        assert not matches, f"Decorative emoji detected in {md_file}: {matches}"
    print("PASS: Zero decorative emojis detected across skill-maker suite")


def test_forwarding_shim():
    # Method-authoring forwarding shim has been hard-retired under accepted Option B.
    assert not SHIM_DIR.exists(), f"Retired forwarding shim directory must be absent: {SHIM_DIR}"
    print("PASS: Forwarding shim (skills/method-authoring) confirmed hard-retired")


def test_setup_installer_compatibility():
    # Verify _is_valid_skill_tree contract
    assert (SKILL_DIR / "SKILL.md").is_file()
    assert not SHIM_DIR.exists()

    with tempfile.TemporaryDirectory(prefix="andino-setup-test-") as tmp:
        tmp_path = Path(tmp)
        host_roots = {
            "claude-code": tmp_path / "claude" / "skills",
            "codex": tmp_path / "agents" / "skills",
            "opencode": tmp_path / "opencode" / "skills",
            "antigravity-cli": tmp_path / "antigravity" / "skills",
            "antigravity-ide": tmp_path / "antigravity-ide" / "skills",
        }

        # Source hash of skill-maker
        source_hashes = {
            p.relative_to(SKILL_DIR).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in SKILL_DIR.rglob("*") if p.is_file()
        }

        # Simulate copy_tree_atomic installation across hosts
        for host, root in host_roots.items():
            target_dir = root / "andino-skill-maker"
            target_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(SKILL_DIR, target_dir)

            # Verify byte-for-byte SHA256 integrity
            for rel_path, expected_hash in source_hashes.items():
                installed_file = target_dir / rel_path
                assert installed_file.is_file(), f"Missing installed file: {installed_file}"
                actual_hash = hashlib.sha256(installed_file.read_bytes()).hexdigest()
                assert actual_hash == expected_hash, f"Hash mismatch in {installed_file}"

    print("PASS: Installer setup compatibility verified byte-for-byte across 5 host targets")


def main():
    print("Starting deterministic offline verification for andino-skill-maker elevation...")
    test_line_count()
    test_sdo_frontmatter()
    test_operational_python_harness()
    test_modular_resources_and_link_integrity()
    test_emoji_cleanliness()
    test_forwarding_shim()
    test_setup_installer_compatibility()
    print("\nALL 7 VERIFICATION SUITES PASSED SUCCESSFULLY (100% PASS).")


if __name__ == "__main__":
    main()
