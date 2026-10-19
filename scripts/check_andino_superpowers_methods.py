"""Apply emitted Andino method examples in disposable stdlib fixtures.

These are deterministic procedural demonstrations, not LLM routing/compliance
evaluations or proof of live host capabilities. No Git or network mutations.
"""
from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory

IDS = (
    "tdd", "debugging", "code-review", "planning", "delegation",
    "plan-execution", "verification", "git-isolation", "delivery",
    "session-diagnostics", "method-authoring",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_case(runtime: Path, method: str) -> tuple[dict, str]:
    path = runtime / "skills" / method / "GUIDE.md"
    content = path.read_text(encoding="utf-8")
    fence = chr(96) * 3
    match = re.search(fence + r"andino-example\n(.*?)\n" + fence, content, re.S)
    if not match:
        raise AssertionError(f"{method}: no runnable worked example")
    return json.loads(match.group(1)), digest(path.read_bytes())


def unit_run(folder: Path, source: str, tests: str) -> dict:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "subject.py").write_text(source, encoding="utf-8")
    (folder / "test_contract.py").write_text(tests, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "unittest", "discover", "-s", ".", "-v"],
        cwd=folder, capture_output=True, text=True, timeout=20,
    )
    return {
        "command": [Path(sys.executable).name, "-B", "-m", "unittest",
                    "discover", "-s", ".", "-v"],
        "exit_code": proc.returncode,
        "output": (proc.stdout + proc.stderr).strip(),
        "source_sha256": digest((folder / "subject.py").read_bytes()),
    }


def red(run: dict, reason: str) -> None:
    assert run["exit_code"] != 0, "Expected RED was green"
    assert "AssertionError" in run["output"], run
    assert reason in run["output"], run
    assert "ImportError" not in run["output"], run
    assert "ModuleNotFoundError" not in run["output"], run
    assert "SyntaxError" not in run["output"], run
    assert "Ran 1 test" in run["output"], run


def green(run: dict) -> None:
    assert run["exit_code"] == 0, run
    assert "Ran 1 test" in run["output"], run
    assert run["output"].endswith("OK"), run


def program(folder: Path, source: str, statement: str) -> dict:
    (folder / "subject.py").write_text(source, encoding="utf-8")
    proc = subprocess.run([sys.executable, "-B", "-c", statement],
                          cwd=folder, text=True, capture_output=True, timeout=20)
    assert proc.returncode == 0, proc.stderr
    return {"exit_code": proc.returncode, "output": proc.stdout.strip()}


def dag(tasks: list[dict]) -> list[list[str]]:
    nodes = {t["id"]: t for t in tasks}
    assert len(nodes) == len(tasks), "duplicate task"
    for task in tasks:
        assert set(task["deps"]) <= nodes.keys(), "dangling dependency"
    remaining = set(nodes)
    completed: set[str] = set()
    levels = []
    while remaining:
        ready = sorted(i for i in remaining
                       if set(nodes[i]["deps"]) <= completed)
        assert ready, "dependency cycle"
        levels.append(ready)
        completed.update(ready)
        remaining.difference_update(ready)
    return levels


def overlap(a: str, b: str) -> bool:
    # Project-relative ownership; normalize separators, dots and case on this
    # Windows-oriented host without touching source checkout paths.
    def parts(value: str) -> tuple[str, ...]:
        normalized = value.replace("\\", "/")
        result = []
        assert not normalized.startswith("/"), "absolute ownership path"
        for part in normalized.split("/"):
            if part in ("", "."):
                continue
            assert part != "..", "ownership escapes workspace"
            result.append(part.casefold())
        return tuple(result)
    left, right = parts(a), parts(b)
    return left == right or left == right[:len(left)] or right == left[:len(right)]


def disjoint(tasks: list[dict]) -> bool:
    for n, task in enumerate(tasks):
        for other in tasks[n + 1:]:
            if any(overlap(a, b) for a in task["files"] for b in other["files"]):
                return False
    return True


def expect_rejected(operation, expected: str) -> str:
    try:
        operation()
    except AssertionError as exc:
        assert expected in str(exc), str(exc)
        return str(exc)
    raise AssertionError(f"Expected rejection: {expected}")


