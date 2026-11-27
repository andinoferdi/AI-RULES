"""Prepare one trial run folder.

Copies the checkpoints to RUN_DIR/checkpoints, makes one user folder per checkpoint under
RUN_DIR/ws (t5 and t6 start from fixture/workspace, the others empty), commits a baseline of
RUN_DIR/ws so the grader can diff it, creates RUN_DIR/out and, when --guide is given, copies
that skill folder to RUN_DIR/guide.

    python setup_run.py RUN_DIR [--guide SKILL_FOLDER]
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixture"
CHECKPOINTS = [f"t{n}" for n in range(1, 9)]
PREFILLED = {"t5", "t6"}
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
    shutil.copytree(FIXTURE / "checkpoints", args.run_dir / "checkpoints")
    ws = args.run_dir / "ws"
    for checkpoint in CHECKPOINTS:
        if checkpoint in PREFILLED:
            shutil.copytree(FIXTURE / "workspace", ws / checkpoint)
        else:
            (ws / checkpoint).mkdir(parents=True)
    subprocess.run([*GIT, "init", "-q", "-b", "main"], cwd=ws, check=True)
    subprocess.run([*GIT, "add", "-A"], cwd=ws, check=True)
    subprocess.run([*GIT, "commit", "-q", "-m", "baseline"], cwd=ws, check=True)
    (args.run_dir / "out").mkdir()
    if args.guide:
        shutil.copytree(args.guide, args.run_dir / "guide",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    print(f"prepared {args.run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
