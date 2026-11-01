#!/usr/bin/env python3
"""
Deterministic Verification Script for Brainstorming Elevation & Decision-Interview Consolidation.
Validates line count, mandatory sections, inline operational examples, progressive resources,
forwarding shims, index references, and 59-skill catalog integrity with zero external dependencies.
"""

import os
import re
import subprocess
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def assert_true(condition, message):
    if not condition:
        print(f"[FAIL] {message}")
        sys.exit(1)
    print(f"[PASS] {message}")

def test_skill_md():
    skill_path = os.path.join(REPO_ROOT, "skills", "brainstorming", "SKILL.md")
    assert_true(os.path.exists(skill_path), "skills/brainstorming/SKILL.md exists")

    with open(skill_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        content = "".join(lines)

    line_count = len(lines)
    assert_true(line_count < 150, f"SKILL.md line count ({line_count}) is strictly under 150 lines")
    assert_true(line_count >= 80, f"SKILL.md line count ({line_count}) has sufficient density (>= 80 lines)")

    # Check mandatory sections
    assert_true("name: andino-brainstorming" in content, "SKILL.md contains correct frontmatter name")
    assert_true("Internal method ID: `andino-brainstorming`" in content, "SKILL.md contains internal method ID")
    assert_true("## Purpose and Selection" in content, "SKILL.md contains Purpose and Selection")
    assert_true("## Inputs and Progressive Resources" in content, "SKILL.md contains Inputs and Progressive Resources")
    assert_true("## Procedure" in content, "SKILL.md contains Procedure")
    assert_true("<HARD-GATE>" in content and "</HARD-GATE>" in content, "SKILL.md contains HARD-GATE block")
    assert_true("## Anti-Rationalization Refutations" in content, "SKILL.md contains Anti-Rationalization Refutations")
    assert_true("## Diagnostic Red Flags" in content, "SKILL.md contains Diagnostic Red Flags")
    assert_true("## Outputs, Verification and Fallback" in content, "SKILL.md contains Outputs, Verification and Fallback")
    assert_true("```python andino-operational-example" in content, "SKILL.md contains runnable operational example")
    assert_true("## Provenance" in content, "SKILL.md contains Provenance")

def test_operational_example():
    skill_path = os.path.join(REPO_ROOT, "skills", "brainstorming", "SKILL.md")
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"```python andino-operational-example\n(.*?)\n```", content, re.DOTALL)
    assert_true(match is not None, "Extracted inline Python operational example from SKILL.md")
    code = match.group(1)

    # Run in normal mode (expected exit 0)
    proc_normal = subprocess.run([sys.executable, "-c", code], env=dict(os.environ, ANDINO_NEGATIVE="0"))
    assert_true(proc_normal.returncode == 0, f"Inline operational example exits 0 in normal mode (got {proc_normal.returncode})")

    # Run in adversarial negative mode (expected exit 1)
    proc_neg = subprocess.run([sys.executable, "-c", code], env=dict(os.environ, ANDINO_NEGATIVE="1"))
    assert_true(proc_neg.returncode == 1, f"Inline operational example exits 1 in adversarial ANDINO_NEGATIVE=1 mode (got {proc_neg.returncode})")

def test_progressive_resources():
    res_dir = os.path.join(REPO_ROOT, "skills", "brainstorming", "resources")
    assert_true(os.path.isdir(res_dir), "skills/brainstorming/resources directory exists")

    for filename in ("grilling-protocol.md", "adr-and-glossary-template.md", "worked-example.md"):
        fpath = os.path.join(res_dir, filename)
        assert_true(os.path.exists(fpath), f"Resource file {filename} exists")
        assert_true(os.path.getsize(fpath) > 500, f"Resource file {filename} is non-trivial (>500 bytes)")

def test_decision_interview_forwarding():
    di_skill = os.path.join(REPO_ROOT, "skills", "decision-interview", "SKILL.md")
    di_guide = os.path.join(REPO_ROOT, "skills", "decision-interview", "GUIDE.md")
    assert_true(os.path.exists(di_skill), "skills/decision-interview/SKILL.md exists")
    assert_true(os.path.exists(di_guide), "skills/decision-interview/GUIDE.md exists")

    with open(di_skill, "r", encoding="utf-8") as f:
        content = f.read()
    assert_true("andino-brainstorming" in content, "decision-interview SKILL.md delegates to andino-brainstorming")
    assert_true("andino-decision-interview" in content, "decision-interview SKILL.md preserves method ID")

def test_references_and_catalog():
    # Check internal-method-index.md
    index_path = os.path.join(REPO_ROOT, "references", "internal-method-index.md")
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()
    assert_true("[brainstorming](../skills/brainstorming/SKILL.md)" in index_content, "internal-method-index links brainstorming")
    assert_true("[decision-interview](../skills/decision-interview/SKILL.md)" in index_content, "internal-method-index links decision-interview")
    assert_true("grill-me | [brainstorming]" in index_content, "grill-me maps to brainstorming")
    assert_true("interview-me | [brainstorming]" in index_content, "interview-me maps to brainstorming")

    # Check provenance.md
    prov_path = os.path.join(REPO_ROOT, "references", "legal", "provenance.md")
    with open(prov_path, "r", encoding="utf-8") as f:
        prov_content = f.read()
    assert_true("elevation of `brainstorming` and consolidation of `decision-interview`" in prov_content, "provenance.md records elevation")

    # Check 59 skills exist in skills/
    skills_dir = os.path.join(REPO_ROOT, "skills")
    skill_subdirs = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
    assert_true(len(skill_subdirs) >= 59, f"Catalog contains {len(skill_subdirs)} member skills (>= 59 required)")
    assert_true("brainstorming" in skill_subdirs, "skills/brainstorming present")
    assert_true("decision-interview" in skill_subdirs, "skills/decision-interview present")

if __name__ == "__main__":
    print("=== Running Deterministic Brainstorming Elevation Verification ===")
    test_skill_md()
    test_operational_example()
    test_progressive_resources()
    test_decision_interview_forwarding()
    test_references_and_catalog()
    print("=== ALL VERIFICATION CHECKS PASSED DETERMINISTICALLY ===")
    sys.exit(0)