def apply_tdd(case: dict, folder: Path) -> dict:
    first = unit_run(folder, case["red_source"], case["test_source"])
    red(first, case["expected_failure"])
    second = unit_run(folder, case["green_source"], case["test_source"])
    green(second)
    # Separate gate: unchanged behavioral contract and same public function.
    reviewed = unit_run(folder, case["refactor_source"], case["test_source"])
    green(reviewed)
    mutant = unit_run(folder, case["red_source"], case["test_source"])
    red(mutant, case["expected_failure"])
    assert case["oracle"] == 15
    return {"red": first, "green": second, "separate_refactor_gate": reviewed,
            "mutation_killed": mutant, "oracle": "known literal 15 for [10,5]"}


def apply_debugging(case: dict, folder: Path) -> dict:
    original = unit_run(folder, case["faulty_source"], case["test_source"])
    red(original, case["expected_failure"])
    a, b, key = case["probe"]
    statement = ("from subject import lookup; import json; print(json.dumps("
                 f"[lookup({a!r},{key!r}),lookup({b!r},{key!r})]))")
    observed = program(folder, case["faulty_source"], statement)
    assert json.loads(observed["output"]) == ["A:7", "A:7"]
    # Distinguishing probe changes only tenant identity in the cache key.
    probe = program(folder, case["fixed_source"], statement)
    assert json.loads(probe["output"]) == ["A:7", "B:7"]
    fixed = unit_run(folder, case["fixed_source"], case["test_source"])
    green(fixed)
    mutant = unit_run(folder, case["faulty_source"], case["test_source"])
    red(mutant, case["expected_failure"])
    return {"exact_repro": original, "observed_two_callers": observed,
            "hypothesis": case["hypothesis"], "distinguishing_probe": probe,
            "regression_and_original_scenario": fixed, "mutation_killed": mutant,
            "limit": "Synthetic multi-tenant cache, no production environment measured"}


def apply_review(case: dict, folder: Path) -> dict:
    folder.mkdir(parents=True, exist_ok=True)
    baseline = folder / "base.py"
    baseline.write_text(case["base_source"], encoding="utf-8")
    candidate = folder / "candidate.py"
    candidate.write_text(case["candidate_source"], encoding="utf-8")
    snapshot = {"candidate.py": digest(candidate.read_bytes())}
    for name, content in case["untracked"].items():
        path = folder / name
        path.write_text(content, encoding="utf-8")
        snapshot[name] = digest(path.read_bytes())
    diff = "".join(difflib.unified_diff(
        baseline.read_text().splitlines(True),
        candidate.read_text().splitlines(True), fromfile="base", tofile="candidate"))
    assert diff and "helper.py" in snapshot
    contract = unit_run(folder, candidate.read_text(), case["test_source"])
    red(contract, "None != 0")
    tree = ast.parse(candidate.read_text())
    eval_lines = [n.lineno for n in ast.walk(tree)
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                  and n.func.id == "eval"]
    boundary_lines = [n.lineno for n in ast.walk(tree)
                      if isinstance(n, ast.If)
                      and isinstance(n.test, ast.Compare)
                      and any(isinstance(op, ast.GtE) for op in n.test.ops)]
    assert eval_lines == [case["expected_standards_line"]] == [2]
    assert boundary_lines == [case["expected_spec_line"]] == [3]
    findings = [
        {"axis": "Spec", "verdict": "FAIL", "file": "candidate.py", "line": 3,
         "trigger": "spend(10,10)", "expected": 0, "observed": None,
         "effect": "Valid exact-balance spend is rejected",
         "remedy": "Reject only amount > balance"},
        {"axis": "Standards", "verdict": "FAIL", "file": "candidate.py", "line": 2,
         "rule": case["standards"], "effect": "Input evaluation violates policy",
         "remedy": "Remove eval and preserve numeric public input contract"},
    ]
    fixed = unit_run(folder, case["fixed_source"], case["test_source"])
    green(fixed)
    assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                   and n.func.id == "eval" for n in ast.walk(ast.parse(case["fixed_source"])))
    candidate.write_text(case["fixed_source"], encoding="utf-8")
    assert digest(candidate.read_bytes()) != snapshot["candidate.py"]
    return {"working_snapshot_including_new_files": snapshot, "diff": diff,
            "spec_regression": contract, "independent_axis_findings": findings,
            "fixed_contract": fixed, "post_review_drift_detected": True,
            "limit": "Procedural review of planted defect, not independent LLM review"}


