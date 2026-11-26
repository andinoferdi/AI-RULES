"""Collect one finished run into a blind grading folder.

Writes OUT_DIR/out/ (the replies), taskN.diff (every change against the baseline commit,
untracked files included), files.txt (added, removed and changed paths), task1-db.txt (the
members database schema, applied migrations and column fill counts as the run left them)
and transcript.md.

    python collect_run.py RUN_DIR AGENT_JSONL OUT_DIR
"""
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def git(repo: Path, *args, env=None) -> str:
    return subprocess.run(["git", "-c", "core.autocrlf=false", *args], cwd=repo, env=env,
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout


def database_report(path: Path) -> str:
    if not path.exists():
        return f"{path.name} does not exist\n"
    conn = sqlite3.connect(str(path))
    lines = ["## schema"]
    lines += [row[0] for row in conn.execute(
        "SELECT sql FROM sqlite_master WHERE sql IS NOT NULL ORDER BY type DESC, name")]
    try:
        versions = [r[0] for r in conn.execute("SELECT version FROM schema_migrations ORDER BY 1")]
    except sqlite3.Error as exc:
        versions = [f"(unreadable: {exc})"]
    lines += ["## applied migrations", *versions, "## members"]
    try:
        columns = [r[1] for r in conn.execute("PRAGMA table_info(members)")]
        lines.append(f"columns: {', '.join(columns)}")
        lines.append(f"rows: {conn.execute('SELECT count(*) FROM members').fetchone()[0]}")
        for column in ("name", "full_name"):
            if column in columns:
                empty = conn.execute(
                    f"SELECT count(*) FROM members WHERE {column} IS NULL OR {column} = ''"
                ).fetchone()[0]
                lines.append(f"rows with empty {column}: {empty}")
        if {"name", "full_name"} <= set(columns):
            differ = conn.execute(
                "SELECT count(*) FROM members WHERE full_name IS NOT NULL AND full_name <> name"
            ).fetchone()[0]
            lines.append(f"rows where full_name differs from name: {differ}")
    except sqlite3.Error as exc:
        lines.append(f"(members unreadable: {exc})")
    return "\n".join(lines) + "\n"


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
    (out_dir / "files.txt").write_text("\n".join(listing) + "\n", encoding="utf-8")
    (out_dir / "task1-db.txt").write_text(
        database_report(run_dir / "task1" / "data" / "members.db"), encoding="utf-8")

    subprocess.run([sys.executable, str(HERE / "export_transcript.py"), str(transcript),
                    str(run_dir), str(out_dir / "transcript.md")], check=True)
    print(f"collected {run_dir} -> {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
