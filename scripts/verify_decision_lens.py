#!/usr/bin/env python3
"""Bounded static Decision Lens contract checks, NOT a natural-language router.

The ten raw prompts/reviewer expectations are preserved for future live evaluation.
This checks actual root/dispatch tables, index destinations and explicit collision
examples against frozen annotations. It never predicts autonomous model selection.
"""
import json
from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def outside_fences(text):
    """Return prose only, retaining line positions; ignore backtick/tilde fences."""
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


def plain(text):
    return re.sub(r"\s+", " ", text.replace("`", "").replace("*", "")).strip()


def lens_matrix(text):
    lines = outside_fences(text).splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith("| User Situation / Task Trigger |")]
    require(len(starts) == 1, "Exactly one real Decision Lens matrix required")
    start = starts[0]
    rows = []
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        cells = [plain(cell) for cell in line.strip().strip("|").split("|")]
        require(len(cells) == 4, "Decision Lens rows require four columns")
        rows.append(cells)
    require(len(rows) == 10, "Decision Lens requires ten situation rows")
    require(len(rows) + 2 < 40, "Decision Lens table must remain under 40 lines")
    return rows


def verify(root=REPO_ROOT):
    root = Path(root)
    fixture = json.loads((root / "tests/fixtures/decision_lens_cases.json").read_text(encoding="utf-8"))
    contract = json.loads((root / "tests/fixtures/decision_lens_contract.json").read_text(encoding="utf-8"))
    cases = fixture["cases"]
    require([c["id"] for c in cases] == list(range(1, 11)), "Original ten raw case IDs must remain 1..10")
    spec = (root / "docs/specs/skill-system-refinement.md").read_text(encoding="utf-8")
    # Cross-check raw prompts and reviewer routes against the approved §4.2, not
    # against a classifier written to return those same expectations.
    for case in cases:
        fields = ("prompt", "expected_route", "rationale")
        require(all(isinstance(case.get(k), str) and case[k].strip() for k in fields), f"Case {case['id']} has invalid raw fields")
        require(type(case.get("is_direct_bypass")) is bool, f"Case {case['id']} bypass must be boolean")
        row = next((line for line in spec.splitlines()
                    if line.startswith(f"| {case['id']} | *\"")), "")
        require(row, f"Approved raw case {case['id']} missing")
        cells = row.strip("|").split("|")
        require(plain(cells[1]).strip('"') == case["prompt"], f"Case {case['id']} raw prompt drifted from approved spec")
        require(case["expected_route"] in plain(cells[2]), f"Case {case['id']} reviewer expectation drifted")
        require(case["is_direct_bypass"] == (case["expected_route"] == "Direct Execution"), f"Case {case['id']} bypass annotation drifted")
    expected = contract["matrix"]
    matrices = {}
    for rel in ("SKILL.md", "references/method-dispatch.md"):
        rows = lens_matrix((root / rel).read_text(encoding="utf-8"))
        for want, actual in zip(expected, rows):
            require(actual == want, f"{rel}: {want[1]} contract mismatch: {actual!r}")
        matrices[rel] = {r[1]: r for r in rows}
    annotations = contract["case_annotations"]
    require([a["id"] for a in annotations] == list(range(1, 11)), "Ten independent phase annotations required")
    for case, annotation in zip(cases, annotations):
        row = matrices["SKILL.md"][annotation["phase"]]
        route = annotation["route"]
        require(route == case["expected_route"], f"Case {case['id']} reviewer annotation mismatch")
        require(route in (row[3] if annotation.get("negative_gate") else row[2]), f"Case {case['id']} missing from actual lens contract")

    index = outside_fences((root / "references/internal-method-index.md").read_text(encoding="utf-8"))
    routes = {c["expected_route"] for c in cases} | {"andino-code-review"}
    for route in sorted(routes - {"Direct Execution", "search-first"}):
        name = route.removeprefix("andino-")
        link = f"[{name}](../skills/{name}/SKILL.md)"
        require(link in index, f"Index does not resolve {route}")
        path = root / "skills" / name / "SKILL.md"
        require(path.is_file(), f"Index target missing: {path}")
        require(f"name: andino-{name}" in path.read_text(encoding="utf-8"), f"Index identity mismatch: {path}")
    for alias in ("method-authoring", "writing-skills", "skill-maker"):
        require(f"| {alias} | [skill-maker](../skills/skill-maker/SKILL.md) |" in index, f"Legacy alias {alias} no longer resolves to skill-maker")

    dispatch = outside_fences((root / "references/method-dispatch.md").read_text(encoding="utf-8"))
    for collision in contract["collisions"]:
        exact = f'*"{collision["prompt"]}"* -> {collision["documented_outcome"]}'
        require(exact in dispatch, f"Documented collision missing/drifted: {collision['prompt']}")
    require("NOT_VERIFIED" in dispatch, "Dispatch must distinguish static checks from live model proof")
    return {"raw_cases": len(cases), "matrix_rows": len(expected),
            "collision_examples": len(contract["collisions"]),
            "static_contract": "PASS", "live_model_routing": "NOT_VERIFIED"}


def main():
    try:
        result = verify()
    except (AssertionError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"[FAIL] STATIC Decision Lens: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    print("ALL 10 DECISION LENS CASES PASSED")
    print("STATIC DECISION LENS CONTRACT PASSED; live model routing NOT_VERIFIED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
