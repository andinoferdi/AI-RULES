"""Independent literal cases from the supplied access specification."""
import ast
import json
import sys
from pathlib import Path

CASES = [
    ("admin_own_org", {"role": "admin", "org": "A"}, {"org": "A"}, True),
    ("admin_other_org", {"role": "admin", "org": "A"}, {"org": "B"}, True),
    ("member_own_org", {"role": "member", "org": "A"}, {"org": "A"}, True),
    ("member_other_org", {"role": "member", "org": "A"}, {"org": "B"}, False),
]

path = Path(sys.argv[1])
mode = sys.argv[2]
source = path.read_bytes()
if mode == "spec":
    namespace = {}
    exec(compile(source, str(path), "exec"), namespace)
    checks = []
    for name, user, record, expected in CASES:
        actual = namespace["can_open"](user, record)
        checks.append({"id": name, "user": user, "record": record,
                       "expected": expected, "actual": actual,
                       "pass": actual is expected})
    result = {"axis": "spec", "cases": checks,
              "passed": sum(c["pass"] for c in checks),
              "failed": sum(not c["pass"] for c in checks)}
else:
    tree = ast.parse(source)
    calls = [{"name": n.func.id, "line": n.lineno}
             for n in ast.walk(tree) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name) and n.func.id == "eval"]
    result = {"axis": "standards", "rule": "never evaluate user input dynamically",
              "dynamic_eval_calls": calls, "pass": not calls}
print(json.dumps(result, sort_keys=True))
sys.exit(int(result.get("failed", 0) > 0 or result.get("pass") is False))
