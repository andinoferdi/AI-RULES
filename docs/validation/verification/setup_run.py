"""Prepare one trial run folder.

Builds RUN_DIR/task1..task3 from the fixture with the history each task expects:

- task1: commit "baseline", then the worker's commit "Add discount codes (R1-R4)".
- task2: commit "Release 2.4.1 candidate".
- task3: commit "baseline", then Bayu's commit "Fix #42", then Tari's uncommitted README draft.

Also creates RUN_DIR/out, copies the handover state (no .git) to RUN_DIR.handover for
collect_run.py and, when --guide is given, copies that skill folder to RUN_DIR/guide.

    python setup_run.py RUN_DIR [--guide SKILL_FOLDER]
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixture"
GIT = ["git", "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false"]
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "dist")
PEOPLE = {
    "wulan": ("Wulan", "wulan@example.invalid"),
    "worker": ("worker-agent", "worker@example.invalid"),
    "rudi": ("Rudi", "rudi@example.invalid"),
    "bayu": ("Bayu", "bayu@example.invalid"),
    "tari": ("Tari", "tari@example.invalid"),
}
HISTORY = {
    "task1": [("base", "wulan", "baseline"), ("worker", "worker", "Add discount codes (R1-R4)")],
    "task2": [(".", "rudi", "Release 2.4.1 candidate")],
    "task3": [("base", "tari", "baseline"),
              ("fix", "bayu", "Fix #42: transliterate accents in slugify")],
}
UNCOMMITTED = {"task3": "wip"}


def commit(repo: Path, who: str, message: str) -> None:
    name, email = PEOPLE[who]
    ident = ["-c", f"user.name={name}", "-c", f"user.email={email}"]
    subprocess.run([*GIT, "add", "-A"], cwd=repo, check=True)
    subprocess.run([*GIT, *ident, "commit", "-q", "-m", message], cwd=repo, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--guide", type=Path)
    args = parser.parse_args()
    handover = args.run_dir.with_name(args.run_dir.name + ".handover")
    if args.run_dir.exists() or handover.exists():
        print(f"refusing to overwrite {args.run_dir}", file=sys.stderr)
        return 1
    heads = {}
    for task, layers in HISTORY.items():
        repo = args.run_dir / task
        repo.mkdir(parents=True)
        subprocess.run([*GIT, "init", "-q", "-b", "main"], cwd=repo, check=True)
        (repo / ".gitignore").write_text("__pycache__/\ndist/\n", encoding="utf-8")
        for layer, who, message in layers:
            shutil.copytree(FIXTURE / task / layer, repo, ignore=IGNORE, dirs_exist_ok=True)
            commit(repo, who, message)
        if task in UNCOMMITTED:
            shutil.copytree(FIXTURE / task / UNCOMMITTED[task], repo, dirs_exist_ok=True)
        heads[task] = subprocess.run([*GIT, "rev-parse", "HEAD"], cwd=repo, check=True,
                                     capture_output=True, text=True).stdout.strip()
        shutil.copytree(repo, handover / task, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    (handover / "heads.json").write_text(json.dumps(heads, indent=2), encoding="utf-8")
    (args.run_dir / "out").mkdir()
    if args.guide:
        shutil.copytree(args.guide, args.run_dir / "guide", ignore=IGNORE)
    print(f"prepared {args.run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
