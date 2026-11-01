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
import hashlib
from pathlib import Path
import stat
import tempfile

CHILD_TIMEOUT = 30


def run_child(arguments, *, cwd, env=None):
    child_env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1',
                     GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                     GIT_TERMINAL_PROMPT='0')
    # Do not let inherited Git routing variables redirect fixture writes.
    for key in list(child_env):
        if key.startswith(('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY',
                           'GIT_ALTERNATE_OBJECT_DIRECTORIES', 'GIT_CONFIG_COUNT', 'GIT_CONFIG_KEY_',
                           'GIT_CONFIG_VALUE_')):
            child_env.pop(key)
    if env:
        child_env.update(env)
    try:
        return subprocess.run(arguments, cwd=cwd, env=child_env, capture_output=True,
                              text=True, encoding='utf-8', errors='replace', timeout=CHILD_TIMEOUT)
    except subprocess.TimeoutExpired as error:
        raise AssertionError(f'Child timed out after {CHILD_TIMEOUT}s: {arguments[0]}') from error


def tree_snapshot(path):
    """Record existence, paths, types, permissions and file bytes, including caches."""
    path = Path(path)
    if not path.exists():
        return None
    result = {}
    for item in [path, *sorted(path.rglob('*'))]:
        relative = item.relative_to(path).as_posix()
        mode = stat.S_IMODE(item.lstat().st_mode)
        if item.is_symlink():
            result[relative] = ('link', mode, os.readlink(item))
        elif item.is_dir():
            result[relative] = ('dir', mode)
        else:
            result[relative] = ('file', mode, hashlib.sha256(item.read_bytes()).hexdigest())
    return result


def source_cache_snapshot(root):
    root = Path(root)
    return {str(p.relative_to(root)): tree_snapshot(p) for p in sorted(root.rglob('__pycache__'))
            if '.git' not in p.parts} | {
                str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(root.rglob('*.pyc')) if '.git' not in p.parts}


def is_within(path, parent):
    path, parent = Path(path).resolve(), Path(parent).resolve()
    return path != parent and parent in path.parents

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
        assert_true(bool(Path(fpath).read_text(encoding='utf-8').strip()), f"Resource file {filename} is nonempty")

def test_worked_example_harness():
    we_path = os.path.join(REPO_ROOT, "skills", "delegation", "resources", "worked-example.md")
    with open(we_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"```python andino-worked-example-verification\n(.*?)\n```", content, re.DOTALL)
    assert_true(match is not None, "Extracted worked-example Python test harness")
    code = match.group(1)

    # Execute the real example, then assert independent outputs of its public functions.
    # Its ANDINO_NEGATIVE flag only forces sys.exit(1); that is not defect detection.
    with tempfile.TemporaryDirectory() as temporary:
        proc = run_child([sys.executable, '-B', '-c', code], cwd=temporary)
        assert_true(proc.returncode == 0 and 'SUCCESS: Delegation DAG' in proc.stdout,
                    'Worked example runs successfully in disposable storage')
        probe = code + '''
assert compute_frontier([{'id':'a','deps':[]},{'id':'b','deps':['a']}], set()) == ['a']
assert compute_frontier([{'id':'a','deps':[]},{'id':'b','deps':['a']}], {'a'}) == ['b']
assert compute_frontier([{'id':'a','deps':[]},{'id':'b','deps':['a']}], {'a','b'}) == []
assert has_write_collision(['src/auth'], ['src/auth/token.py'])
assert has_write_collision(['src/auth/token.py'], ['src/auth'])
assert not has_write_collision(['src/auth'], ['src/authentication'])
print('PUBLIC_EXAMPLE_FUNCTIONS_VERIFIED')
'''
        probe = "__name__ = 'fixture'\n" + probe
        result = run_child([sys.executable, '-B', '-c', probe], cwd=temporary)
        assert_true(result.returncode == 0 and 'PUBLIC_EXAMPLE_FUNCTIONS_VERIFIED' in result.stdout,
                    'DAG dependencies/completion and component-boundary path collisions verified')

