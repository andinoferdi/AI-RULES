#!/usr/bin/env python3
"""Grade Natural Writing eval outputs against docs/validation/natural-writing cases.

Each case `<id>` needs two files in the outputs directory:
  <id>.artifact.md  the artifact text only (the edited, written or reviewed text)
  <id>.reply.md     the full reply as delivered (artifact plus surrounding notes)

Checks per case, all from the case's `expect` block:
  compare_mode / max_verdict  skill checker `compare` verdict may not exceed max_verdict
  unchanged                   artifact equals input (whitespace at the ends and line endings ignored)
  must_contain                every substring present in the artifact (case-sensitive)
  must_not_contain            no substring present in the artifact (case-insensitive)
  must_contain_any            each group: at least one substring present in the artifact (case-insensitive)
  note_contains_any           each group: one substring present in the reply outside the artifact
  max_scan_hits               skill checker `scan` hint count may not exceed this value

This is a record of observed outputs, not a gate: exit 0 unless the inputs are unreadable.
Usage: python scripts/grade_natural_writing.py --cases CASES --outputs DIR --checker CHECK_PY [--json]
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

RANK = {"PASS": 0, "WARNING": 1, "NEEDS_REVIEW": 2, "FAIL": 3}


def _norm(text: str) -> str:
    return text.replace("\r\n", "\n").strip()


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("natural_writing_check", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def grade_case(case: dict, outputs: Path, checker) -> dict:
    expect = case["expect"]
    artifact_file = outputs / f"{case['id']}.artifact.md"
    reply_file = outputs / f"{case['id']}.reply.md"
    if not artifact_file.is_file():
        return {"id": case["id"], "result": "FAIL", "reasons": ["missing artifact output"], "verdict": None}
    artifact = artifact_file.read_text(encoding="utf-8-sig")
    reply = reply_file.read_text(encoding="utf-8-sig") if reply_file.is_file() else artifact
    note = reply.replace(artifact.strip(), "") if artifact.strip() else reply
    reasons = []
    # Surrounding whitespace is file framing, not an edit (review mode compares exactly).
    verdict = checker.check(_norm(case["input"]), _norm(artifact), expect["compare_mode"]).verdict
    if RANK[verdict] > RANK[expect["max_verdict"]]:
        reasons.append(f"compare {verdict} > {expect['max_verdict']}")
    if expect.get("unchanged") and _norm(artifact) != _norm(case["input"]):
        reasons.append("unchanged: artifact differs from input")
    for needle in expect.get("must_contain", []):
        if needle not in artifact:
            reasons.append(f"must_contain missing: {needle!r}")
    lowered = artifact.lower()
    for needle in expect.get("must_not_contain", []):
        if needle.lower() in lowered:
            reasons.append(f"must_not_contain present: {needle!r}")
    for group in expect.get("must_contain_any", []):
        if not any(item.lower() in lowered for item in group):
            reasons.append(f"must_contain_any none of: {group}")
    for group in expect.get("note_contains_any", []):
        if not any(item.lower() in note.lower() for item in group):
            reasons.append(f"note_contains_any none of: {group}")
    if "max_scan_hits" in expect:
        hits = checker.scan(artifact, case["lang"])
        if len(hits) > expect["max_scan_hits"]:
            reasons.append(f"scan hits {len(hits)} > {expect['max_scan_hits']}: "
                           + ", ".join(h.rule for h in hits))
    return {"id": case["id"], "result": "FAIL" if reasons else "PASS", "reasons": reasons, "verdict": verdict}


def grade(cases: list, outputs: Path, checker) -> dict:
    results = [grade_case(case, Path(outputs), checker) for case in cases]
    return {"passed": sum(r["result"] == "PASS" for r in results), "total": len(results), "cases": results}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--outputs", required=True, type=Path)
    parser.add_argument("--checker", required=True, type=Path, help="path to the skill's scripts/check.py")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        cases = json.loads(args.cases.read_text(encoding="utf-8"))["cases"]
        checker = load_module(args.checker)
    except (OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    report = grade(cases, args.outputs, checker)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for r in report["cases"]:
            print(f"{r['result']:4} {r['id']} ({r['verdict']})" + "".join(f"\n     - {x}" for x in r["reasons"]))
        print(f"{report['passed']}/{report['total']} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
