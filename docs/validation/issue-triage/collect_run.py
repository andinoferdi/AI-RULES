"""Collect one finished trial run into a blinded grading folder.

    python -I collect_run.py RUN_DIR GRADE_DIR

Copies RUN_DIR/out to GRADE_DIR/out, writes GRADE_DIR/state.txt with the repository state the
rubric lists (status, branch, stash, every branch head, the diff of tracked files and the
content of untracked files outside .gitignore), replaces RUN_DIR with <RUN_DIR>, and fails
if a guidance name is left in the copied text.
"""
import shutil
import subprocess
import sys
from pathlib import Path

GUIDANCE_NAMES = ["andino", "mattpocock", "matt pocock", "guide-p", "guide-q", "guide-r",
                  "agent-brief.md", "out-of-scope.md", "tracker-notes.md", "AGENT-BRIEF",
                  "OUT-OF-SCOPE.md"]


def git(repo, *args):
    run = subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=repo,
                         capture_output=True, text=True, encoding="utf-8")
    return run.stdout + run.stderr


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: python -I collect_run.py RUN_DIR GRADE_DIR")
    run_dir, grade_dir = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    repo = run_dir / "shelf"
    if grade_dir.exists():
        sys.exit(f"{grade_dir} exists")
    shutil.copytree(run_dir / "out", grade_dir / "out")
    untracked = git(repo, "ls-files", "--others", "--exclude-standard").split()
    parts = [
        "$ git status --short\n" + git(repo, "status", "--short"),
        "$ git branch --show-current\n" + git(repo, "branch", "--show-current"),
        "$ git stash list\n" + git(repo, "stash", "list"),
        "$ git for-each-ref --format='%(refname:short) %(objectname:short)' refs/heads\n"
        + git(repo, "for-each-ref", "--format=%(refname:short) %(objectname:short)",
              "refs/heads"),
        "$ git log --oneline -1 --all\n" + git(repo, "log", "--oneline", "-1", "--all"),
        "$ git diff\n" + git(repo, "diff"),
    ]
    for rel in untracked:
        text = (repo / rel).read_text(encoding="utf-8", errors="replace")
        parts.append(f"$ untracked {rel}\n{text}")
    (grade_dir / "state.txt").write_text("\n".join(parts), encoding="utf-8")
    leaks = []
    for path in grade_dir.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for form in (str(run_dir), run_dir.as_posix()):
            text = text.replace(form, "<RUN_DIR>")
        path.write_text(text, encoding="utf-8")
        lowered = text.lower()
        leaks += [f"{path.name}: {name}" for name in GUIDANCE_NAMES if name.lower() in lowered]
    if leaks:
        sys.exit("guidance names left: " + "; ".join(leaks))
    print(f"collected {run_dir.name} -> {grade_dir}")


if __name__ == "__main__":
    main()
