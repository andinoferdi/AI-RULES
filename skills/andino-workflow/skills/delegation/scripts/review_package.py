#!/usr/bin/env python3
"""
review_package.py — Cross-platform diff packager for Andino Delegation.
Generates an isolated diff package containing commit log, stat summary, and net diff.
Zero external dependencies (Python 3.8+ stdlib).
"""

import os
import subprocess
import sys
from pathlib import Path

# Import resolver from same directory
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
try:
    from delegation_workspace import resolve_workspace
except ImportError:
    def resolve_workspace(p):
        return Path(p).resolve().parent

def run_git(args: list[str]) -> str:
    res = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True
    )
    return res.stdout

def create_review_package(plan_path_str: str, base_ref: str, head_ref: str, out_file_str: str = None) -> Path:
    plan_file = Path(plan_path_str).resolve()
    if not plan_file.exists():
        sys.stderr.write(f"Error: plan file not found: {plan_file}\n")
        sys.exit(2)

    # Verify commits exist
    try:
        base_sha = run_git(["rev-parse", "--verify", base_ref]).strip()
        head_sha = run_git(["rev-parse", "--verify", head_ref]).strip()
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"Error: invalid git ref: {e}\n")
        sys.exit(2)

    # Range guards
    try:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", base_sha, head_sha],
            check=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace"
        )
    except subprocess.CalledProcessError:
        sys.stderr.write(f"Error: HEAD ({head_ref}) is not a descendant of BASE ({base_ref})\n")
        sys.exit(3)

    count_str = run_git(["rev-list", "--count", f"{base_sha}..{head_sha}"]).strip()
    if int(count_str) <= 0:
        sys.stderr.write(f"Error: commit range is empty: {base_ref}..{head_ref}\n")
        sys.exit(3)

    base7 = base_sha[:7]
    head7 = head_sha[:7]

    if out_file_str:
        out_file = Path(out_file_str).resolve()
    else:
        workspace = resolve_workspace(plan_path_str)
        out_file = workspace / f"review-{base7}..{head7}.diff"

    out_file.parent.mkdir(parents=True, exist_ok=True)

    commits_log = run_git(["log", "--oneline", f"{base_sha}..{head_sha}"])
    diff_stat = run_git(["diff", "--stat", f"{base_sha}..{head_sha}"])
    diff_u10 = run_git(["diff", "-U10", f"{base_sha}..{head_sha}"])

    content = [
        f"# Review Package: {base7}..{head7}\n\n",
        "## Commits\n",
        commits_log,
        "\n## Files Changed\n",
        diff_stat,
        "\n## Net Unified Diff\n",
        diff_u10,
    ]

    out_file.write_text("".join(content), encoding="utf-8")
    byte_count = out_file.stat().st_size
    print(f"wrote {out_file.as_posix()}: {count_str} commit(s), {byte_count} bytes")
    return out_file

def main():
    if len(sys.argv) < 4:
        sys.stderr.write("Usage: review_package.py PLAN_FILE BASE HEAD [OUTFILE]\n")
        sys.exit(2)

    plan_path = sys.argv[1]
    base_ref = sys.argv[2]
    head_ref = sys.argv[3]
    outfile = sys.argv[4] if len(sys.argv) > 4 else None

    create_review_package(plan_path, base_ref, head_ref, outfile)

if __name__ == "__main__":
    main()
