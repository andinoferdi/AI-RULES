"""Prepare one trial run folder.

Builds the three fixture repositories in RUN_DIR/task1..task3 with their git history
(task1: tag v2.3, then the v2.4-rc1 candidate; task3: a published baseline, then the
handed-over fix), creates RUN_DIR/out and, when --guide is given, copies that skill folder
to RUN_DIR/guide. The starting commit of each repository is written to RUN_DIR.heads.json,
outside the run folder, for collect_run.py.

    python setup_run.py RUN_DIR [--guide SKILL_FOLDER]
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixture"
GIT = ["git", "-c", "user.name=trial", "-c", "user.email=trial@example.invalid",
       "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false"]
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc")
HISTORY = {
    "task1": [("base", "v2.3: owner email on tasks", "v2.3"),
              ("change", "v2.4-rc1: task sharing, owner lookup refactor", "v2.4-rc1")],
    "task2": [(".", "v2.5 with bulk_edit at 5%", None)],
    "task3": [("base", "Published help site", None),
              ("change", "Fix billing typo and footer year", None)],
}


def git(repo: Path, *args: str) -> str:
    return subprocess.run([*GIT, *args], cwd=repo, check=True, capture_output=True,
                          text=True).stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--guide", type=Path)
    args = parser.parse_args()

    if args.run_dir.exists():
        print(f"refusing to overwrite {args.run_dir}", file=sys.stderr)
        return 1
    heads = {}
    for task, steps in HISTORY.items():
        target = args.run_dir / task
        target.mkdir(parents=True)
        git(target, "init", "-q", "-b", "main")
        (target / ".gitignore").write_text("__pycache__/\nsite/\n", encoding="utf-8")
        for layer, message, tag in steps:
            shutil.copytree(FIXTURE / task / layer, target, ignore=IGNORE, dirs_exist_ok=True)
            git(target, "add", "-A")
            git(target, "commit", "-q", "-m", message)
            if tag:
                git(target, "tag", tag)
        heads[task] = git(target, "rev-parse", "HEAD")
    (args.run_dir / "out").mkdir()
    if args.guide:
        shutil.copytree(args.guide, args.run_dir / "guide", ignore=IGNORE)
    Path(f"{args.run_dir}.heads.json").write_text(json.dumps(heads, indent=2), encoding="utf-8")
    print(f"prepared {args.run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
