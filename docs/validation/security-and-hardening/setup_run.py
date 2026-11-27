"""Prepare one trial run folder.

task1 and task3 are copied and committed as one baseline commit on `main`. task2 gets its
`base/` files committed on `main`, then a branch `feature/attachments` with the `feature/`
files on top, left checked out. Every repository gets the tag `trial-baseline` at its
starting commit so the grader can diff. RUN_DIR/out is created and, when --guide is given,
the skill folder is copied to RUN_DIR/guide.

    python setup_run.py RUN_DIR [--guide SKILL_FOLDER]
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixture"
GIT = ["git", "-c", "user.name=trial", "-c", "user.email=trial@example.invalid",
       "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false"]
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc")


def commit(repo: Path, message: str) -> None:
    subprocess.run([*GIT, "add", "-A"], cwd=repo, check=True)
    subprocess.run([*GIT, "commit", "-q", "-m", message], cwd=repo, check=True)


def init(repo: Path) -> None:
    subprocess.run([*GIT, "init", "-q", "-b", "main"], cwd=repo, check=True)
    (repo / ".gitignore").write_text("__pycache__/\nstorage/\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--guide", type=Path)
    args = parser.parse_args()

    if args.run_dir.exists():
        print(f"refusing to overwrite {args.run_dir}", file=sys.stderr)
        return 1
    for task in ("task1", "task3"):
        repo = args.run_dir / task
        shutil.copytree(FIXTURE / task, repo, ignore=IGNORE)
        init(repo)
        commit(repo, "baseline")
        subprocess.run([*GIT, "tag", "trial-baseline"], cwd=repo, check=True)

    repo = args.run_dir / "task2"
    shutil.copytree(FIXTURE / "task2" / "base", repo, ignore=IGNORE)
    init(repo)
    commit(repo, "Invoice API")
    subprocess.run([*GIT, "switch", "-q", "-c", "feature/attachments"], cwd=repo, check=True)
    shutil.copytree(FIXTURE / "task2" / "feature", repo, ignore=IGNORE, dirs_exist_ok=True)
    commit(repo, "Add invoice attachments")
    subprocess.run([*GIT, "tag", "trial-baseline"], cwd=repo, check=True)

    (args.run_dir / "out").mkdir()
    if args.guide:
        shutil.copytree(args.guide, args.run_dir / "guide", ignore=IGNORE)
    print(f"prepared {args.run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
