"""Prepare one trial run folder.

Copies the fixture repository to RUN_DIR/koperasi, commits a baseline (so the grader can
diff), creates RUN_DIR/out and, when --guide is given, copies that skill folder to
RUN_DIR/guide.

    python setup_run.py RUN_DIR [--guide SKILL_FOLDER]
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixture" / "koperasi"
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
    target = args.run_dir / "koperasi"
    shutil.copytree(FIXTURE, target, ignore=ignore)
    subprocess.run([*GIT, "init", "-q", "-b", "main"], cwd=target, check=True)
    (target / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
    subprocess.run([*GIT, "add", "-A"], cwd=target, check=True)
    subprocess.run([*GIT, "commit", "-q", "-m", "baseline"], cwd=target, check=True)
    (args.run_dir / "out").mkdir()
    if args.guide:
        shutil.copytree(args.guide, args.run_dir / "guide", ignore=ignore)
    print(f"prepared {args.run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
