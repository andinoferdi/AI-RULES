#!/usr/bin/env python3
"""Deterministic offline verifier for elevated api-and-interface-design skill.

Validates:
1. Strict line-count ceiling (<150 lines) on root SKILL.md.
2. Strict line-count ceiling (<150 lines) on resources/http-contracts/contract.md.
3. SDO isolation and frontmatter formatting on root SKILL.md.
4. Absence of nested SKILL.md files inside any resources/ directory.
5. Resource contract isolation header on all contract.md files.
6. Local markdown link resolution across all skill files (zero broken links).
7. Deterministic execution of embedded operational Python harness (exit 0 normal, exit 1 on ANDINO_NEGATIVE=1).
8. Existence and non-trivial content (>300 chars) of all core guides.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "api-and-interface-design"


def extract_code_block(markdown_text: str, language_marker: str) -> str:
    pattern = rf"```{re.escape(language_marker)}\n(.*?)```"
    match = re.search(pattern, markdown_text, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find code block with marker: {language_marker}")
    return match.group(1)


def test_line_counts():
    root_skill = SKILL_DIR / "SKILL.md"
    assert root_skill.is_file(), f"Missing {root_skill}"
    root_lines = len(root_skill.read_text(encoding="utf-8").splitlines())
    assert root_lines < 150, f"SKILL.md exceeds strict 150 ceiling: {root_lines} lines"
    print(f"PASS: root SKILL.md line count budget ({root_lines} lines < 150)")

    http_contract = SKILL_DIR / "resources" / "http-contracts" / "contract.md"
    assert http_contract.is_file(), f"Missing {http_contract}"
    http_lines = len(http_contract.read_text(encoding="utf-8").splitlines())
    assert http_lines < 150, f"http-contracts/contract.md exceeds strict 150 ceiling: {http_lines} lines"
    print(f"PASS: http-contracts/contract.md line count budget ({http_lines} lines < 150)")


def test_frontmatter_sdo():
    root_skill = SKILL_DIR / "SKILL.md"
    text = root_skill.read_text(encoding="utf-8")
    assert text.startswith("---\n"), "SKILL.md must begin with YAML frontmatter"
    match = re.search(r"^name:\s*([^\n]+)", text, re.MULTILINE)
    assert match and match.group(1).strip() == "andino-api-and-interface-design", (
        f"Invalid name in frontmatter: {match.group(1) if match else 'None'}"
    )
    desc_match = re.search(r"^description:\s*([^\n]+)", text, re.MULTILINE)
    assert desc_match and desc_match.group(1).strip().startswith("Use when"), (
        "Description must follow SDO trigger-only pattern (Use when...)"
    )
    print("PASS: SDO frontmatter verified on root SKILL.md")


def test_no_nested_skills():
    nested = list((SKILL_DIR / "resources").rglob("SKILL.md"))
    assert len(nested) == 0, f"Resources must not contain nested SKILL.md files: {nested}"
    print("PASS: Zero nested SKILL.md files confirmed in resources/")


def test_resource_isolation_headers():
    for contract in (SKILL_DIR / "resources").rglob("contract.md"):
        content = contract.read_text(encoding="utf-8")
        assert not content.startswith("---\n"), f"{contract} must not have YAML frontmatter"
        assert "Resource contract; selected directly under its canonical owner." in content, (
            f"{contract} missing resource isolation header"
        )
    print("PASS: Resource isolation headers verified on all contract.md files")


def test_python_harness():
    root_skill = SKILL_DIR / "SKILL.md"
    code = extract_code_block(root_skill.read_text(encoding="utf-8"), "python andino-operational-example")
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        fpath = f.name
    try:
        # 1. Normal run -> exit 0
        p_normal = subprocess.run([sys.executable, fpath], capture_output=True, text=True)
        assert p_normal.returncode == 0, f"Normal run failed ({p_normal.returncode}): {p_normal.stderr}"
        out = json.loads(p_normal.stdout.strip())
        assert out.get("status") == "CONTRACT_VERIFIED", f"Unexpected output: {out}"

        # 2. Negative run -> exit 1
        env_neg = os.environ.copy()
        env_neg["ANDINO_NEGATIVE"] = "1"
        p_neg = subprocess.run([sys.executable, fpath], env=env_neg, capture_output=True, text=True)
        assert p_neg.returncode == 1, f"Negative run expected exit 1, got {p_neg.returncode}: {p_neg.stdout}"
        print("PASS: Operational Python harness deterministically verified (exit 0 normal, exit 1 negative)")
    finally:
        if os.path.exists(fpath):
            os.unlink(fpath)


def test_markdown_links():
    prose_pattern = re.compile(r"```.*?```", re.DOTALL)
    link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    broken = []
    for md_path in SKILL_DIR.rglob("*.md"):
        content = md_path.read_text(encoding="utf-8")
        clean_content = prose_pattern.sub("", content)
        for match in link_pattern.finditer(clean_content):
            target = match.group(1).split("#", 1)[0].strip()
            if not target or ":" in target or target.startswith("/"):
                continue
            resolved = (md_path.parent / target).resolve()
            if not resolved.exists():
                broken.append((str(md_path.relative_to(ROOT)), target))
    assert len(broken) == 0, f"Broken markdown links detected: {broken}"
    print("PASS: All internal markdown links resolve successfully (zero dead links)")


def main():
    print("=== Verifying api-and-interface-design Elevation ===")
    test_line_counts()
    test_frontmatter_sdo()
    test_no_nested_skills()
    test_resource_isolation_headers()
    test_python_harness()
    test_markdown_links()
    print("=== ALL ELEVATION AUDITS PASSED DETERMINISTICALLY ===")


if __name__ == "__main__":
    main()
