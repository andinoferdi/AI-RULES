"""Collect one documentation-and-adrs trial run for blind grading.

Usage: python -I collect_run.py <run-dir> <out-dir>

Writes into <out-dir>:
  task1.md .. task4.md   the runner's reports (missing ones are noted in state.txt)
  summary.md             the runner's final message, when the parent saved it there
  state.txt              HEAD, branch, git status, commits since the fixture, test run
  changes.diff           full diff of tracked files against the fixture HEAD
  changes-ignore-eol.diff  the same diff with CR/LF line-ending changes ignored
  new-files/             copies of untracked files

Absolute paths of the run directory are replaced with <RUN_DIR> in every text file.
"""
import shutil
import subprocess
import sys
from pathlib import Path

FIXTURE_HEAD = "428f72f13318f64cc9206b898b7868af56213ea6"


def run(cmd, cwd):
    done = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace")
    return (done.stdout + done.stderr).rstrip("\n")


def scrub(text, run_dir):
    for form in {str(run_dir), str(run_dir).replace("\\", "/"), run_dir.as_posix()}:
        text = text.replace(form, "<RUN_DIR>")
    return text


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    run_dir = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=False)
    repo = run_dir / "repo"
    git = ["git", "-c", "core.autocrlf=false", "-c", "core.quotepath=false"]

    missing = []
    for name in ("task1.md", "task2.md", "task3.md", "task4.md", "summary.md"):
        source = run_dir / "out" / name
        if source.exists():
            (out / name).write_text(scrub(source.read_text(encoding="utf-8"), run_dir),
                                    encoding="utf-8")
        else:
            missing.append(name)

    untracked = run(git + ["ls-files", "--others", "--exclude-standard"], repo).splitlines()
    for rel in untracked:
        target = out / "new-files" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(repo / rel, target)

    state = [
        "HEAD: " + run(git + ["rev-parse", "HEAD"], repo),
        "Branch: " + run(git + ["branch", "--show-current"], repo),
        "Fixture HEAD unchanged: " + str(run(git + ["rev-parse", "HEAD"], repo) == FIXTURE_HEAD),
        "Commits after fixture HEAD:",
        run(git + ["log", "--oneline", FIXTURE_HEAD + "..HEAD"], repo) or "(none)",
        "Stash entries: " + (run(git + ["stash", "list"], repo) or "(none)"),
        "",
        "git status --short:",
        run(git + ["status", "--short"], repo) or "(clean)",
        "",
        "Missing outputs: " + (", ".join(missing) or "(none)"),
        "",
        "Test run (python -m unittest discover -s tests -t .):",
        run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."], repo),
    ]
    (out / "state.txt").write_text(scrub("\n".join(state) + "\n", run_dir), encoding="utf-8")
    diff = run(git + ["diff", FIXTURE_HEAD], repo)
    (out / "changes.diff").write_text(scrub(diff + "\n", run_dir), encoding="utf-8")
    # File tools on Windows may rewrite LF as CRLF; this diff shows content changes only.
    content = run(git + ["diff", "--ignore-cr-at-eol", FIXTURE_HEAD], repo)
    (out / "changes-ignore-eol.diff").write_text(scrub(content + "\n", run_dir),
                                                 encoding="utf-8")
    print(f"collected {run_dir} -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
