"""Prepare one trial run folder.

Builds RUN_DIR/billing with the history the run prompt describes: a first commit with the
package, spec and plan; a bare RUN_DIR/origin.git that has it; a second commit for Task 1
(also pushed), whose plan entry is marked DONE; then the product owner's note left
uncommitted in NOTES.md. Creates RUN_DIR/out and, with --guide, copies that skill folder
to RUN_DIR/guide. Each --support folder is copied to RUN_DIR/<its name>, for a reference
skill whose scripts expect helper folders beside it.

    python setup_run.py RUN_DIR [--guide SKILL_FOLDER] [--support FOLDER ...]
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixture"
GIT = ["git", "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false"]
DIMAS = ["-c", "user.name=Dimas", "-c", "user.email=dimas@example.invalid"]
TASK1_DONE = (
    ("| 1. `format_cents` | TODO |", "| 1. `format_cents` | DONE |"),
    ("3. Commit.\n\nStatus: TODO\nResult / Evidence: -\n\n## Task 2",
     "3. Commit.\n\nStatus: DONE\nResult / Evidence: `python -m unittest tests.test_money -v`"
     " -> Ran 8 tests, OK (Dimas, 2026-11-24). Commit `BIL-31 Task 1: format_cents`.\n\n"
     "## Task 2"),
)


def git(repo, *args):
    subprocess.run([*GIT, *DIMAS, *args], cwd=repo, check=True, capture_output=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--guide", type=Path)
    parser.add_argument("--support", type=Path, action="append", default=[])
    args = parser.parse_args()

    if args.run_dir.exists():
        print(f"refusing to overwrite {args.run_dir}", file=sys.stderr)
        return 1
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
    repo = args.run_dir / "billing"
    shutil.copytree(FIXTURE / "base", repo, ignore=ignore)
    (repo / ".gitignore").write_text("__pycache__/\n", encoding="utf-8", newline="\n")
    git(repo, "init", "-q", "-b", "main")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "BIL-31: billing package, accepted spec and plan")

    origin = args.run_dir / "origin.git"
    subprocess.run([*GIT, "init", "-q", "--bare", "-b", "main", str(origin)], check=True,
                   capture_output=True)
    git(repo, "remote", "add", "origin", origin.resolve().as_posix())

    shutil.copytree(FIXTURE / "task1", repo, dirs_exist_ok=True, ignore=ignore)
    plan = repo / "docs" / "plan.md"
    text = plan.read_text(encoding="utf-8")
    for old, new in TASK1_DONE:
        if old not in text:
            print(f"plan anchor missing: {old[:40]!r}", file=sys.stderr)
            return 1
        text = text.replace(old, new)
    plan.write_text(text, encoding="utf-8", newline="\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "BIL-31 Task 1: format_cents")
    git(repo, "push", "-q", "origin", "main")

    shutil.copy2(FIXTURE / "wip" / "NOTES.md", repo / "NOTES.md")

    (args.run_dir / "out").mkdir()
    if args.guide:
        shutil.copytree(args.guide, args.run_dir / "guide", ignore=ignore)
    for folder in args.support:
        shutil.copytree(folder, args.run_dir / folder.name, ignore=ignore)
    print(f"prepared {args.run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
