"""Export a runner's Claude Code subagent transcript to Markdown for blind grading.

Keeps every tool call in order with a truncated result and the runner's own text, replaces
the run folder path with <RUN>, and hides reads of the guidance folder so the grader cannot
tell which skill (if any) the runner had.

    python export_transcript.py AGENT_JSONL RUN_DIR OUT_MD
"""
import json
import re
import sys
from pathlib import Path

MAX_LINES = 60


def clip(text: str) -> str:
    lines = text.splitlines()
    if len(lines) > MAX_LINES:
        lines = lines[:MAX_LINES] + [f"... ({len(lines) - MAX_LINES} more lines)"]
    return "\n".join(lines)


def result_text(content) -> str:
    if isinstance(content, str):
        return content
    parts = []
    for item in content or []:
        if isinstance(item, dict) and item.get("type") == "text":
            parts.append(item.get("text", ""))
    return "\n".join(parts)


def main() -> int:
    transcript, run_dir, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    run_variants = {run_dir, run_dir.replace("\\", "/"), run_dir.replace("/", "\\"),
                    run_dir.replace("\\", "\\\\")}

    def blind(text: str) -> str:
        for variant in sorted(run_variants, key=len, reverse=True):
            text = text.replace(variant, "<RUN>")
        text = re.sub(r"<RUN>[\\/]+guide[\\/][^\s'\"`)]*", "<RUN>/[guidance]", text)
        return re.sub(r"\bSKILL\.md\b|\bGUIDE\.md\b", "[guidance]", text)

    entries = [json.loads(line) for line in transcript.read_text(encoding="utf-8").splitlines()
               if line.strip()]
    pending, hidden, blocks, step = {}, set(), [], 0
    first_user_seen = False
    for entry in entries:
        message = entry.get("message") or {}
        content = message.get("content")
        if entry.get("type") == "user" and not first_user_seen:
            first_user_seen = True  # the run prompt is identical for every arm
            continue
        if entry.get("type") == "assistant" and isinstance(content, list):
            for item in content:
                if item.get("type") == "text" and item.get("text", "").strip():
                    blocks.append("> " + blind(item["text"]).strip().replace("\n", "\n> "))
                elif item.get("type") == "tool_use":
                    step += 1
                    raw = json.dumps(item.get("input", {}), ensure_ascii=False)
                    if re.search(r"[\\/]guide[\\/]|[\\/]guide\"", raw) and item["name"] in (
                            "Read", "Glob", "Grep"):
                        hidden.add(item["id"])
                        blocks.append(f"### {step}. {item['name']}\n[reads guidance]")
                        continue
                    shown = item.get("input", {})
                    if item["name"] == "Bash":
                        body = "$ " + shown.get("command", "")
                    elif item["name"] in ("Write",):
                        body = f"{shown.get('file_path')}\n---\n{clip(shown.get('content', ''))}"
                    elif item["name"] in ("Edit",):
                        body = (f"{shown.get('file_path')}\n--- old\n{clip(shown.get('old_string', ''))}"
                                f"\n--- new\n{clip(shown.get('new_string', ''))}")
                    else:
                        body = raw
                    pending[item["id"]] = step
                    blocks.append(f"### {step}. {item['name']}\n```\n{blind(body)}\n```")
        elif entry.get("type") == "user" and isinstance(content, list):
            for item in content:
                if item.get("type") != "tool_result" or item.get("tool_use_id") in hidden:
                    continue
                text = clip(blind(result_text(item.get("content"))))
                blocks.append(f"Result of step {pending.get(item.get('tool_use_id'), '?')}:\n```\n{text}\n```")
    out.write_text("# Runner transcript\n\n" + "\n\n".join(blocks) + "\n", encoding="utf-8")
    print(f"wrote {out} ({step} tool calls, {len(hidden)} guidance reads hidden)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
