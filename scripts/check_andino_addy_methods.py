"""Execute bounded Addy-derived procedures from emitted guides; no model/live claims."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

EXPECTED_IDS = {
    "api-and-interface-design", "browser-testing-with-devtools",
    "ci-cd-and-automation", "code-simplification",
    "constraint-driven-development", "context-engineering",
    "deprecation-and-migration", "documentation-and-adrs",
    "doubt-driven-development", "frontend-ui-engineering",
    "git-workflow-and-versioning", "idea-refine",
    "incremental-implementation", "observability-and-instrumentation",
    "performance-optimization", "security-and-hardening",
    "shipping-and-launch", "source-driven-development",
}
# Each control disables a load-bearing operation, not a heading or output label.
MUTATIONS = {
    "api-and-interface-design": ("if row:", "if False:", False, "ignore previously claimed intent"),
    "browser-testing-with-devtools": ("if status >= 500:", "if status >= 600:", False, "misclassify server status"),
    "ci-cd-and-automation": ('any(state[d] != "pass" for d in deps)', 'any(state[d] == "pass" for d in deps)', False, "invert prerequisite gate"),
    "code-simplification": ("return 2 * x", "return 3 * x", False, "change accepted numeric behavior"),
    "constraint-driven-development": ("if new_min < old_min:", "if new_min > old_min:", False, "invert minimum ratchet"),
    "context-engineering": ('sum(x["cost"] for x in required)>budget', 'sum(x["cost"] for x in required)<budget', False, "invert protected-context budget"),
    "deprecation-and-migration": ("if active_old == 0:", "if active_old >= 0:", True, "contract while legacy consumer remains"),
    "documentation-and-adrs": ("max(nums)+1", "max(nums)", False, "reuse existing ADR sequence number"),
    "doubt-driven-development": ('if f.get("contract_unclear"):', "if False:", False, "ignore contract-misread precedence"),
    "frontend-ui-engineering": ('if tag=="div" and "onclick" in a:', "if False:", True, "miss click-only nonsemantic action"),
    "git-workflow-and-versioning": ("paths & baseline", "paths & set()", True, "ignore pre-existing user change"),
    "idea-refine": ('o["dealbreaker_validated"]', "True", True, "recommend unvalidated dealbreaker"),
    "incremental-implementation": ("if any(not state.get(d) for d in deps):", "if False:", True, "execute before dependency is ready"),
    "observability-and-instrumentation": ('set(labels)-{"route","status_class","provider"}', "set()", True, "accept unbounded metric dimension"),
    "performance-optimization": ("b-a>noise", "b-a>0", True, "retain a gain inside measurement noise"),
    "security-and-hardening": (" or p==root", "", True, "permit owned root as destructive leaf"),
    "shipping-and-launch": ("error_now>2*error_base", "error_now>3*error_base", True, "advance rollback boundary too far"),
    "source-driven-development": ("if project_version!=docs_version:", "if False:", True, "accept documentation for wrong version"),
}

# Python audit hooks block network/process operations and writes outside the owned
# TemporaryDirectory. The examples are trusted repository code, not arbitrary input.
WRAPPER = r"""
import ast, json, os, sys
from pathlib import Path
root = Path.cwd().resolve()
prefixes = [Path(sys.base_prefix).resolve(), Path(sys.prefix).resolve()]
source = sys.stdin.read()
allowed = {"json","os","sqlite3","hashlib","pathlib","concurrent.futures","statistics","re","html.parser","itertools"}
for node in ast.walk(ast.parse(source)):
    if isinstance(node, ast.Import):
        if any(a.name not in allowed for a in node.names):
            raise RuntimeError("example import outside audited standard-library set")
    if isinstance(node, ast.ImportFrom):
        if node.module not in allowed:
            raise RuntimeError("example import outside audited standard-library set")
def inside(path, roots):
    try:
        p = Path(path).resolve()
        return any(p == r or p.is_relative_to(r) for r in roots)
    except (TypeError, ValueError, OSError):
        return False
def audit(event, args):
    if event.startswith(("socket.", "subprocess.", "os.system", "os.exec", "os.spawn")):
        raise RuntimeError("network and external process disabled")
    if event == "open" and not isinstance(args[0], int):
        path, mode, flags = args
        writing = bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if not inside(path, [root] if writing else [root, *prefixes]):
            raise RuntimeError("example file access outside owned temporary scope")
    if event in {"os.mkdir","os.remove","os.rmdir","os.rename","os.replace","os.symlink","os.link",
                 "os.chmod","os.chown","os.truncate","os.utime"}:
        if not inside(args[0], [root]):
            raise RuntimeError("example mutation outside temporary scope")
        if event in {"os.rename","os.replace","os.symlink","os.link"} and not inside(args[1],[root]):
            raise RuntimeError("example target outside temporary scope")
    if event == "sqlite3.connect":
        if args[0] != ":memory:" and not inside(args[0],[root]):
            raise RuntimeError("SQLite path outside temporary scope")
