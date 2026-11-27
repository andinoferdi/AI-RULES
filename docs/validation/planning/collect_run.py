"""Collect one finished run into a blind grading folder.

Writes OUT_DIR/plan.md (every new or changed Markdown file in the repository, each under its
path), OUT_DIR/reply.md and OUT_DIR/files.txt (paths added, changed or removed against the
baseline commit). Guide and product names are replaced with [guide] and plan folders with
<plan> so the grader cannot read the arm from them.

    python collect_run.py RUN_DIR OUT_DIR
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

NAMES = re.compile(r"superpowers|writing-plans|planning-and-task-breakdown|andino[-\w]*|"
                   r"agent-skills|subagent-driven-development|executing-plans|plan-execution",
                   re.IGNORECASE)
PLAN_DIRS = re.compile(r"(?:docs/superpowers/plans|docs/exec-plans/active|tasks)/")


def git(repo: Path, *args, env=None) -> str:
    return subprocess.run(["git", "-c", "core.autocrlf=false", *args], cwd=repo, env=env,
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout


def blind(text: str) -> str:
    return NAMES.sub("[guide]", PLAN_DIRS.sub("<plan>/", text))


def main() -> int:
    run_dir, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    out_dir.mkdir(parents=True)
    repo = run_dir / "koperasi"
    base = git(repo, "rev-list", "--max-parents=0", "HEAD").split()[0]
    with tempfile.TemporaryDirectory() as temp:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(temp) / "index"))
        git(repo, "read-tree", "HEAD", env=env)
        git(repo, "add", "-A", env=env)
        names = git(repo, "diff", "--cached", "--name-status", base, env=env)
    commits = git(repo, "log", "--oneline", f"{base}..HEAD")
    (out_dir / "files.txt").write_text(
        blind(names or "(no changes)\n") + (f"commits after baseline:\n{commits}" if commits else ""),
        encoding="utf-8")
    parts = []
    for line in names.splitlines():
        status, path = line.split("\t")[0], line.split("\t")[-1]
        if status != "D" and path.endswith(".md"):
            text = (repo / path).read_text(encoding="utf-8")
            parts.append(f"<!-- file: {blind(path)} -->\n\n{blind(text)}")
    (out_dir / "plan.md").write_text("\n\n".join(parts) or "(no plan file)\n", encoding="utf-8")
    reply = run_dir / "out" / "reply.md"
    (out_dir / "reply.md").write_text(
        blind(reply.read_text(encoding="utf-8")) if reply.exists() else "(no reply)\n",
        encoding="utf-8")
    print(f"collected {run_dir} -> {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
