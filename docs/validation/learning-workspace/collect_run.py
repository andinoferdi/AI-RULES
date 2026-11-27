"""Collect one finished run into a blind grading folder.

Writes OUT_DIR/out/ (the replies), OUT_DIR/ws/ (every user folder as the run left it),
ws.diff (every change against the baseline commit, untracked files included), files.txt
(added, removed and changed paths per checkpoint) and transcript.md.

    python collect_run.py RUN_DIR AGENT_JSONL OUT_DIR
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def git(repo: Path, *args, env=None) -> str:
    return subprocess.run(["git", "-c", "core.autocrlf=false", *args], cwd=repo, env=env,
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout


def main() -> int:
    run_dir, transcript, out_dir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    out_dir.mkdir(parents=True)
    shutil.copytree(run_dir / "out", out_dir / "out")
    ws = run_dir / "ws"
    shutil.copytree(ws, out_dir / "ws", ignore=shutil.ignore_patterns(".git"))
    base = git(ws, "rev-list", "--max-parents=0", "HEAD").split()[0]
    with tempfile.TemporaryDirectory() as temp:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(temp) / "index"))
        git(ws, "read-tree", "HEAD", env=env)
        git(ws, "add", "-A", env=env)
        diff = git(ws, "diff", "--cached", base, env=env)
        names = git(ws, "diff", "--cached", "--name-status", base, env=env)
    commits = git(ws, "log", "--oneline", f"{base}..HEAD")
    (out_dir / "ws.diff").write_text(diff, encoding="utf-8")
    listing = names or "(no changes)\n"
    if commits:
        listing += f"commits after baseline:\n{commits}"
    (out_dir / "files.txt").write_text(listing, encoding="utf-8")
    subprocess.run([sys.executable, str(HERE / "export_transcript.py"), str(transcript),
                    str(run_dir), str(out_dir / "transcript.md")], check=True)
    print(f"collected {run_dir} -> {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
