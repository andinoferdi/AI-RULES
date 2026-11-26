"""Prepare one trial run folder.

Copies the three fixture repositories to RUN_DIR/task1..task3 and commits a baseline in
each. task3 gets two commits: the sign-up code before ACC-212 (emails compared as typed),
then the ACC-212 fix, so the runner can test against the pre-fix revision. The baseline
commit of every task is written next to the run folder, to RUN_DIR.bases.json, where the
runner does not see it. Creates RUN_DIR/out and, when --guide is given, copies that skill
folder to RUN_DIR/guide.

    python setup_run.py RUN_DIR [--guide SKILL_FOLDER]
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixture"
GIT = ["git", "-c", "user.name=Fikri", "-c", "user.email=fikri@kopikita.example",
       "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false"]


def commit(repo: Path, message: str) -> str:
    subprocess.run([*GIT, "add", "-A"], cwd=repo, check=True)
    subprocess.run([*GIT, "commit", "-q", "-m", message], cwd=repo, check=True)
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True,
                          capture_output=True, text=True).stdout.strip()


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
    bases = {}
    for task in ("task1", "task2", "task3"):
        target = args.run_dir / task
        shutil.copytree(FIXTURE / task, target, ignore=ignore)
        subprocess.run([*GIT, "init", "-q", "-b", "main"], cwd=target, check=True)
        (target / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
        if task == "task3":
            service = target / "accounts" / "service.py"
            fixed = service.read_bytes()
            shutil.copyfile(FIXTURE / "task3-history" / "service_before_acc212.py", service)
            bases["task3-pre-fix"] = commit(target, "Add account registration")
            service.write_bytes(fixed)
            bases[task] = commit(target, "Normalize emails before the duplicate check (ACC-212)")
        else:
            bases[task] = commit(target, "baseline")
    bases_file = args.run_dir.with_name(args.run_dir.name + ".bases.json")
    bases_file.write_text(json.dumps(bases, indent=2), encoding="utf-8")
    (args.run_dir / "out").mkdir()
    if args.guide:
        shutil.copytree(args.guide, args.run_dir / "guide", ignore=ignore)
    print(f"prepared {args.run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
