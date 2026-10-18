import ast
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
candidate = root / "candidate.py"
source = candidate.read_bytes()
namespace = {}
exec(compile(source, str(candidate), "exec"), namespace)
cases = [
    ("admin_own", {"role": "admin", "org": "A"}, {"org": "A"}, True),
    ("admin_other", {"role": "admin", "org": "A"}, {"org": "B"}, True),
    ("member_own", {"role": "member", "org": "A"}, {"org": "A"}, True),
    ("member_other", {"role": "member", "org": "A"}, {"org": "B"}, False),
]
observed = []
for name, user, record, expected in cases:
    actual = namespace["can_open"](user, record)
    observed.append({"id": name, "user": user, "record": record,
                     "expected": expected, "actual": actual,
                     "matches_spec": actual == expected})
tree = ast.parse(source)
dynamic_calls = [{"line": node.lineno, "call": node.func.id}
                 for node in ast.walk(tree)
                 if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                 and node.func.id in {"eval", "exec"}]

# This deliberately faulty in-memory copy checks the independent admin oracle.
mutation = source.decode().replace('role == "admin"', 'role == "administrator"')
mutant_namespace = {}
exec(compile(mutation, "<disposable-admin-mutation>", "exec"), mutant_namespace)
mutant_actual = mutant_namespace["can_open"]({"role": "admin", "org": "A"}, {"org": "A"})
result = {
    "candidate_path": str(candidate),
    "sha256_before": hashlib.sha256(source).hexdigest(),
    "scope": {"baseline": "new file; empty prior bytes", "owned_new_files_reviewed": ["candidate.py"],
              "reviewed_bytes": len(source), "reviewed_lines": len(source.splitlines())},
    "spec_cases": observed,
    "spec_matches": sum(case["matches_spec"] for case in observed),
    "spec_mismatches": sum(not case["matches_spec"] for case in observed),
    "standards_dynamic_calls": dynamic_calls,
    "mutation": {"kind": "admin comparison changed only in memory", "expected": True,
                 "actual": mutant_actual, "independent_oracle_detected": mutant_actual is not True,
                 "candidate_file_modified": False},
    "sha256_after": hashlib.sha256(candidate.read_bytes()).hexdigest(),
    "environment": "offline Python standard library; no service calls",
}
(root / "probe-results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
