"""Collect one finished writing-tickets run into a blinded grading folder.

    python -I collect_run.py RUN_DIR GRADE_DIR

Copies RUN_DIR/out and RUN_DIR/roomy/.scratch into GRADE_DIR, writes GRADE_DIR/state.txt with
the repository state the rubric's S0 criterion reads (status, branch, last commit, the diff of
tracked files outside .scratch, untracked paths), replaces RUN_DIR with <RUN_DIR> and guidance
names with <GUIDE>.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

GUIDANCE_NAMES = ["andino-writing-tickets", "writing-tickets", "to-tickets", "andino",
                  "mattpocock", "matt pocock", "setup-matt-pocock-skills", "ticket_graph",
                  "ticket-graph"]


def git(repo, *args):
    run = subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=repo,
                         capture_output=True, text=True, encoding="utf-8")
    return run.stdout + run.stderr


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: python -I collect_run.py RUN_DIR GRADE_DIR")
    run_dir, grade_dir = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    repo = run_dir / "roomy"
    if grade_dir.exists():
        sys.exit(f"{grade_dir} exists")
    shutil.copytree(run_dir / "out", grade_dir / "out")
    if (repo / ".scratch").exists():
        shutil.copytree(repo / ".scratch", grade_dir / "scratch")
    parts = [
        "$ git status --short --untracked-files=all\n"
        + git(repo, "status", "--short", "--untracked-files=all"),
        "$ git branch --show-current\n" + git(repo, "branch", "--show-current"),
        "$ git log --oneline -1\n" + git(repo, "log", "--oneline", "-1"),
        "$ git diff -- . ':(exclude).scratch'\n" + git(repo, "diff", "--", ".", ":(exclude).scratch"),
        "$ git diff -- .scratch\n" + git(repo, "diff", "--", ".scratch"),
    ]
    (grade_dir / "state.txt").write_text("\n".join(parts), encoding="utf-8")
    pattern = re.compile("|".join(re.escape(n) for n in GUIDANCE_NAMES), re.I)
    for path in grade_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            for form in (str(run_dir), run_dir.as_posix()):
                text = text.replace(form, "<RUN_DIR>")
            path.write_text(pattern.sub("<GUIDE>", text), encoding="utf-8")
    print(f"collected {run_dir.name} -> {grade_dir}")


if __name__ == "__main__":
    main()
