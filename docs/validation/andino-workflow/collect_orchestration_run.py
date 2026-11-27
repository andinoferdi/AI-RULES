"""Collect one finished orchestration-trial run into a grading folder.

    python -I collect_orchestration_run.py RUN_DIR GRADE_DIR [TRANSCRIPT] [SKILL_DIR]

Copies RUN_DIR/out, writes GRADE_DIR/state.txt with the repository state (status, last commit,
diff of tracked files, untracked paths) and copies untracked files into GRADE_DIR/untracked.
With TRANSCRIPT (the runner's subagent .jsonl), writes GRADE_DIR/trace.md: every tool call in
order with its main input, and the token totals summed once per assistant message. RUN_DIR and
SKILL_DIR are replaced by <RUN_DIR> and <GUIDE> everywhere.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

INPUT_KEYS = ("file_path", "path", "pattern", "command", "query", "url", "skill", "description")


def git(repo, *args):
    run = subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=repo,
                         capture_output=True, text=True, encoding="utf-8")
    return run.stdout + run.stderr


def summarize(tool_input):
    parts = []
    for key in INPUT_KEYS:
        if key in tool_input and tool_input[key]:
            value = str(tool_input[key]).replace("\n", " ")
            parts.append(f"{key}={value[:220]}")
    return "; ".join(parts) or json.dumps(tool_input)[:220]


def trace(transcript):
    calls, usage_by_message = [], {}
    for line in Path(transcript).read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        message = row.get("message") or {}
        if row.get("type") != "assistant" or not isinstance(message.get("content"), list):
            continue
        if message.get("usage"):
            usage_by_message[message.get("id") or row.get("uuid")] = message["usage"]
        for block in message["content"]:
            if block.get("type") == "tool_use":
                calls.append(f"{block.get('name')}: {summarize(block.get('input') or {})}")
    totals = {key: sum(int(u.get(key) or 0) for u in usage_by_message.values())
              for key in ("input_tokens", "cache_creation_input_tokens",
                          "cache_read_input_tokens", "output_tokens")}
    lines = ["# Trace", "",
             f"Assistant messages: {len(usage_by_message)}; tool calls: {len(calls)}", "",
             "| Tokens | Count |", "| --- | --- |"]
    lines += [f"| {key} | {value} |" for key, value in totals.items()]
    lines += [f"| total processed | {sum(totals.values())} |", "", "## Tool calls", ""]
    lines += [f"{number}. {call}" for number, call in enumerate(calls, 1)]
    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) not in (3, 4, 5):
        sys.exit("usage: python -I collect_orchestration_run.py RUN_DIR GRADE_DIR "
                 "[TRANSCRIPT] [SKILL_DIR]")
    run_dir, grade_dir = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    transcript = sys.argv[3] if len(sys.argv) > 3 else None
    skill_dir = Path(sys.argv[4]).resolve() if len(sys.argv) > 4 else None
    repo = run_dir / "ledgerly"
    if grade_dir.exists():
        sys.exit(f"{grade_dir} exists")
    shutil.copytree(run_dir / "out", grade_dir / "out")
    untracked = git(repo, "ls-files", "--others", "--exclude-standard").split()
    for name in untracked:
        target = grade_dir / "untracked" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(repo / name, target)
    parts = [
        "$ git status --short --untracked-files=all\n"
        + git(repo, "status", "--short", "--untracked-files=all"),
        "$ git log --oneline -1\n" + git(repo, "log", "--oneline", "-1"),
        "$ git diff\n" + git(repo, "diff"),
    ]
    (grade_dir / "state.txt").write_text("\n".join(parts), encoding="utf-8")
    if transcript:
        (grade_dir / "trace.md").write_text(trace(transcript), encoding="utf-8")
    replacements = [(str(run_dir), "<RUN_DIR>"), (run_dir.as_posix(), "<RUN_DIR>")]
    if skill_dir:
        replacements = [(str(skill_dir), "<GUIDE>"), (skill_dir.as_posix(), "<GUIDE>")] \
            + replacements
    for path in grade_dir.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            for old, new in replacements:
                text = text.replace(old, new).replace(old.replace("/", "\\\\"), new)
            path.write_text(text, encoding="utf-8")
    print(f"collected {run_dir.name} -> {grade_dir}")


if __name__ == "__main__":
    main()