def apply_planning(case: dict, folder: Path) -> dict:
    levels = dag(case["tasks"])
    assert levels == [["create"], ["audit", "list"]]
    nodes = {t["id"]: t for t in case["tasks"]}
    for task in case["tasks"]:
        produced = {sig for dep in task["deps"] for sig in nodes[dep]["produces"]}
        assert set(task["consumes"]) <= produced, "unmet interface"
    cycle = expect_rejected(lambda: dag(case["bad_cycle"]), "cycle")
    dangling = expect_rejected(lambda: dag(case["dangling"]), "dangling")
    assert disjoint([nodes["audit"], nodes["list"]])
    return {"frontiers": levels, "interface_compatibility": "matched",
            "cycle_rejected": cycle, "dangling_rejected": dangling,
            "independent_after_create": ["audit", "list"]}


def apply_delegation(case: dict, folder: Path) -> dict:
    levels = dag(case["tasks"])
    ready = [t for t in case["tasks"] if t["id"] in levels[0]]

    def select(tasks, authorized, capability, cap):
        if not authorized or not capability or not disjoint(tasks):
            return []
        return tasks[:min(cap, 3)]

    selected = select(ready, case["authorized"], case["capability"],
                      case["max_children"])
    assert [t["id"] for t in selected] == ["api", "docs"]
    assert not disjoint(case["overlap"]), "ancestor ownership collision missed"
    assert not disjoint([{"files": ["SRC/shared.py"]}, {"files": ["src/./shared.py"]}])
    assert not select(ready, False, True, 3)
    assert not select(ready, True, False, 3)
    assert not select(case["overlap"], True, True, 3)
    many = [{"id": str(n), "files": [f"file-{n}.py"]} for n in range(5)]
    assert [t["id"] for t in select(many, True, True, 9)] == ["0", "1", "2"]
    return {"ready_selected": [t["id"] for t in selected],
            "dependent_ui_not_selected": "ui" not in [t["id"] for t in selected],
            "ancestor_and_normalized_overlap_rejected": True,
            "denied_or_missing_tool_fallback": "inline",
            "live_children_spawned": 0,
            "limit": "Scheduling/ownership procedure only; no real agent dispatch in checker"}


def apply_execution(case: dict, folder: Path) -> dict:
    folder.mkdir(parents=True, exist_ok=True)
    for name, content in case["files"].items():
        (folder / name).write_text(content, encoding="utf-8", newline="\n")
    evidence = {t["id"]: {"path": t["path"], "hash": digest(t["content"].encode())}
                for t in case["completed"]}
    def current():
        return {tid for tid, item in evidence.items()
                if digest((folder / item["path"]).read_bytes()) == item["hash"]}
    complete = current()
    assert complete == {"create"}
    assert set(case["next_task"]["deps"]) <= complete
    preserved = digest((folder / "created.py").read_bytes())
    # Apply resume: select list and leave already evidenced create untouched.
    selected = (case["next_task"]["id"]
                if set(case["next_task"]["deps"]) <= complete else None)
    assert selected == "list" and digest((folder / "created.py").read_bytes()) == preserved
    (folder / "created.py").write_text(case["drift_content"], encoding="utf-8")
    assert current() == set()
    assert not set(case["next_task"]["deps"]) <= current()
    return {"plan_id": case["plan_id"], "unchanged_task_skipped": "create",
            "selected_next": selected, "create_hash": preserved,
            "drift_invalidates_producer_and_blocks_list": True}


def apply_verification(case: dict, folder: Path) -> dict:
    run = unit_run(folder, case["source"], case["test"])
    green(run)
    source = folder / "subject.py"
    recorded = digest(source.read_bytes())
    source.write_text(case["changed_source"], encoding="utf-8")
    stale = digest(source.read_bytes()) != recorded
    assert stale
    failed = unit_run(folder, case["changed_source"], case["test"])
    red(failed, "16 != 15")
    return {"claim": case["criterion"], "verified": run,
            "tested_sha256": recorded, "stale_evidence_rejected": stale,
            "current_changed_behavior": failed}


