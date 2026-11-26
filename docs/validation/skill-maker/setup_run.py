"""Prepare one trial run folder.

Copies fixture/repo to RUN_DIR/repo, restoring the real names of the files kept under fixture
names in this repository (AGENTS.md, skills/*/SKILL.md, .editorconfig), commits a baseline so
the grader can diff, creates RUN_DIR/out and, when --guide is given, copies that skill folder to
RUN_DIR/guide.

    python setup_run.py RUN_DIR [--guide SKILL_FOLDER]
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixture" / "repo"
RENAMES = {"AGENTS.fixture.md": "AGENTS.md", "SKILL.fixture.md": "SKILL.md",
           "editorconfig.fixture": ".editorconfig"}
GIT = ["git", "-c", "user.name=trial", "-c", "user.email=trial@example.invalid",
       "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--guide", type=Path)
    args = parser.parse_args()

    if args.run_dir.exists():
        print(f"refusing to overwrite {args.run_dir}", file=sys.stderr)
        return 1
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
    repo = args.run_dir / "repo"
    shutil.copytree(FIXTURE, repo, ignore=ignore)
    for path in sorted(repo.rglob("*")):
        if path.name in RENAMES:
            path.rename(path.with_name(RENAMES[path.name]))
    subprocess.run([*GIT, "init", "-q", "-b", "main"], cwd=repo, check=True)
    subprocess.run([*GIT, "add", "-A"], cwd=repo, check=True)
    subprocess.run([*GIT, "commit", "-q", "-m", "baseline"], cwd=repo, check=True)
    (args.run_dir / "out").mkdir()
    if args.guide:
        shutil.copytree(args.guide, args.run_dir / "guide", ignore=ignore)
    print(f"prepared {args.run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
