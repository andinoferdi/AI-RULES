#!/usr/bin/env python3
"""Floor-guard battery for the constraint-driven-development upgrade.

Usage: python -I battery.py <dir> [--json <out.json>]

A regression suite for the reference guards this repository ships in the skill (the current
and the candidate versions), run on guard files extracted into <dir>/scripts/. It is not run on
code taken from third-party repositories. Every guard found at <dir>/scripts/floor-guard.mjs
and <dir>/scripts/floor_guard.py runs against the scenarios below. Each scenario is a fresh git repository in a temporary directory whose base
commit on `main` holds the arm's whole scripts/ folder, fixture/task2/CONSTRAINTS.md and a few
source and test files with pre-existing suppressions. The guard runs from the repository root
as `<runtime> scripts/<guard> --base <ref>`.

A scenario passes when every guard present exits with the expected code and, where the
scenario says so, prints nothing that contains the fake key. With no guard file every scenario
fails. Exit codes: 0 clean, 1 violation, 2 the guard could not run.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONSTRAINTS = (HERE / "fixture" / "task2" / "CONSTRAINTS.md").read_text(encoding="utf-8")
KEY = "lk_live_EXAMPLE_ONLY_7Q2X"
LEAK_MARKER = "EXAMPLE_ONLY"

BASE = {
    "CONSTRAINTS.md": CONSTRAINTS,
    "src/app.ts": "export function add(a: number, b: number): number {\n  return a + b;\n}\n",
    "src/legacy.ts": (
        "/* eslint-disable @typescript-eslint/no-explicit-any */\n"
        "// @ts-ignore -- pre-existing\n"
        "export const legacy: any = JSON.parse(\"{}\");\n"
        "// TODO(LED-1): remove\n"
    ),
    "tests/app.test.ts": (
        "import { expect, it } from \"vitest\";\n"
        "import { add } from \"../src/app\";\n"
        "\n"
        "it(\"adds\", () => {\n"
        "  expect(add(1, 2)).toBe(3);\n"
        "  expect(add(-1, 1)).toBe(0);\n"
        "});\n"
    ),
    "worker/jobs.py": "def total(rows):  # type: ignore[no-untyped-def]\n    return sum(rows)  # noqa: E501\n",
    "worker/tests/test_jobs.py": "from jobs import total\n\n\ndef test_total():\n    assert total([1, 2]) == 3\n",
    "worker/tests/test_rounding.py": "def test_round():\n    assert round(2.5) == 2\n",
}


def replace(text, old, new):
    if text.count(old) != 1:
        raise SystemExit(f"battery fixture error: {old!r} not found exactly once")
    return text.replace(old, new)


# Each change: (path, function from old text to new text, or None to delete, mode).
# Modes: "commit" (committed on the feature branch), "stage" (git add, not committed),
# "untracked" (written, never added).
SCENARIOS = [
    {"id": "G1", "name": "clean change; base has pre-existing suppressions", "expect": 0, "changes": [
        ("src/app.ts", lambda t: t + "\nexport function sub(a: number, b: number): number {\n  return a - b;\n}\n", "commit"),
        ("tests/app.test.ts", lambda t: t + "\nit(\"subtracts\", () => {\n  expect(1 - 1).toBe(0);\n});\n", "commit"),
    ]},
    {"id": "G2", "name": "untracked new file adds @ts-ignore", "expect": 1, "changes": [
        ("src/new.ts", lambda t: "// @ts-ignore\nexport const n: number = \"x\" as unknown as number;\n", "untracked"),
    ]},
    {"id": "G3", "name": "staged, uncommitted .skip(", "expect": 1, "changes": [
        ("tests/app.test.ts", lambda t: t + "\nit.skip(\"later\", () => {});\n", "stage"),
    ]},
    {"id": "G4", "name": "comparison ref does not exist", "expect": 2, "base": "origin/missing-ref", "changes": []},
    {"id": "G5", "name": "CONSTRAINTS.md minimum lowered (>= 80% to >= 75%, written with the >= sign)", "expect": 1, "changes": [
        ("CONSTRAINTS.md", lambda t: replace(t, "changed lines ≥ 80% covered", "changed lines ≥ 75% covered"), "commit"),
    ]},
    {"id": "G6", "name": "CONSTRAINTS.md minimum raised (>= 80% to >= 85%) is silent", "expect": 0, "changes": [
        ("CONSTRAINTS.md", lambda t: replace(t, "changed lines ≥ 80% covered", "changed lines ≥ 85% covered"), "commit"),
    ]},
    {"id": "G7", "name": "ratchet tolerance raised (0.5 to 1.5)", "expect": 1, "changes": [
        ("CONSTRAINTS.md", lambda t: replace(t, "| 61.7% | must not fall | 0.5 |", "| 61.7% | must not fall | 1.5 |"), "commit"),
    ]},
    {"id": "G8", "name": "suppression on a line holding a key; output must not show the key", "expect": 1, "no_leak": True, "changes": [
        ("src/app.ts", lambda t: t + f"\nconst key: string = \"{KEY}\"; // eslint-disable-line\nexport {{ key }};\n", "commit"),
    ]},
    {"id": "G9", "name": "Python # type: ignore added", "expect": 1, "changes": [
        ("worker/jobs.py", lambda t: t + "\n\ndef render(rows):\n    return str(total(rows))  # type: ignore[arg-type]\n", "commit"),
    ]},
    {"id": "G10", "name": "Python @pytest.mark.skip added", "expect": 1, "changes": [
        ("worker/tests/test_jobs.py", lambda t: replace(
            "import pytest\n\n" + t, "def test_total():", "@pytest.mark.skip(reason=\"flaky\")\ndef test_total():"), "commit"),
    ]},
    {"id": "G11", "name": "assertion removed from a test that stays", "expect": 1, "changes": [
        ("tests/app.test.ts", lambda t: replace(t, "  expect(add(-1, 1)).toBe(0);\n", ""), "commit"),
    ]},
    {"id": "G12", "name": "Python stub raises NotImplementedError", "expect": 1, "changes": [
        ("worker/jobs.py", lambda t: t + "\n\ndef export(rows):\n    raise NotImplementedError(\"export is not implemented yet\")\n", "commit"),
    ]},
    {"id": "G13", "name": "Python test file test_rounding.py deleted", "expect": 1, "changes": [
        ("worker/tests/test_rounding.py", None, "commit"),
    ]},
]


def git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True, stdin=subprocess.DEVNULL,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def write(repo, rel, text):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def build(root, scripts_dir, scenario):
    repo = root / scenario["id"]
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "battery@example.invalid")
    git(repo, "config", "user.name", "battery")
    git(repo, "config", "core.autocrlf", "false")
    for rel, text in BASE.items():
        write(repo, rel, text)
    shutil.copytree(scripts_dir, repo / "scripts")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "base")
    git(repo, "switch", "-q", "-c", "feature")
    for rel, change, mode in scenario["changes"]:
        path = repo / rel
        if change is None:
            path.unlink()
        else:
            write(repo, rel, change(path.read_text(encoding="utf-8") if path.exists() else ""))
        if mode in ("commit", "stage"):
            git(repo, "add", "-A", "--", rel)
        if mode == "commit":
            git(repo, "commit", "-q", "-m", f"change {rel}")
    return repo


def run_guard(repo, guard, base):
    runtime = "node" if guard.endswith(".mjs") else sys.executable
    try:
        proc = subprocess.run([runtime, f"scripts/{guard}", "--base", base], cwd=repo,
                              stdin=subprocess.DEVNULL, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=60)
    except subprocess.TimeoutExpired:
        return {"exit": "timeout", "output": ""}
    return {"exit": proc.returncode, "output": (proc.stdout + proc.stderr)[-4000:]}


def main():
    args = sys.argv[1:]
    json_out = None
    if "--json" in args:
        i = args.index("--json")
        json_out = args[i + 1]
        del args[i:i + 2]
    if len(args) != 1:
        raise SystemExit(__doc__)
    arm_repo = Path(args[0]).resolve()
    scripts_dir = arm_repo / "scripts"
    guards = [g for g in ("floor-guard.mjs", "floor_guard.py") if (scripts_dir / g).is_file()]
    results = []
    with tempfile.TemporaryDirectory(prefix="cdd-battery-") as tmp:
        for scenario in SCENARIOS:
            row = {"id": scenario["id"], "name": scenario["name"], "expect": scenario["expect"],
                   "guards": {}, "pass": False}
            if guards:
                repo = build(Path(tmp), scripts_dir, scenario)
                ok = True
                for guard in guards:
                    res = run_guard(repo, guard, scenario.get("base", "main"))
                    leaked = LEAK_MARKER in res["output"]
                    res["leaked_key"] = leaked
                    row["guards"][guard] = res
                    ok = ok and res["exit"] == scenario["expect"] and not (scenario.get("no_leak") and leaked)
                row["pass"] = ok
            results.append(row)
    for row in results:
        exits = ", ".join(f"{g}={r['exit']}{' LEAK' if r['leaked_key'] else ''}" for g, r in row["guards"].items()) or "no guard"
        print(f"{row['id']:<4} {'PASS' if row['pass'] else 'FAIL'}  expect {row['expect']}  [{exits}]  {row['name']}")
    passed = sum(r["pass"] for r in results)
    print(f"guards: {', '.join(guards) or 'none'}; passed {passed} of {len(results)}")
    if json_out:
        Path(json_out).write_text(json.dumps({"guards": guards, "results": results}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
