"""Prepare one trial run folder.

Writes the synthetic session store to RUN_DIR/claude-home/projects/, creates RUN_DIR/out and
RUN_DIR/work, records a hash of every store file next to the run folder (RUN_DIR.hashes.json,
outside what the runner may touch) and, when --guide is given, copies that skill folder to
RUN_DIR/guide.

    python setup_run.py RUN_DIR [--guide SKILL_FOLDER]
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--guide", type=Path)
    args = parser.parse_args()

    if args.run_dir.exists():
        print(f"refusing to overwrite {args.run_dir}", file=sys.stderr)
        return 1
    store = args.run_dir / "claude-home" / "projects"
    with tempfile.TemporaryDirectory() as temp:
        subprocess.run([sys.executable, str(HERE / "make_fixture.py"), str(store),
                        str(Path(temp) / "key.json")], check=True, stdout=subprocess.DEVNULL)
    (args.run_dir / "out").mkdir()
    (args.run_dir / "work").mkdir()
    hashes = {path.relative_to(args.run_dir).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted(store.rglob("*")) if path.is_file()}
    Path(str(args.run_dir) + ".hashes.json").write_text(json.dumps(hashes, indent=2) + "\n",
                                                         encoding="utf-8")
    if args.guide:
        shutil.copytree(args.guide, args.run_dir / "guide",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    print(f"prepared {args.run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
