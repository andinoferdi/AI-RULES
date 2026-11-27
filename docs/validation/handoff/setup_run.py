"""Prepare one trial run folder for the handoff comparison.

Builds RUN_DIR/task1 (a feature branch with commits, a staged edit, an unstaged edit and
untracked files), RUN_DIR/task2 (the boundary scenarios), RUN_DIR/task3 (a repository that
moved on after a handoff was written) and RUN_DIR/handoff-from-sari.md. Records each
repository's starting tree and status inside its .git folder for collect_run.py, creates
RUN_DIR/out and, when --guide is given, copies that skill folder to RUN_DIR/guide.

    python setup_run.py RUN_DIR [--guide SKILL_FOLDER]
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixture"
GIT = ["git", "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false"]


def git(repo, *args, author=("Andi", "andi@example.invalid"), env=None):
    who = ["-c", f"user.name={author[0]}", "-c", f"user.email={author[1]}"]
    return subprocess.run([*GIT, *who, *args], cwd=repo, env=env, check=True,
                          capture_output=True, text=True, encoding="utf-8").stdout.strip()


def overlay(src, repo):
    shutil.copytree(src, repo, dirs_exist_ok=True)


def commit(repo, message, author=("Andi", "andi@example.invalid")):
    git(repo, "add", "-A", author=author)
    git(repo, "commit", "-q", "-m", message, author=author)


def record_start(repo):
    """Store the full working-tree snapshot and status so the collector can diff against it."""
    with tempfile.TemporaryDirectory() as temp:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(temp) / "index"))
        git(repo, "read-tree", "HEAD", env=env)
        git(repo, "add", "-A", env=env)
        tree = git(repo, "write-tree", env=env)
    meta = repo / ".git" / "trial"
    meta.mkdir()
    (meta / "start-tree").write_text(tree + "\n", encoding="utf-8")
    (meta / "start-head").write_text(git(repo, "rev-parse", "HEAD") + "\n", encoding="utf-8")
    (meta / "start-status").write_text(git(repo, "status", "--porcelain=v1", "-b") + "\n",
                                       encoding="utf-8")


def build_task1(run):
    repo = run / "task1"
    overlay(FIXTURE / "task1" / "base", repo)
    git(repo, "init", "-q", "-b", "main")
    (repo / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
    commit(repo, "invoicekit baseline")
    git(repo, "checkout", "-q", "-b", "feat/csv-export")
    overlay(FIXTURE / "task1" / "c1", repo)
    commit(repo, "Add CSV export spec and plan")
    overlay(FIXTURE / "task1" / "c2", repo)
    commit(repo, "Add export CLI entry point")
    overlay(FIXTURE / "task1" / "staged", repo)
    git(repo, "add", "invoicekit/models.py")
    overlay(FIXTURE / "task1" / "unstaged", repo)
    overlay(FIXTURE / "task1" / "untracked", repo)
    record_start(repo)


def build_task3(run):
    repo = run / "task3"
    sari, rizal = ("Sari", "sari@example.invalid"), ("Rizal", "rizal@example.invalid")
    overlay(FIXTURE / "task3" / "a", repo)
    git(repo, "init", "-q", "-b", "main")
    (repo / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
    commit(repo, "Capped exponential backoff (NET-12 step 1)", sari)
    overlay(FIXTURE / "task3" / "b", repo)
    commit(repo, "Default attempts from config (NET-12 step 2)", sari)
    base = git(repo, "rev-parse", "--short", "HEAD")
    overlay(FIXTURE / "task3" / "c", repo)
    commit(repo, "OPS-51: lower default attempts to 3; rename backoff to compute_delay", rizal)
    handoff = (FIXTURE / "handoff-from-sari.md").read_text(encoding="utf-8")
    (run / "handoff-from-sari.md").write_text(handoff.replace("{BASE}", base), encoding="utf-8")
    record_start(repo)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--guide", type=Path)
    args = parser.parse_args()

    run = args.run_dir
    if run.exists():
        print(f"refusing to overwrite {run}", file=sys.stderr)
        return 1
    run.mkdir(parents=True)
    build_task1(run)
    shutil.copytree(FIXTURE / "task2", run / "task2")
    build_task3(run)
    shutil.copy(FIXTURE / "session1.md", run / "session1.md")
    (run / "out").mkdir()
    if args.guide:
        shutil.copytree(args.guide, run / "guide",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    print(f"prepared {run}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
