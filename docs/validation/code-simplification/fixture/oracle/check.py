"""Compare one trial run folder against the fixture's original behavior.

Usage: python -I check.py <RUN_DIR>

<RUN_DIR>/repo is the edited copy of fixture/repo and <RUN_DIR>/out/task2/users.js is the
simplified snippet. Prints one JSON summary; a family passes when every case in it records
the same value or error (type and message) and the same audit list as the original.
"""
import hashlib
import json
import subprocess
import sys
import textwrap
from pathlib import Path

ORACLE = Path(__file__).resolve().parent
FIXTURE = ORACLE.parent
START = "# simplify-ignore-start"
END = "# simplify-ignore-end"


def probe_orders(repo):
    result = subprocess.run(
        [sys.executable, "-I", str(ORACLE / "probe_orders.py"), str(repo)],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        return None, result.stderr.strip()[-2000:]
    return json.loads(result.stdout), None


def probe_users(snippet):
    result = subprocess.run(
        ["node", str(ORACLE / "probe_users.js"), str(snippet)],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        return None, result.stderr.strip()[-2000:]
    return json.loads(result.stdout), None


def compare(original, candidate):
    summary = {}
    for family, expected in original.items():
        actual = candidate.get(family)
        if isinstance(expected, dict):
            pairs = [(key, expected[key], (actual or {}).get(key)) for key in expected]
        else:
            actual = actual or []
            pairs = [(index, case, actual[index] if index < len(actual) else None)
                     for index, case in enumerate(expected)]
        mismatches = [
            {"case": key, "original": want, "candidate": got}
            for key, want, got in pairs if want != got
        ]
        summary[family] = {
            "cases": len(pairs),
            "mismatches": len(mismatches),
            "first_mismatch": mismatches[0] if mismatches else None,
        }
    return summary


def protected_block(path):
    text = path.read_bytes().decode("utf-8")
    if text.count(START) != 1 or text.count(END) != 1:
        return None
    begin = text.index(START)
    return text[begin:text.index(END) + len(END)]


def tree(root):
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


def main():
    run_dir = Path(sys.argv[1]).resolve()
    repo = run_dir / "repo"
    report = {"run_dir": str(run_dir)}

    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."],
        cwd=repo, capture_output=True, text=True, timeout=300,
    )
    report["tests_pass"] = tests.returncode == 0
    report["tests_tail"] = tests.stderr.strip().splitlines()[-3:]

    before, after = tree(FIXTURE / "repo"), tree(repo)
    report["changed_files"] = sorted(name for name in before if name in after and before[name] != after[name])
    report["added_files"] = sorted(name for name in after if name not in before)
    report["deleted_files"] = sorted(name for name in before if name not in after)
    report["original_tests_unchanged"] = all(
        after.get(name) == digest for name, digest in before.items() if name.startswith("tests/")
    )

    original_block = protected_block(FIXTURE / "repo/orders/pricing.py")
    run_block = protected_block(repo / "orders/pricing.py") if (repo / "orders/pricing.py").exists() else None
    report["protected_region_identical"] = run_block == original_block
    report["protected_region_same_ignoring_indent"] = (
        run_block is not None
        and textwrap.dedent(run_block.split("\n", 1)[1]) == textwrap.dedent(original_block.split("\n", 1)[1])
    )

    original, _ = probe_orders(FIXTURE / "repo")
    candidate, error = probe_orders(repo)
    report["orders"] = compare(original, candidate) if candidate else {"probe_error": error}

    snippet = run_dir / "out/task2/users.js"
    if snippet.exists():
        original, _ = probe_users(FIXTURE / "snippet/users.js")
        candidate, error = probe_users(snippet)
        report["users"] = compare(original, candidate) if candidate else {"probe_error": error}
    else:
        report["users"] = {"missing": str(snippet)}

    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
