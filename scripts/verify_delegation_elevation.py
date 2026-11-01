#!/usr/bin/env python3
"""
Deterministic Verification Script for Delegation Elevation.
Validates line count, mandatory sections, inline operational examples, progressive resources,
helper scripts, index references, and 59-skill catalog integrity with zero external dependencies.
"""

import json
import os
import re
import subprocess
import sys
import time

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def assert_true(condition, message):
    if not condition:
        print(f"[FAIL] {message}")
        sys.exit(1)
    print(f"[PASS] {message}")

def test_skill_md():
    skill_path = os.path.join(REPO_ROOT, "skills", "delegation", "SKILL.md")
    assert_true(os.path.exists(skill_path), "skills/delegation/SKILL.md exists")

    with open(skill_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        content = "".join(lines)

    line_count = len(lines)
    assert_true(line_count < 150, f"SKILL.md line count ({line_count}) is strictly under 150 lines")
    assert_true(line_count >= 70, f"SKILL.md line count ({line_count}) has sufficient density (>= 70 lines)")

    # Check mandatory sections
    assert_true("name: andino-delegation" in content, "SKILL.md contains correct frontmatter name")
    assert_true("Internal method ID: `andino-delegation`" in content, "SKILL.md contains internal method ID")
    assert_true("## 1. Dominant Negative Gates" in content, "SKILL.md contains Dominant Negative Gates")
    assert_true("## 2. Tri-Modal Operational Triage" in content, "SKILL.md contains Tri-Modal Operational Triage")
    assert_true("## 3. Gated Finite State Machine" in content, "SKILL.md contains Gated Finite State Machine")
    assert_true("## 4. Five Floor Invariants" in content, "SKILL.md contains Five Floor Invariants")
    assert_true("## 5. Operational Contract & Verification Harness" in content, "SKILL.md contains Operational Contract")
    assert_true("## 6. Progressive Disclosure & Provenance" in content, "SKILL.md contains Progressive Disclosure & Provenance")

    # Validate JSON in operational example
    match = re.search(r"```andino-operational-example\n(.*?)\n```", content, re.DOTALL)
    assert_true(match is not None, "Extracted andino-operational-example JSON block")
    contract = json.loads(match.group(1))
    assert_true(contract.get("concurrency_limit") == 3, "Operational example sets concurrency_limit == 3")
    assert_true(contract.get("max_fix_rounds") == 5, "Operational example sets max_fix_rounds == 5")
    assert_true(len(contract.get("tasks", [])) == 3, "Operational example defines 3 tasks")
    assert_true(contract.get("expected_frontier_step_0") == ["t1", "t2"], "Step 0 frontier is t1, t2")
    assert_true(contract.get("expected_frontier_step_1") == ["t3"], "Step 1 frontier is t3")

def test_guide_md():
    guide_path = os.path.join(REPO_ROOT, "skills", "delegation", "GUIDE.md")
    assert_true(os.path.exists(guide_path), "skills/delegation/GUIDE.md exists")

    with open(guide_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert_true("## 1. Architectural Overview & Synthesis" in content, "GUIDE.md contains Architectural Synthesis")
    assert_true("## 2. Tri-Modal Operational Triage" in content, "GUIDE.md contains Tri-Modal Triage")
    assert_true("## 3. The 6-Phase Gated Finite State Machine" in content, "GUIDE.md contains 6-Phase FSM")
    assert_true("## 4. Adaptive Model Selection & Reasoning Effort Rubric" in content, "GUIDE.md contains Model Tiering Rubric")
    assert_true("## 5. Anti-Rationalization Refutations & AI Evasion Move Counters" in content, "GUIDE.md contains Anti-Rationalizations")
    assert_true("## 6. Compaction Amnesia Recovery & Windows NTFS Defense" in content, "GUIDE.md contains Compaction & Windows Defense")
    assert_true("## 7. Progressive Disclosure Directory" in content, "GUIDE.md contains Progressive Disclosure")

def test_progressive_resources():
    res_dir = os.path.join(REPO_ROOT, "skills", "delegation", "resources")
    assert_true(os.path.isdir(res_dir), "skills/delegation/resources directory exists")

    required = [
        "frontier-and-dag-protocols.md",
        "subagent-brief-and-report-schemas.md",
        "two-track-review-and-fix-loop.md",
        "workspace-and-isolation-guards.md",
        "worked-example.md",
    ]
    for filename in required:
        fpath = os.path.join(res_dir, filename)
        assert_true(os.path.exists(fpath), f"Resource file {filename} exists")
        assert_true(os.path.getsize(fpath) > 500, f"Resource file {filename} is non-trivial (>500 bytes)")

def test_worked_example_harness():
    we_path = os.path.join(REPO_ROOT, "skills", "delegation", "resources", "worked-example.md")
    with open(we_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"```python andino-worked-example-verification\n(.*?)\n```", content, re.DOTALL)
    assert_true(match is not None, "Extracted worked-example Python test harness")
    code = match.group(1)

    # Normal mode
    proc_normal = subprocess.run([sys.executable, "-c", code], env=dict(os.environ, ANDINO_NEGATIVE="0"), capture_output=True, text=True)
    assert_true(proc_normal.returncode == 0, f"Worked example test harness passes in normal mode (exit 0)")

    # Adversarial negative mode
    proc_neg = subprocess.run([sys.executable, "-c", code], env=dict(os.environ, ANDINO_NEGATIVE="1"), capture_output=True, text=True)
    assert_true(proc_neg.returncode != 0, f"Worked example test harness catches negative mode (non-zero exit: got {proc_neg.returncode})")

def test_helper_scripts():
    scripts_dir = os.path.join(REPO_ROOT, "skills", "delegation", "scripts")
    assert_true(os.path.isdir(scripts_dir), "skills/delegation/scripts directory exists")

    plan_path = os.path.join(REPO_ROOT, "docs", "exec-plans", "active", "delegation-elevation.md")
    assert_true(os.path.exists(plan_path), "Plan file exists for script testing")

    # Test delegation_workspace.py
    ws_py = os.path.join(scripts_dir, "delegation_workspace.py")
    res_ws = subprocess.run([sys.executable, ws_py, plan_path], capture_output=True, text=True, encoding="utf-8")
    assert_true(res_ws.returncode == 0, "delegation_workspace.py runs and exits 0")
    ws_out = res_ws.stdout.strip()
    assert_true(".andino/delegation/delegation-elevation" in ws_out, f"Workspace path resolved correctly: {ws_out}")

    # Test task_brief.py
    tb_py = os.path.join(scripts_dir, "task_brief.py")
    res_tb = subprocess.run([sys.executable, tb_py, plan_path, "1"], capture_output=True, text=True, encoding="utf-8")
    assert_true(res_tb.returncode == 0, "task_brief.py runs and exits 0 for Task 1")

    # Clean up test workspace
    andino_dir = os.path.join(REPO_ROOT, ".andino")
    if os.path.exists(andino_dir):
        import shutil
        shutil.rmtree(andino_dir, ignore_errors=True)

    # Verify shell wrappers exist
    for wrapper in ["delegation-workspace", "task-brief", "review-package"]:
        wpath = os.path.join(scripts_dir, wrapper)
        assert_true(os.path.exists(wpath), f"Shell wrapper {wrapper} exists")

def test_references_and_catalog():
    index_path = os.path.join(REPO_ROOT, "references", "internal-method-index.md")
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()
    assert_true("[delegation](../skills/delegation/SKILL.md)" in index_content, "internal-method-index links delegation")
    assert_true("subagent-driven implementation" in index_content, "internal-method-index mentions subagent-driven")

    reg_path = os.path.join(REPO_ROOT, "references", "capability-registry.md")
    with open(reg_path, "r", encoding="utf-8") as f:
        reg_content = f.read()
    assert_true("subagent-driven-development, implement-spec resolve to canonical delegation" in reg_content, "capability-registry maps subagent-driven and implement-spec")

    readme_path = os.path.join(REPO_ROOT, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
    assert_true("`andino-delegation`" in readme_content, "README.md lists andino-delegation")

    prov_path = os.path.join(REPO_ROOT, "references", "legal", "provenance.md")
    with open(prov_path, "r", encoding="utf-8") as f:
        prov_content = f.read()
    assert_true("elevation of `delegation`" in prov_content, "provenance.md records elevation of delegation")

    skills_dir = os.path.join(REPO_ROOT, "skills")
    skill_subdirs = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
    assert_true(len(skill_subdirs) >= 59, f"Catalog contains {len(skill_subdirs)} member skills (>= 59 required)")
    assert_true("delegation" in skill_subdirs, "skills/delegation present in catalog")

if __name__ == "__main__":
    start = time.perf_counter()
    print("=== Running Deterministic Delegation Elevation Verification ===")
    test_skill_md()
    test_guide_md()
    test_progressive_resources()
    test_worked_example_harness()
    test_helper_scripts()
    test_references_and_catalog()
    elapsed = time.perf_counter() - start
    print(f"=== ALL VERIFICATION CHECKS PASSED DETERMINISTICALLY in {elapsed:.3f}s ===")
    assert_true(elapsed < 1.0, f"Verification completed swiftly (< 1.0s, elapsed {elapsed:.3f}s)")
    sys.exit(0)
