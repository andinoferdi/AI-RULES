"""Collect one finished run into a blind grading folder.

Writes OUT_DIR/out/ (the replies), repo.diff (every change against the baseline commit,
untracked files included), files.txt (added, removed and changed paths, and commits made after
the baseline) and transcript.md, exported with the debugging trial's exporter so reads of the
guidance folder are hidden.

    python collect_run.py RUN_DIR AGENT_JSONL OUT_DIR
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EXPORTER = Path(__file__).resolve().parent.parent / "debugging" / "export_transcript.py"


def git(repo: Path, *args, env=None) -> str:
    return subprocess.run(["git", "-c", "core.autocrlf=false", *args], cwd=repo, env=env,
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout


def main() -> int:
    run_dir, transcript, out_dir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    out_dir.mkdir(parents=True)
    shutil.copytree(run_dir / "out", out_dir / "out")
    repo = run_dir / "repo"
    base = git(repo, "rev-list", "--max-parents=0", "HEAD").split()[0]
    with tempfile.TemporaryDirectory() as temp:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(temp) / "index"))
        git(repo, "read-tree", "HEAD", env=env)
        git(repo, "add", "-A", env=env)
        diff = git(repo, "diff", "--cached", base, env=env)
        names = git(repo, "diff", "--cached", "--name-status", base, env=env)
    commits = git(repo, "log", "--oneline", f"{base}..HEAD")
    (out_dir / "repo.diff").write_text(diff, encoding="utf-8")
    (out_dir / "files.txt").write_text(
        (names or "(no changes)\n") + (f"commits after baseline:\n{commits}" if commits else ""),
        encoding="utf-8")
    subprocess.run([sys.executable, str(EXPORTER), str(transcript), str(run_dir),
                    str(out_dir / "transcript.md")], check=True)
    # Runners read the guide through shell variables ("$R/guide/x.md"), which the exporter's
    # <RUN>/guide pattern misses; hide every guide path so file names cannot reveal the arm.
    exported = out_dir / "transcript.md"
    text = re.sub(r"guide/[^\s'\"`;|)]*", "guide/[guidance]", exported.read_text(encoding="utf-8"))
    # A runner that cd's into the guide folder names its files without the guide/ prefix; hide
    # those paths, and bare file names that do not also exist in the repository.
    guide = run_dir / "guide"
    if guide.is_dir():
        repo_names = {path.name for path in repo.rglob("*") if path.is_file()}
        names = set()
        for path in guide.rglob("*"):
            if path.is_file():
                names.add(path.relative_to(guide).as_posix())
                if path.name not in repo_names:
                    names.add(path.name)
        for name in sorted(names, key=len, reverse=True):
            text = re.sub(r"(?<![\w./-])" + re.escape(name) + r"(?![\w-])", "[guidance]", text)
    exported.write_text(text, encoding="utf-8")
    print(f"collected {run_dir} -> {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
