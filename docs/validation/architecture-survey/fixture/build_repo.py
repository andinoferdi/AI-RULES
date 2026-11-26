"""Build the architecture-survey trial repository with its scripted git history.

Usage: python build_repo.py <RUN_DIR>

Copies fixture/repo to <RUN_DIR>/repo, commits every file with the initial date, then replays
history.json. A later commit touches each listed file by rewriting its first line, which is a
`// <path>` comment, to `// <path> (rev N)`. Standard library only.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUTHOR = ("Fixture Dev", "dev@example.invalid")


def git(repo, *args, date=None):
    env = dict(os.environ)
    env.update({"GIT_AUTHOR_NAME": AUTHOR[0], "GIT_AUTHOR_EMAIL": AUTHOR[1],
                "GIT_COMMITTER_NAME": AUTHOR[0], "GIT_COMMITTER_EMAIL": AUTHOR[1]})
    if date:
        env.update({"GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date})
    subprocess.run(["git", "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false", *args],
                   cwd=repo, env=env, check=True, capture_output=True)


def bump(path, rel, revision):
    lines = path.read_text(encoding="utf-8").split("\n")
    if not lines[0].startswith("// "):
        raise SystemExit(f"{rel}: first line must be a // comment")
    lines[0] = f"// {rel} (rev {revision})"
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main(run_dir):
    repo = Path(run_dir).resolve() / "repo"
    if repo.exists():
        raise SystemExit(f"{repo} already exists")
    shutil.copytree(HERE / "repo", repo)
    history = json.loads((HERE / "history.json").read_text(encoding="utf-8"))

    git(repo, "init", "-q", "-b", "main")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", history["initial"]["message"], date=history["initial"]["date"])

    revisions = {}
    for commit in history["commits"]:
        for rel in commit["files"]:
            revisions[rel] = revisions.get(rel, 1) + 1
            bump(repo / rel, rel, revisions[rel])
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", commit["message"], date=commit["date"])

    print(f"{repo}: {1 + len(history['commits'])} commits")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