def apply_isolation(case: dict, folder: Path) -> dict:
    classified = []
    for item in case["cases"]:
        result = ("submodule" if item["superproject"] else
                  ("linked" if item["git_dir"] != item["common"] else "ordinary"))
        assert result == item["expected"]
        classified.append(result)
    folder.mkdir(parents=True, exist_ok=True)
    allowed = (folder / case["allowed_root"]).resolve()
    allowed.mkdir()
    protected = (folder / case["protected"]).resolve()
    protected.mkdir()
    marker = protected / "user.txt"
    marker.write_text("preserve", encoding="utf-8")
    original = digest(marker.read_bytes())
    def target_ok(name):
        target = (folder / name).resolve()
        return (target != allowed and target.is_relative_to(allowed)
                and target != protected and not target.is_relative_to(protected))
    assert target_ok(case["safe"])
    assert not target_ok(case["unsafe"])
    assert not target_ok(case["protected"])
    assert digest(marker.read_bytes()) == original
    return {"metadata_classifications": classified,
            "contained_target_accepted": True,
            "outside_and_protected_targets_rejected": True,
            "user_marker_preserved": True, "git_mutations": 0,
            "limit": "Synthetic Git metadata plus real filesystem containment; no live worktree created"}


def apply_delivery(case: dict, folder: Path) -> dict:
    ready = all(c["state"] == "passed" for c in case["criteria"])
    assert ready
    actions = [name for name, allowed in case["permissions"].items() if allowed]
    assert actions == []
    blocked = case["criteria"] + [case["blocked"]]
    assert not all(c["state"] == "passed" for c in blocked)
    return {"implementation_ready": ready, "candidate": case["candidate"],
            "allowed_integration_actions": actions,
            "material_unverified_criterion_blocks_ready_claim": case["blocked"]["id"],
            "git_or_external_mutations": 0}


def apply_session(case: dict, folder: Path) -> dict:
    folder.mkdir(parents=True, exist_ok=True)
    records = []
    for original in case["records"]:
        item = dict(original)
        if "repeat_count" in item:
            item["text"] = item.pop("text_prefix") + item.pop("repeat") * item.pop("repeat_count")
        records.append(item)
    source = folder / "session.jsonl"
    source.write_text("".join(json.dumps(x) + "\n" for x in records), encoding="utf-8")
    before = digest(source.read_bytes())
    measured_bytes = source.stat().st_size
    with source.open("rb") as stream:
        sizes = [len(line) for line in stream]
    assert measured_bytes >= max(sizes)
    assert max(sizes) > 100000
    extracted = []
    placeholders = {}
    # Only this synthetic scenario's documented credential category. General
    # privacy classification is not claimed complete by this narrow example.
    token = re.compile(r"(?<=Bearer )[A-Za-z0-9_]+")
    def redact(match):
        value = match.group(0)
        if value not in placeholders:
            placeholders[value] = f"<SECRET-{len(placeholders) + 1}>"
        return placeholders[value]
    for line_no, line in enumerate(source.open(encoding="utf-8"), 1):
        record = json.loads(line)
        text = record["text"]
        # Locate signal without dumping giant record. Malicious text is never
        # executed or promoted to a shell/tool instruction.
        if case["signal"] in text:
            scrubbed = token.sub(redact, text)
            quote = scrubbed[:min(case["quote_limit"], case["record_limit"])]
            extracted.append({"line": line_no, "quote": quote,
                              "source": "session.jsonl", "classification": record["type"]})
    exported = folder / "report.json"
    exported.write_text(json.dumps(extracted), encoding="utf-8")
    assert len(extracted) == 1 and extracted[0]["line"] == 2
    assert case["signal"] in extracted[0]["quote"]
    assert len(extracted[0]["quote"]) <= case["quote_limit"]
    assert case["secret"] not in exported.read_text()
    assert "<SECRET-1>" in exported.read_text()
    assert digest(source.read_bytes()) == before
    return {"source_sha256_unchanged": before, "record_sizes": sizes,
            "bounded_findings": extracted, "secret_removed": True,
            "privacy_outcome": "synthetic credential category passed",
            "evidence_support": "tenant mismatch signal retained at original line 2",
            "hostile_record_actions": 0,
            "limit": "No live session inspected; narrow synthetic redaction, not privacy certification"}


