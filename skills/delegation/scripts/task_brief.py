#!/usr/bin/env python3
"""
task_brief.py — Cross-platform task brief extractor for Andino Delegation.
Extracts a specific task section from an implementation plan into a dedicated brief file.
Zero external dependencies (Python 3.8+ stdlib).
"""

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

    text = plan_file.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    escaped_id = re.escape(str(task_identifier))
    task_title = re.compile(
        rf"^(?:Task[ \t]+{escaped_id}(?=[:\s]|$)|"
        rf"{escaped_id}(?:[ \t]*:|[ \t]+[—–-](?:[ \t]+|$)|$))",
        re.IGNORECASE,
    )
    headings = []
    fence = None
    for index, line in enumerate(lines):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            continue
        if marker:
            fence = marker[1]
            continue
        heading = re.match(r"^ {0,3}(#{1,6})[ \t]+(.+?)\s*$", line)
        if heading:
            headings.append((index, len(heading[1]), heading[2]))

    matches = [(index, depth) for index, depth, title in headings if task_title.match(title)]
    if len(matches) != 1:
        reason = "not found" if not matches else "ambiguous (duplicate headings)"
        sys.stderr.write(f"Error: Task '{task_identifier}' {reason} in {plan_file}\n")
        sys.exit(3)

    start, depth = matches[0]
    end = next((index for index, level, _ in headings if index > start and level <= depth), len(lines))
    task_lines = lines[start:end]
    if out_file_str:
        out_file = Path(out_file_str).resolve()
    else:
        workspace = resolve_workspace(plan_path_str)
        safe_id = re.sub(r"[^a-zA-Z0-9_\-]", "_", str(task_identifier))
        out_file = workspace / f"task-{safe_id}-brief.md"
    out_file.parent.mkdir(parents=True, exist_ok=True)
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
