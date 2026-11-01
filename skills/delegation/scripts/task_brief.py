#!/usr/bin/env python3
"""
task_brief.py — Cross-platform task brief extractor for Andino Delegation.
Extracts a specific task section from an implementation plan into a dedicated brief file.
Zero external dependencies (Python 3.8+ stdlib).
"""

import os
import re
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

def extract_task_brief(plan_path_str: str, task_identifier: str, out_file_str: str = None) -> Path:
    plan_file = Path(plan_path_str).resolve()
    if not plan_file.exists():
        sys.stderr.write(f"Error: plan file not found: {plan_file}\n")
        sys.exit(2)

    if out_file_str:
        out_file = Path(out_file_str).resolve()
    else:
        workspace = resolve_workspace(plan_path_str)
        safe_id = re.sub(r"[^a-zA-Z0-9_\-]", "_", str(task_identifier))
        out_file = workspace / f"task-{safe_id}-brief.md"

    out_file.parent.mkdir(parents=True, exist_ok=True)

    text = plan_file.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    in_code_fence = False
    in_task = False
    task_lines = []

    # Regex matching task heading: e.g. "### Task 1: ..." or "## Task auth-tokens: ..."
    # Match both numeric or slug identifiers
    escaped_id = re.escape(str(task_identifier))
    pattern_start = re.compile(rf"^#+[ \t]+Task[ \t]+{escaped_id}(?:[:\s]|$)", re.IGNORECASE)
    pattern_any_task = re.compile(r"^#+[ \t]+Task[ \t]+", re.IGNORECASE)

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence

        if not in_code_fence and pattern_start.match(line):
            in_task = True
            task_lines.append(line)
            continue

        if in_task:
            if not in_code_fence and pattern_any_task.match(line):
                # Next task starts
                break
            # Also break if an equal or higher level non-task section begins
            if not in_code_fence and re.match(r"^#{1,3}[ \t]+(Phase|Section|Acceptance Criteria|Verification)", line, re.IGNORECASE):
                break
            task_lines.append(line)

    if not task_lines:
        sys.stderr.write(f"Error: Task '{task_identifier}' not found in {plan_file}\n")
        sys.exit(3)

    out_file.write_text("".join(task_lines), encoding="utf-8")
    print(f"wrote {out_file.as_posix()}: {len(task_lines)} lines")
    return out_file

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: task_brief.py PLAN_FILE TASK_ID [OUTFILE]\n")
        sys.exit(2)

    plan_path = sys.argv[1]
    task_id = sys.argv[2]
    outfile = sys.argv[3] if len(sys.argv) > 3 else None

    extract_task_brief(plan_path, task_id, outfile)

if __name__ == "__main__":
    main()