sys.addaudithook(audit)
exec(compile(source, "<guide-operational-example>", "exec"), {"__name__":"__main__"})
"""


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def example_code(text: str) -> str:
    marker = "\x60\x60\x60python andino-operational-example\n"
    if text.count(marker) != 1:
        raise ValueError("guide must contain one operational example")
    return text.split(marker, 1)[1].split("\n\x60\x60\x60", 1)[0]


def run_example(code: str, adversarial: bool) -> dict:
    with TemporaryDirectory(prefix="andino-addy-proof-") as temp:
        env = {k: v for k, v in os.environ.items() if k.upper() in {
            "SYSTEMROOT", "WINDIR", "PATH", "TEMP", "TMP", "COMSPEC"
        }}
        if adversarial:
            env["ANDINO_NEGATIVE"] = "1"
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        try:
            proc = subprocess.run(
                [sys.executable, "-I", "-B", "-c", WRAPPER],
                input=code, text=True, encoding="utf8", capture_output=True,
                cwd=temp, env=env, timeout=15, creationflags=creationflags,
            )
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": "example timeout"}
        if proc.returncode:
            return {"ok": False, "exit_code": proc.returncode,
                    "error": proc.stderr[-2000:]}
        try:
            value = json.loads(proc.stdout)
        except json.JSONDecodeError:
            return {"ok": False, "error": "example output is not one JSON value",
                    "stdout": proc.stdout[-1000:]}
        return {"ok": True, "observed": value}


def check_method(method: dict, runtime: Path) -> dict:
    mid = method["id"]
    guide = runtime / "skills" / mid / "GUIDE.md"
    code = example_code(guide.read_text(encoding="utf8"))
    resources = {}
    for rel in method["resources"]:
        p = (runtime / rel).resolve()
        if not p.is_relative_to(runtime.resolve()) or not p.is_file():
            raise ValueError("missing or escaped packaged resource: " + rel)
        resources[rel] = digest(p)
    expected = method["operational"]["expected"]
    adversarial_expected = method["operational"]["adversarial_expected"]
    default = run_example(code, False)
    negative = run_example(code, True)
    old, new, mutant_negative, fault = MUTATIONS[mid]
    if code.count(old) != 1:
        raise ValueError("mutation location missing/ambiguous: " + mid)
    mutant = run_example(code.replace(old, new, 1), mutant_negative)
    oracle = adversarial_expected if mutant_negative else expected
    caught = not mutant["ok"] or mutant["observed"] != oracle
    default_pass = default["ok"] and default["observed"] == expected
    negative_pass = negative["ok"] and negative["observed"] == adversarial_expected
    return {
        "id": mid,
        "metadata_sha256": hashlib.sha256(json.dumps(method, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
        "status": "PASS" if default_pass and negative_pass and caught else "FAIL",
        "guide_sha256": digest(guide),
        "resource_sha256": resources,
        "positive_activation_request": method["activation"]["positive"]["request"],
        "negative_activation_request": method["activation"]["negative"]["request"],
        "activation_evidence": "DECLARED_FIXTURES_ONLY; model routing not executed",
        "default": {**default, "expected": expected, "pass": default_pass},
        "adversarial": {**negative, "expected": adversarial_expected, "pass": negative_pass},
        "mutation": {"fault": fault, "detected": caught, "result": mutant},
        "limit": method["operational"]["limit"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    main_root = Path(__file__).resolve().parents[1]
    evidence_dir = main_root / "docs" / "validation" / "andino-unified"
    parser.add_argument("--runtime-root", type=Path, default=main_root.parent / "AI-RULES")
    parser.add_argument("--manifest", type=Path, default=evidence_dir / "addy-methods.json")
    parser.add_argument("--output", type=Path, default=evidence_dir / "addy-operational.json")
    args = parser.parse_args()
    methods = json.loads(args.manifest.read_text(encoding="utf8"))
    ids = [m["id"] for m in methods]
    if set(ids) != EXPECTED_IDS or len(ids) != len(EXPECTED_IDS):
        raise ValueError("manifest must cover the 18 assigned methods exactly once")
    results = []
    for method in methods:
        try:
            result = check_method(method, args.runtime_root)
        except Exception as exc:
            result = {"id": method["id"], "status": "FAIL",
                      "error": type(exc).__name__ + ": " + str(exc)}
        results.append(result)
    passed = sum(r["status"] == "PASS" for r in results)
    report = {
        "schema_version": 1,
        "source_family": "addy",
        "kind": "executed-guide-procedure-examples",
        "runtime_root": str(args.runtime_root.resolve()),
        "manifest_sha256": digest(args.manifest),
        "inputs": {"scripts/check_andino_addy_methods.py": digest(Path(__file__)),
                   args.manifest.resolve().relative_to(main_root).as_posix(): digest(args.manifest)},
        "summary": {"methods": len(results), "passed": passed,
                    "failed": len(results)-passed,
                    "live_browser_or_service_runs": 0,
                    "model_activation_runs": 0},
        "limits": [
            "Activation requests are explicit positive/negative fixtures; no model routing is inferred from keywords.",
            "Executed Python examples demonstrate bounded procedures and mutation sensitivity, not whole-project/live-host parity.",
            "All example filesystem mutations occurred in owned TemporaryDirectory; network/external process disabled.",
        ],
        "methods": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf8")
    print(json.dumps(report["summary"], sort_keys=True))
    for result in results:
        print(result["id"] + ": " + result["status"])
        if result["status"] != "PASS":
            print(json.dumps(result, ensure_ascii=False))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