def apply_authoring(case: dict, folder: Path) -> dict:
    required = set(case["record"]["required"])
    available = set(case["record"]["available"])
    missing = sorted(required - available)
    assert missing == ["limits", "tested_identity"]
    # This is an artifact-contract application under explicit synthetic
    # pressure, not an LLM response inferred from request keywords.
    publication_possible = case["authority"]["publish"] and not missing
    assert not publication_possible
    candidate = {"decision": ("withhold_publish_and_identify_missing_identity"
                              if not publication_possible
                              else "prepare_authorized_publication"),
                 "missing_fields": missing, "nested_agents": 0}
    assert candidate["decision"] == case["expected"]
    assert not case["authority"]["nested_agents"]
    return {"pressure": case["pressure_request"],
            "baseline_example": case["baseline_output"],
            "applied_artifact_contract": candidate,
            "publication_actions": 0,
            "fresh_context_control_runs": 0,
            "limit": "Procedural pressure walkthrough; provided baseline illustration is not an observed model control. LLM guidance effectiveness remains unverified."}


APPLY = {
    "tdd": apply_tdd, "debugging": apply_debugging, "code-review": apply_review,
    "planning": apply_planning, "delegation": apply_delegation,
    "plan-execution": apply_execution, "verification": apply_verification,
    "git-isolation": apply_isolation, "delivery": apply_delivery,
    "session-diagnostics": apply_session, "method-authoring": apply_authoring,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", type=Path,
                        default=Path(__file__).resolve().parents[2] / "AI-RULES")
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parents[1] /
                        "docs/validation/andino-unified/superpowers-operational.json")
    parser.add_argument('--methods', type=Path, default=Path(__file__).resolve().parents[1] /
                        'docs/validation/andino-unified/superpowers-methods.json')
    args = parser.parse_args()
    metadata_path = args.methods.resolve()
    owned = json.loads(metadata_path.read_text(encoding='utf-8'))
    metadata = {m['id']: m for m in owned}
    if set(metadata) != set(IDS) or len(owned) != len(IDS):
        raise ValueError('manifest must cover the 11 assigned methods exactly once')
    results = []
    with TemporaryDirectory(prefix="andino-superpowers-procedures-") as temp:
        for method in IDS:
            case, guide_hash = read_case(args.runtime, method)
            observed = APPLY[method](case, Path(temp) / method)
            results.append({"method": method, "status": "PASS",
                            "metadata_sha256": digest(json.dumps(metadata[method], sort_keys=True, separators=(',', ':')).encode()),
                            "evidence_type": "deterministic_procedural_application",
                            "guide_sha256": guide_hash,
                            "resource_sha256": {
                                str(path.relative_to(args.runtime)).replace("\\", "/"):
                                digest(path.read_bytes())
                                for path in sorted((args.runtime / "skills" / method /
                                                    "resources").rglob("*"))
                                if path.is_file()
                            },
                            "observed": observed})
    report = {
        "schema_version": 1, "source_family": "superpowers", "status": "PASS", "methods": results,
        "inputs": {"scripts/check_andino_superpowers_methods.py": digest(Path(__file__).read_bytes()),
                   metadata_path.relative_to(Path(__file__).resolve().parents[1]).as_posix(): digest(metadata_path.read_bytes())},
        "runtime": str(args.runtime.resolve()),
        "command": "python scripts/check_andino_superpowers_methods.py --runtime <runtime-root>",
        "method_count": len(results),
        "limits": [
            "No live host loading, real subagent dispatch, external service or production rollout tested.",
            "No fresh-context LLM control/candidate runs; raw-request routing and future agent compliance are not proved.",
            "Worked examples are synthetic and temporary; original repository/Git state is not mutated.",
            "Standard-library algorithms apply guide examples; structure or keyword presence is never scored as behavior proof.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(f"PASS: {len(results)} procedural method scenarios; {args.output}")
    print("LLM behavior/live-host evidence: NOT VERIFIED (see report limits)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
