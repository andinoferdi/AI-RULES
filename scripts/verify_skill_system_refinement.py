#!/usr/bin/env python3
"""
verify_skill_system_refinement.py - Deterministic master verification suite
for the Final Skill System Refinement across the Andino ecosystem.

Validates:
1. Root coordinator contract (`SKILL.md`) line budget (< 150 lines) and embedded decision lens (< 40 lines).
2. Canonical `skills/skill-maker` bundle, dual-mode authoring contract, boundary/craft tests, and negative mode.
3. Physical forwarding shim `skills/method-authoring` redirecting to `skills/skill-maker`.
4. Contrastive Decision Lens fixture (`tests/fixtures/decision_lens_cases.json`, contract, and static verifier).
5. Zero forbidden decorative emojis across the entire `skills/` tree.
6. Delegation elevation safety (`ANDINO_WORKSPACE_OVERRIDE`, git fixture, snapshots, NTFS cleanup).
7. Scoped inventory for 20 member directories, identity, negative gates, craft-exception line budgets,
   and fence-aware relative Markdown target audits.
8. Documentation, catalog counts (>= 60), 6-phase debugging alignment, and internal method index mappings.
"""

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHILD_TIMEOUT = 30

SCOPED_DIRECTORIES = [
    "skills/agent-document-authoring",
    "skills/api-and-interface-design",
    "skills/architecture-survey",
    "skills/article-shaping",
    "skills/brainstorming",
    "skills/browser-testing-with-devtools",
    "skills/ci-cd-and-automation",
    "skills/code-review",
    "skills/code-simplification",
    "skills/constraint-driven-development",
    "skills/context-engineering",
    "skills/debugging",
    "skills/decision-interview",
    "skills/decision-map",
    "skills/deep-module-design",
    "skills/delegation",
    "skills/planning",
    "skills/plan-execution",
    "skills/skill-maker",
    "skills/method-authoring",
]

CRAFT_EXCEPTIONS = {
    "skills/api-and-interface-design": "Contract-first API design, error semantics, and interface boundary craft",
    "skills/architecture-survey": "Bounded architectural discovery, topology mapping, and dependency inspection craft",
    "skills/browser-testing-with-devtools": "Headless and interactive browser runtime verification craft",
    "skills/ci-cd-and-automation": "Pipeline automation and pre-commit CI gating craft",
    "skills/planning": "Actionable task decomposition and dependency sequencing craft",
    "skills/plan-execution": "Gated plan execution and checkpoint progression craft",
}


def assert_true(condition, msg):
    if not condition:
        print(f"[FAIL] {msg}", file=sys.stderr)
        sys.exit(1)
    print(f"[PASS] {msg}")


def outside_fences(text):
    """Return prose only, retaining line positions; ignore backtick/tilde code fences."""
    fence = None
    result = []
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            result.append("")
        else:
            result.append(line if fence is None else "")
    return "\n".join(result)


def run_child(arguments, *, cwd=None, env=None):
    child_env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    if env:
        child_env.update(env)
    if arguments[0] == sys.executable and "-B" not in arguments:
        arguments = [arguments[0], "-B", *arguments[1:]]
    try:
        return subprocess.run(
            arguments,
            cwd=cwd or REPO_ROOT,
            env=child_env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=CHILD_TIMEOUT,
        )
    except subprocess.TimeoutExpired as error:
        raise AssertionError(f"Child process timed out after {CHILD_TIMEOUT}s: {arguments}") from error


def test_root_coordinator():
    skill_path = os.path.join(REPO_ROOT, "SKILL.md")
    assert_true(os.path.exists(skill_path), "Root SKILL.md exists")
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.splitlines()
    assert_true(len(lines) < 150, f"Root SKILL.md ({len(lines)} lines) is strictly under 150 lines")
    assert_true("## Select work methods first" in content, "Root SKILL.md contains 'Select work methods first'")
    assert_true(
        "| User Situation / Task Trigger | Active Phase | Primary Specialist | Direct Bypass / Negative Gate |"
        in content,
        "Root SKILL.md embeds Decision Lens table",
    )
    # Check Decision Lens table line budget (< 40 lines)
    lens_lines = [
        l for l in outside_fences(content).splitlines() if l.startswith("|")
    ]
    lens_table_lines = len(lens_lines)
    assert_true(
        lens_table_lines < 40,
        f"Decision Lens table ({lens_table_lines} table lines) is strictly under 40 lines",
    )
    assert_true("`skill-maker`" in content, "Root SKILL.md Decision Lens references skill-maker")
    assert_true("**Direct Execution**" in content, "Root SKILL.md Decision Lens contains Direct Execution Bypass")


