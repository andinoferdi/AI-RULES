"""Paired fresh-context fixture; oracle is withheld from planners/executors.

prepare writes only into a new named directory. verify checks public outputs and
locked artifact decisions, not implementation tokens. Stdlib only.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys


ITEMS = [
    {"id": "a", "title": 'Tea, "green"', "state": "archived"},
    {"id": "b", "title": "Baris\nbaru", "state": "active"},
    {"id": "c", "title": "Kopi", "state": "archived"},
    {"id": "d", "title": "Draft", "state": "draft"},
]
SOURCE = '''import argparse
import json
from pathlib import Path


def load_rows(path: Path) -> list[dict[str, str]]:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    schema = json.loads(Path(__file__).with_name("schema.json").read_text(encoding="utf-8"))
    parser.add_argument("--state", choices=["all", *schema["states"]], default="all")
    args = parser.parse_args(argv)
    rows = load_rows(args.source)
    if args.state != "all":
        rows = [row for row in rows if row["state"] == args.state]
    print(json.dumps(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''
TESTS = '''import contextlib
import io
import json
from pathlib import Path
import unittest
from export import main


def run_cli(*options):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        code = main([str(Path(__file__).with_name("items.json")), *options])
    return code, output.getvalue()


class ExportTests(unittest.TestCase):
    def test_json_default(self):
        code, output = run_cli()
        self.assertEqual(0, code)
        self.assertEqual(4, len(json.loads(output)))

    def test_active_filter(self):
        code, output = run_cli("--state", "active")
        self.assertEqual(0, code)
        self.assertEqual(["b"], [row["id"] for row in json.loads(output)])
'''
REQUEST = '''# Accepted export change

Plan only; write PLAN.md without editing application/schema/tests/README. Another
executor will implement it with only this repository and the saved plan, no chat.

R1: Add CSV output via --format csv; JSON remains the omitted/default format and
must keep its current shape. CSV uses exactly id,title,state columns in that order,
correct quoting for commas/quotes/newlines, original row order and a header even
when the filtered source is empty. Use Python stdlib csv; add no dependencies.
R2: Extend schema.json states with archived after draft, preserving active and
draft. Existing --state accepts archived, all keeps every row, exact matching is
case-sensitive, filtering happens before either renderer. Invalid options still
exit 2 through argparse. Do not change load_rows/main public signatures.
R3: README.md::Quickstart: replace the exact command python export.py --state active
with python export.py --state archived --format csv. Keep the adjacent setup line.
R4: A future published-only export needs a remote provider whose schema and endpoint
are not available (see provider-notes.md). Do not invent or implement it. Include
a bounded discovery task and explicitly unready consumer; independent local work
must be ready to proceed. The provider uncertainty does not block R1-R3.

Repo is Python 3.11+ stdlib. Existing test command at root:
python -m unittest discover -s . -p test_export.py -v
No test script/package.json, no external services for R1-R3. Changes are authorized
after planning by another executor, no commit/push or new approval gate in fixture.
'''


def prepare(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    files = {
        "export.py": SOURCE, "test_export.py": TESTS,
        "items.json": json.dumps(ITEMS, ensure_ascii=False, indent=2) + "\n",
        "empty.json": "[]\n",
        "schema.json": '{"states": ["active", "draft"]}\n',
        "README.md": "# Export\n\n## Quickstart\n\nUse Python 3.11+.\n\n```text\npython export.py --state active\n```\n",
        "provider-notes.md": "Provider endpoint/schema unavailable; obtain an authorized contract sample before designing a consumer. No credentials are supplied.\n",
        "REQUEST.md": REQUEST,
    }
    for name, content in files.items():
        (destination / name).write_text(content, encoding="utf-8")
    identity = {name: hashlib.sha256((destination / name).read_bytes()).hexdigest()
                for name in files}
    (destination / "baseline.json").write_text(json.dumps(identity, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {destination}")


def verify(folder: Path) -> None:
    checks = 0

    def run(*options: str, source: str = "items.json", status: int = 0) -> str:
        nonlocal checks
        result = subprocess.run([sys.executable, "export.py", source, *options],
                                cwd=folder, capture_output=True, text=True, timeout=10)
        assert result.returncode == status, (options, result.returncode, result.stderr)
        checks += 1
        return result.stdout

    assert json.loads(run()) == ITEMS
    assert json.loads(run("--state", "archived")) == [ITEMS[0], ITEMS[2]]
    assert json.loads(run("--state", "active")) == [ITEMS[1]]
    assert json.loads(run("--state", "draft")) == [ITEMS[3]]
    header = ["id", "title", "state"]
    parsed = lambda output: list(csv.reader(io.StringIO(output)))
    rows = lambda items: [[row[key] for key in header] for row in items]
    assert parsed(run("--format", "csv")) == [header, *rows(ITEMS)]
    assert parsed(run("--state", "archived", "--format", "csv")) == [header, *rows([ITEMS[0], ITEMS[2]])]
    assert parsed(run("--format", "csv", source="empty.json")) == [header]
    assert json.loads(run(source="empty.json")) == []
    run("--state", "Archived", status=2)
    run("--format", "xml", status=2)
    assert json.loads((folder / "schema.json").read_text(encoding="utf-8"))["states"] == ["active", "draft", "archived"]
    readme = (folder / "README.md").read_text(encoding="utf-8")
    assert readme == "# Export\n\n## Quickstart\n\nUse Python 3.11+.\n\n```text\npython export.py --state archived --format csv\n```\n"
    checks += 2
    tree = ast.parse((folder / "export.py").read_text(encoding="utf-8"))
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    for name, args, returns in (
        ("main", "argv: list[str] | None=None", "int"),
        ("load_rows", "path: Path", "list[dict[str, str]]"),
    ):
        # Parse the accepted signatures independently, tolerating whitespace only.
        expected = ast.parse(f"def {name}({args}) -> {returns}: pass").body[0]
        assert ast.dump(functions[name].args) == ast.dump(expected.args), name
        assert ast.dump(functions[name].returns) == ast.dump(expected.returns), name
        checks += 1
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(alias.name.split('.')[0] in sys.stdlib_module_names for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0 and node.module.split('.')[0] in sys.stdlib_module_names
    assert not any((folder / name).exists() for name in ("requirements.txt", "pyproject.toml", "package.json"))
    checks += 1
    print(f"PASS: {checks} independent public-output/artifact checks ({folder})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("prepare", "verify"))
    parser.add_argument("folder", type=Path)
    options = parser.parse_args()
    (prepare if options.operation == "prepare" else verify)(options.folder)