def test_helper_scripts():
    root = Path(REPO_ROOT)
    scripts_dir = root / 'skills/delegation/scripts'
    before_andino = tree_snapshot(root / '.andino')
    before_source = tree_snapshot(scripts_dir)
    before_caches = source_cache_snapshot(root)
    try:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary)
            repo = fixture / 'git-fixture'
            repo.mkdir()
            workspace_base = fixture / 'workspaces'
            sibling = workspace_base / 'sibling'
            sibling.mkdir(parents=True)
            sentinel = sibling / 'preserve.txt'
            sentinel.write_bytes(b'sibling workspace must survive\n')
            # Real repository .andino is only observed; sentinels exist ONLY in fixture.
            (repo / '.andino').mkdir()
            (repo / '.andino/plan.txt').write_bytes(b'fixture plan remains\n')
            fixture_andino = tree_snapshot(repo / '.andino')
            sibling_before = tree_snapshot(sibling)
            env = {'ANDINO_WORKSPACE_OVERRIDE': str(workspace_base)}

            def git(*args):
                result = run_child(['git', '-c', 'core.hooksPath=' + str(fixture / 'no-hooks'),
                                    '-c', 'commit.gpgSign=false', '-c', 'user.name=Verifier Fixture',
                                    '-c', 'user.email=fixture@example.invalid', *args], cwd=repo)
                assert_true(result.returncode == 0, f'Fixture Git {args[0]} succeeds: {result.stderr[:300]}')
                return result.stdout.strip()

            git('init', '--quiet')
            (repo / 'payload.txt').write_text('before\n', encoding='utf-8')
            git('add', 'payload.txt')
            git('commit', '--quiet', '-m', 'fixture baseline')
            base = git('rev-parse', 'HEAD')
            (repo / 'payload.txt').write_text('after\n', encoding='utf-8')
            git('add', 'payload.txt')
            git('commit', '--quiet', '-m', 'fixture changed payload')
            head = git('rev-parse', 'HEAD')
            # Reverse range HEAD..BASE is a concrete non-ancestor case; no branch writes.
            plan = repo / 'plan.md'
            task = '### Task 1: Isolate helpers\nKeep literal task content.\n```text\n### Task 99: fenced decoy\n```\n\n'
            plan.write_text('# Disposable Plan\n\n' + task + '### Task 2: Do not include\nExcluded task body.\n', encoding='utf-8')

            def helper(name, *args):
                return run_child([sys.executable, '-B', str(scripts_dir / name), str(plan), *args], cwd=repo, env=env)

            resolved = helper('delegation_workspace.py')
            assert_true(resolved.returncode == 0, f'Workspace helper succeeds: {resolved.stderr[:300]}')
            workspace = Path(resolved.stdout.strip())
            assert_true(is_within(workspace, workspace_base), 'Workspace is an actual descendant of override, not a substring match')
            assert_true((workspace / 'plan-path').read_text(encoding='utf-8').strip() == 'plan.md', 'Workspace records correct fixture plan ownership')
            assert_true(helper('delegation_workspace.py').stdout.strip() == resolved.stdout.strip(), 'Workspace resolution is idempotent')
            brief = helper('task_brief.py', '1')
            assert_true(brief.returncode == 0, f'Task brief helper succeeds: {brief.stderr[:300]}')
            assert_true((workspace / 'task-1-brief.md').read_text(encoding='utf-8') == task,
                        'Task brief contains exact selected task and fenced decoy, excludes next task')
            missing = helper('task_brief.py', '404')
            assert_true(missing.returncode == 3 and 'not found' in missing.stderr,
                        'Missing task returns public error 3')
            assert_true(not (workspace / 'task-404-brief.md').exists(), 'Missing task produces no brief artifact')

            package = helper('review_package.py', base, head)
            assert_true(package.returncode == 0, f'Review package helper succeeds: {package.stderr[:300]}')
            package_path = workspace / f'review-{base[:7]}..{head[:7]}.diff'
            content = package_path.read_text(encoding='utf-8')
            assert_true(is_within(package_path, workspace_base) and all(value in content for value in
                        ('## Commits', 'fixture changed payload', '## Files Changed', 'payload.txt',
                         '## Net Unified Diff', '-before', '+after')),
                        'Valid review package contains real commit, stat and unified diff content')
            for label, low, high, expected_code, error_text in (
                ('empty', head, head, 3, 'empty'),
                ('invalid', 'definitely-not-a-valid-ref', head, 2, 'invalid git ref'),
                ('non-ancestor', head, base, 3, 'not a descendant'),
            ):
                before_reject = tree_snapshot(workspace_base)
                rejected = helper('review_package.py', low, high)
                assert_true(rejected.returncode == expected_code and error_text in rejected.stderr,
                            f'Review package rejects {label} range with public error {expected_code}')
                assert_true(tree_snapshot(workspace_base) == before_reject, f'{label} review range writes no artifacts')
            assert_true(tree_snapshot(sibling) == sibling_before, 'Sibling workspace sentinel survives all helpers')
            assert_true(tree_snapshot(repo / '.andino') == fixture_andino, 'Fixture repository .andino remains unchanged')
    finally:
        assert_true(tree_snapshot(root / '.andino') == before_andino, 'Actual repository .andino before/after snapshot identical')
        assert_true(tree_snapshot(scripts_dir) == before_source, 'Helper source tree including caches before/after identical')
        assert_true(source_cache_snapshot(root) == before_caches, 'Repository source import-cache inventory before/after identical')

    for wrapper in ('delegation-workspace', 'task-brief', 'review-package'):
        assert_true((scripts_dir / wrapper).is_file(), f'Shell wrapper {wrapper} exists')


def test_readonly_cleanup():
    # Python 3.12 TemporaryDirectory already resets read-only permissions at cleanup.
    # This checks an actual Windows read-only file, not open-handle/locked-file behavior.
    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        protected = directory / 'readonly.txt'
        protected.write_text('read-only cleanup fixture', encoding='utf-8')
        protected.chmod(stat.S_IREAD)
        assert_true(not (protected.stat().st_mode & stat.S_IWRITE), 'Fixture file is read-only before cleanup')
    assert_true(not directory.exists(), 'TemporaryDirectory removes read-only fixture without custom cleanup')

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
    test_readonly_cleanup()
    test_references_and_catalog()
    elapsed = time.perf_counter() - start
    print(f"=== ALL VERIFICATION CHECKS PASSED DETERMINISTICALLY in {elapsed:.3f}s ===")
    print('Scope: static artifacts + isolated helper behavior; live model delegation NOT_VERIFIED')
    sys.exit(0)