def test_method_dispatch():
    dispatch_path = os.path.join(REPO_ROOT, "references", "method-dispatch.md")
    assert_true(os.path.exists(dispatch_path), "references/method-dispatch.md exists")
    with open(dispatch_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert_true("### Situation-to-Outcome Decision Lens" in content, "method-dispatch.md contains Decision Lens")
    assert_true("### Contrastive Near-Miss Pairs" in content, "method-dispatch.md contains Near-Miss Pairs")
    assert_true("### Low Ceremony Interaction Standard" in content, "method-dispatch.md contains Low Ceremony Standard")
    assert_true(
        "`[andino-workflow] Active method: <method-name> — <reason>.`" in content,
        "method-dispatch.md defines single-line rationale schema",
    )
    assert_true("### Selection-to-Loading Enforcement" in content, "method-dispatch.md contains Selection-to-Loading Enforcement")
    assert_true("DISCOVERED -> AVAILABLE -> INVOKABLE -> ACTIVE -> USED" in content, "method-dispatch.md defines 5-state lifecycle")


def test_skill_maker_and_authoring_contracts():
    sm_dir = os.path.join(REPO_ROOT, "skills", "skill-maker")
    assert_true(os.path.isdir(sm_dir), "skills/skill-maker directory exists")

    skill_path = os.path.join(sm_dir, "SKILL.md")
    assert_true(os.path.exists(skill_path), "skills/skill-maker/SKILL.md exists")
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.splitlines()
    assert_true(len(lines) < 150, f"skill-maker/SKILL.md ({len(lines)} lines) is strictly under 150 lines")
    assert_true("name: andino-skill-maker" in content, "skill-maker frontmatter name is andino-skill-maker")
    assert_true("Mode A: Remedial" in content, "skill-maker defines Mode A Remedial")
    assert_true("Mode B: Greenfield" in content, "skill-maker defines Mode B Greenfield")
    assert_true("## 1. Dominant Negative Gates" in content, "skill-maker contains Dominant Negative Gates")

    guide_path = os.path.join(sm_dir, "GUIDE.md")
    assert_true(os.path.exists(guide_path), "skills/skill-maker/GUIDE.md exists")

    contract_path = os.path.join(sm_dir, "resources", "contract.md")
    assert_true(os.path.exists(contract_path), "skills/skill-maker/resources/contract.md exists")

    # Extract evaluate_skill_contract function from SKILL.md
    fn_match = re.search(r"(def evaluate_skill_contract\(.*?\n(?=sample_payload))", content, re.DOTALL)
    assert_true(fn_match is not None, "Extracted evaluate_skill_contract definition from skill-maker/SKILL.md")
    eval_scope = {"re": re}
    exec(fn_match.group(1), eval_scope)
    evaluate_skill_contract = eval_scope["evaluate_skill_contract"]

    # 1. Boundary strict 149 lines (accepted)
    res_149 = evaluate_skill_contract({
        "name": "andino-boundary-test",
        "mode": "remedial",
        "contract_lines": 149,
        "has_negative_gates": True,
    })
    assert_true(res_149.get("valid") is True and res_149.get("status") == "CONTRACT_VERIFIED",
                "evaluate_skill_contract accepts strict boundary 149 lines")

    # 2. Boundary strict 150 lines (rejected)
    res_150 = evaluate_skill_contract({
        "name": "andino-boundary-test",
        "mode": "remedial",
        "contract_lines": 150,
        "has_negative_gates": True,
    })
    assert_true(res_150.get("valid") is False and "Strict contracts require <150 lines" in res_150.get("error", ""),
                "evaluate_skill_contract rejects strict boundary 150 lines")

    # 3. Greenfield mode (accepted)
    res_green = evaluate_skill_contract({
        "name": "andino-greenfield-test",
        "mode": "greenfield",
        "contract_lines": 88,
        "has_negative_gates": True,
    })
    assert_true(res_green.get("valid") is True and res_green.get("mode") == "greenfield",
                "evaluate_skill_contract accepts greenfield mode")

    # 4. Remedial mode (accepted)
    res_remed = evaluate_skill_contract({
        "name": "andino-remedial-test",
        "mode": "remedial",
        "contract_lines": 100,
        "has_negative_gates": True,
    })
    assert_true(res_remed.get("valid") is True and res_remed.get("mode") == "remedial",
                "evaluate_skill_contract accepts remedial mode")

    # 5. Member contract kind with documented craft exception (accepted at 150+ lines)
    res_member_exc = evaluate_skill_contract({
        "name": "andino-member-craft",
        "mode": "greenfield",
        "contract_kind": "member",
        "craft_exception": "Domain FSM and extensive procedural protocols",
        "contract_lines": 210,
        "has_negative_gates": True,
    })
    assert_true(res_member_exc.get("valid") is True and res_member_exc.get("status") == "CONTRACT_VERIFIED",
                "evaluate_skill_contract accepts member contract kind with documented craft exception at 210 lines")

    # 6. Member contract kind without craft exception (rejected at 150+ lines)
    res_member_no_exc = evaluate_skill_contract({
        "name": "andino-member-craft",
        "mode": "greenfield",
        "contract_kind": "member",
        "craft_exception": "",
        "contract_lines": 150,
        "has_negative_gates": True,
    })
    assert_true(res_member_no_exc.get("valid") is False,
                "evaluate_skill_contract rejects member contract kind without craft exception at 150 lines")

    # 7. Root contract kind with craft exception (rejected at 150+ lines; root cannot bypass strict line limit)
    res_root_exc = evaluate_skill_contract({
        "name": "andino-root-test",
        "mode": "greenfield",
        "contract_kind": "root",
        "craft_exception": "Root coordinator craft",
        "contract_lines": 150,
        "has_negative_gates": True,
    })
    assert_true(res_root_exc.get("valid") is False,
                "evaluate_skill_contract rejects root contract kind at 150+ lines even with craft exception")

    # 8. Invalid modes, names, and negative gate flags
    assert_true(evaluate_skill_contract({"mode": "invalid"}).get("valid") is False,
                "evaluate_skill_contract rejects invalid mode")
    assert_true(evaluate_skill_contract({"mode": "remedial", "name": "bad_name"}).get("valid") is False,
                "evaluate_skill_contract rejects non-kebab name")
    assert_true(evaluate_skill_contract({
        "name": "andino-sample",
        "mode": "greenfield",
        "contract_lines": 88,
        "has_negative_gates": False,
    }).get("valid") is False, "evaluate_skill_contract rejects has_negative_gates=False")

    # Test runnable operational example code block
    m = re.search(r"```python andino-operational-example\n(.*?)```", content, re.DOTALL)
    assert_true(bool(m), "skill-maker/SKILL.md contains runnable operational example")
    code = m.group(1)

    # Test normal mode via run_child
    res_normal = run_child([sys.executable, "-c", code])
    assert_true(res_normal.returncode == 0, f"skill-maker operational example exits 0 in normal mode: {res_normal.stderr}")
    assert_true("CONTRACT_VERIFIED" in res_normal.stdout, "skill-maker operational example returns CONTRACT_VERIFIED")

    # Test negative mode via run_child with ANDINO_NEGATIVE=1
    res_neg = run_child([sys.executable, "-c", code], env={"ANDINO_NEGATIVE": "1"})
    assert_true(res_neg.returncode != 0, "skill-maker operational example catches negative mode (exits non-zero)")
    assert_true("Strict contracts require <150 lines" in res_neg.stderr,
                "skill-maker negative mode reports strict line limit violation")


def test_method_authoring_forwarding_shim():
    ma_dir = os.path.join(REPO_ROOT, "skills", "method-authoring")
    assert_true(os.path.isdir(ma_dir), "skills/method-authoring directory exists (forwarding shim)")

    skill_path = os.path.join(ma_dir, "SKILL.md")
    assert_true(os.path.exists(skill_path), "skills/method-authoring/SKILL.md exists")
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.splitlines()
    assert_true(len(lines) < 70, f"method-authoring forwarding shim ({len(lines)} lines) is concise (< 70 lines)")
    assert_true("andino-skill-maker" in content, "method-authoring forwards to andino-skill-maker")

    m = re.search(r"```python andino-operational-example\n(.*?)```", content, re.DOTALL)
    assert_true(bool(m), "method-authoring/SKILL.md contains forwarding verification harness")
    code = m.group(1)
    res = run_child([sys.executable, "-c", code])
    assert_true(res.returncode == 0, f"method-authoring forwarding verification exits 0: {res.stderr}")


def test_decision_lens_evaluator():
    script_path = os.path.join(REPO_ROOT, "scripts", "verify_decision_lens.py")
    assert_true(os.path.exists(script_path), "scripts/verify_decision_lens.py exists")
    res = run_child([sys.executable, script_path])
    assert_true(res.returncode == 0, f"verify_decision_lens.py exits 0:\n{res.stderr}")
    assert_true("STATIC DECISION LENS CONTRACT PASSED" in res.stdout,
                "verify_decision_lens.py confirms static contract pass")
    assert_true("NOT_VERIFIED" in res.stdout,
                "verify_decision_lens.py explicitly marks live model routing NOT_VERIFIED")


def test_zero_decorative_emojis():
    skills_dir = os.path.join(REPO_ROOT, "skills")
    emoji_pattern = re.compile(r"[\U00010000-\U0010ffff]|[☀-➿]")
    found = []
    for root, _, files in os.walk(skills_dir):
        for file in files:
            if file.endswith(".md"):
                fpath = os.path.join(root, file)
                with open(fpath, "r", encoding="utf-8") as f:
                    text = f.read()
                matches = emoji_pattern.findall(text)
                if matches:
                    rel = os.path.relpath(fpath, REPO_ROOT).replace("\\", "/")
                    found.append((rel, matches))
    assert_true(len(found) == 0, f"Zero decorative emojis in skills/ (found {len(found)} files with emojis: {found})")


def test_delegation_elevation():
    script_path = os.path.join(REPO_ROOT, "scripts", "verify_delegation_elevation.py")
    assert_true(os.path.exists(script_path), "scripts/verify_delegation_elevation.py exists")
    res = run_child([sys.executable, script_path])
    assert_true(res.returncode == 0, f"verify_delegation_elevation.py exits 0:\n{res.stderr}")
    assert_true("ALL VERIFICATION CHECKS PASSED DETERMINISTICALLY" in res.stdout,
                "verify_delegation_elevation.py passes all checks")


def test_scoped_inventory_and_links():
    root = Path(REPO_ROOT)
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    checked_links = 0
    broken_links = []

    for rel_dir in SCOPED_DIRECTORIES:
        dir_path = root / rel_dir
        assert_true(dir_path.is_dir(), f"Scoped directory exists: {rel_dir}")
        skill_path = dir_path / "SKILL.md"
        assert_true(skill_path.is_file(), f"SKILL.md exists in {rel_dir}")

        content = skill_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        dir_name = Path(rel_dir).name

        # Identity check: canonical frontmatter name
        assert_true(f"name: andino-{dir_name}" in content,
                    f"Canonical frontmatter identity 'name: andino-{dir_name}' in {rel_dir}/SKILL.md")

        # Line budget check: strict <150 lines unless documented in CRAFT_EXCEPTIONS
        if rel_dir in CRAFT_EXCEPTIONS:
            assert_true(len(lines) > 0, f"{rel_dir}/SKILL.md has content")
        else:
            assert_true(len(lines) < 150,
                        f"{rel_dir}/SKILL.md ({len(lines)} lines) strictly adheres to <150 line budget")

        # Negative gate or forwarding directive check
        if rel_dir in ("skills/method-authoring", "skills/decision-interview"):
            assert_true("Forwarding Directive" in content or "forwards" in content.lower(),
                        f"Forwarding shim {rel_dir} contains explicit forwarding directive")
        else:
            has_gate = bool(re.search(
                r"negative\s+gate|non-trigger|do\s+not\s+(?:use|activate)\s+for|anti-pattern|when\s+not\s+to\s+use|diagnostic\s+red\s+flags",
                content,
                re.IGNORECASE,
            ))
            assert_true(has_gate, f"Negative gate or non-trigger contract present in {rel_dir}/SKILL.md")

        # Relative Markdown target check (fence-aware) across all markdown files in directory
        for md_path in dir_path.rglob("*.md"):
            prose = outside_fences(md_path.read_text(encoding="utf-8"))
            for _, raw_target in link_pattern.findall(prose):
                target = raw_target.strip().split("#")[0]
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                resolved = (md_path.parent / target).resolve()
                if not resolved.exists():
                    broken_links.append((str(md_path.relative_to(root)), raw_target, str(resolved)))
                else:
                    checked_links += 1

    assert_true(len(broken_links) == 0,
                f"Zero broken relative links across 20 scoped directories (checked {checked_links}, broken: {broken_links})")
    print(f"[PASS] Checked {checked_links} relative Markdown links across 20 scoped directories with zero broken targets")


def test_catalog_and_registries():
    # Catalog directory count >= 60 (including shims)
    skills_dir = os.path.join(REPO_ROOT, "skills")
    subdirs = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
    assert_true(len(subdirs) >= 60, f"Catalog directory count ({len(subdirs)}) >= 60")
    assert_true("skill-maker" in subdirs, "skills/skill-maker present in skills/")
    assert_true("method-authoring" in subdirs, "skills/method-authoring present in skills/")

    # internal-method-index mappings
    index_path = os.path.join(REPO_ROOT, "references", "internal-method-index.md")
    with open(index_path, "r", encoding="utf-8") as f:
        icontent = f.read()
    assert_true("[skill-maker](../skills/skill-maker/SKILL.md)" in icontent, "internal-method-index links skill-maker")
    assert_true("[method-authoring](../skills/method-authoring/SKILL.md)" in icontent, "internal-method-index links method-authoring forwarding alias")
    assert_true("| writing-skills | [skill-maker](../skills/skill-maker/SKILL.md) |" in icontent, "internal-method-index maps writing-skills to skill-maker")

    # README.md debugging alignment: 6 true phase names Loop -> Minimize -> Hypothesize -> Probe -> Fix -> Clean
    readme_path = os.path.join(REPO_ROOT, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        rcontent = f.read()
    assert_true("Loop -> Minimize -> Hypothesize -> Probe -> Fix -> Clean" in rcontent,
                "README.md describes debugging with true six phase names: Loop -> Minimize -> Hypothesize -> Probe -> Fix -> Clean")

    # provenance.md elevation record
    prov_path = os.path.join(REPO_ROOT, "references", "legal", "provenance.md")
    with open(prov_path, "r", encoding="utf-8") as f:
        pcontent = f.read()
    assert_true("elevation of the Skill System, `skill-maker`, and Coordinator Discovery" in pcontent or
                "elevation of `delegation`" in pcontent,
                "provenance.md records skill system elevation")


def main():
    start_time = time.perf_counter()
    print("=== Running Deterministic Skill System Refinement Master Verifier ===")

    test_root_coordinator()
    test_method_dispatch()
    test_skill_maker_and_authoring_contracts()
    test_method_authoring_forwarding_shim()
    test_decision_lens_evaluator()
    test_zero_decorative_emojis()
    test_delegation_elevation()
    test_scoped_inventory_and_links()
    test_catalog_and_registries()

    elapsed = time.perf_counter() - start_time
    print(f"=== ALL MASTER REFINEMENT CHECKS PASSED DETERMINISTICALLY in {elapsed:.3f}s ===")
    print("Scope: static contracts, dual-mode authoring, fence-aware link audits, and isolated safety invariants.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
