"""Collect one finished run into a blind grading folder.

Writes OUT_DIR/out/ (the replies), taskN.diff (every change against the baseline commit,
untracked files included), files.txt (added, removed and changed paths, and whether the
production snapshot in task1 is byte-identical to the fixture) and transcript.md.

    python collect_run.py RUN_DIR AGENT_JSONL OUT_DIR
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAPSHOT = Path("task1") / "data" / "accounts.json"


def git(repo: Path, *args, env=None) -> str:
    return subprocess.run(["git", "-c", "core.autocrlf=false", *args], cwd=repo, env=env,
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "(missing)"


def main() -> int:
    run_dir, transcript, out_dir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    out_dir.mkdir(parents=True)
    shutil.copytree(run_dir / "out", out_dir / "out")
    listing = []
    for task in ("task1", "task2", "task3"):
        repo = run_dir / task
        base = git(repo, "rev-list", "--max-parents=0", "HEAD").split()[0]
        with tempfile.TemporaryDirectory() as temp:
            env = dict(os.environ, GIT_INDEX_FILE=str(Path(temp) / "index"))
            git(repo, "read-tree", "HEAD", env=env)
            git(repo, "add", "-A", env=env)
            diff = git(repo, "diff", "--cached", base, "--", ".", env=env)
            names = git(repo, "diff", "--cached", "--name-status", base, "--", ".", env=env)
        commits = git(repo, "log", "--oneline", f"{base}..HEAD")
        (out_dir / f"{task}.diff").write_text(diff, encoding="utf-8")
        listing.append(f"## {task}\n{names or '(no changes)'}"
                       + (f"\ncommits after baseline:\n{commits}" if commits else ""))
    same = digest(run_dir / SNAPSHOT) == digest(HERE / "fixture" / SNAPSHOT)
    listing.append(f"task1/data/accounts.json identical to the fixture: {same}")
    (out_dir / "files.txt").write_text("\n".join(listing) + "\n", encoding="utf-8")

    subprocess.run([sys.executable, str(HERE / "export_transcript.py"), str(transcript),
                    str(run_dir), str(out_dir / "transcript.md")], check=True)
    print(f"collected {run_dir} -> {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
