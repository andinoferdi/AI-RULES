"""Lint: every Python file compiles, has no tabs and no line over 100 characters."""
import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
problems = []
for path in sorted(ROOT.rglob("*.py")):
    if ".git" in path.parts or "dist" in path.parts:
        continue
    try:
        py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError as error:
        problems.append(f"{path.relative_to(ROOT)}: {error.msg}")
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if "\t" in line:
            problems.append(f"{path.relative_to(ROOT)}:{number}: tab character")
        if len(line) > 100:
            problems.append(f"{path.relative_to(ROOT)}:{number}: line longer than 100")
for problem in problems:
    print(problem)
print(f"lint: {len(problems)} problem(s)")
sys.exit(1 if problems else 0)
