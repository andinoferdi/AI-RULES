#!/usr/bin/env python3
"""Deterministic offline verifier for elevated delivery craft under git-skills/branch-integration.

Validates:
1. Hard retirement of legacy callable skill directory (skills/delivery must be absent).
2. Strict line-count ceiling (<150 lines) on branch-integration contract.md.
3. Resource isolation header contract (non-callable internal resource under canonical owner).
4. Deterministic execution of embedded operational Python harness (exit 0 normal, exit 1 on ANDINO_NEGATIVE=1).
5. Existence and integrity of all modular resources in resources/*.
6. Local markdown link resolution (zero broken links).
7. Non-functional decorative emoji audit.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "git-skills" / "resources" / "branch-integration"
RETIRED_DIR = ROOT / "skills" / "delivery"


def extract_code_block(markdown_text: str, language_marker: str) -> str:
    pattern = rf"```{re.escape(language_marker)}\n(.*?)```"
    match = re.search(pattern, markdown_text, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find code block with marker: {language_marker}")
    return match.group(1)


def test_retired_directory():
    assert not RETIRED_DIR.exists(), f"Retired delivery skill directory must be absent: {RETIRED_DIR}"
    print("PASS: Forwarder/standalone delivery directory confirmed hard-retired")


def test_line_count():
    contract_file = SKILL_DIR / "contract.md"
    assert contract_file.is_file(), f"Missing {contract_file}"
    lines = contract_file.read_text(encoding="utf-8").splitlines()
    total_lines = len(lines)
    assert total_lines < 150, f"contract.md exceeds strict 150 ceiling: {total_lines} lines"
    print(f"PASS: contract.md line count budget ({total_lines} lines < 150)")


def test_resource_isolation_header():
    contract_file = SKILL_DIR / "contract.md"
    content = contract_file.read_text(encoding="utf-8")
    assert "Resource contract; selected directly under its canonical owner." in content, (
        "Missing resource contract isolation header"
    )
    # Ensure no YAML frontmatter declaring an independent callable skill identity
    assert not content.startswith("---\n"), "Resource contract must not have YAML frontmatter declaring a standalone skill"
    print("PASS: Resource isolation header verified (non-callable internal procedure)")


def test_operational_python_harness():
    contract_file = SKILL_DIR / "contract.md"
    code = extract_code_block(contract_file.read_text(encoding="utf-8"), "python andino-operational-example")

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
    assert data.get("status") == "DELIVERY_CONTRACT_VERIFIED", f"Unexpected status: {data}"

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
    assert (SKILL_DIR / "guide.md").is_file(), f"Missing guide.md in {SKILL_DIR}"
    assert (SKILL_DIR / "contract.md").is_file(), f"Missing contract.md in {SKILL_DIR}"

    required_resources = [
        "contract.md",
        "environment-and-worktree-detection.md",
        "pre-integration-verification.md",
        "integration-menu-and-execution.md",
        "workspace-cleanup-and-safety.md",
        "anti-rationalization-and-failure-modes.md",
    ]
    res_dir = SKILL_DIR / "resources"
    assert res_dir.is_dir(), f"Missing resources directory: {res_dir}"
    for filename in required_resources:
        file_path = res_dir / filename
        assert file_path.is_file(), f"Missing required resource: {file_path}"
        assert file_path.stat().st_size > 100, f"Resource file is suspiciously small: {file_path}"

    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    for md_file in SKILL_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        clean_content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        for text, target in link_pattern.findall(clean_content):
            if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
                continue
            target_path = target.split("#")[0]
            if not target_path:
                continue
            resolved = (md_file.parent / target_path).resolve()
            assert resolved.exists(), f"Broken relative link in {md_file}: [{text}]({target}) -> {resolved}"

    print(f"PASS: All {len(required_resources)} modular resources verified with 100% link integrity")


def test_emoji_cleanliness():
    emoji_pattern = re.compile(r"[\U0001F300-\U0001FAFF]")
    for md_file in SKILL_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        clean_content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        clean_content = re.sub(r"`.*?`", "", clean_content)
        matches = emoji_pattern.findall(clean_content)
        assert not matches, f"Decorative emoji detected in {md_file}: {matches}"
    print("PASS: Zero decorative emojis detected across branch-integration suite")


def main():
    print("Starting deterministic offline verification for git-skills/branch-integration elevation...")
    test_retired_directory()
    test_line_count()
    test_resource_isolation_header()
    test_operational_python_harness()
    test_modular_resources_and_link_integrity()
    test_emoji_cleanliness()
    print("\nALL 6 VERIFICATION SUITES PASSED SUCCESSFULLY (100% PASS).")


if __name__ == "__main__":
    main()
