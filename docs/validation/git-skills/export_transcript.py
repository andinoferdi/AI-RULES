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
    """Keep the start and the end of long output; results and timings are usually last."""
    lines = text.splitlines()
    if len(lines) > MAX_LINES:
        head, tail = MAX_LINES // 3, MAX_LINES - MAX_LINES // 3
        lines = lines[:head] + [f"... ({len(lines) - MAX_LINES} lines omitted)"] + lines[-tail:]
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
        text = re.sub(r"[^\s'\"`]*trial[\\/]+run-\d+", "<RUN>", text)
        text = re.sub(r"\brun-\d+\b", "run-X", text)
        for name in guide_names:  # skill folder names would reveal the arm
            text = re.sub(r"(?<![\w-])" + re.escape(name) + r"(?![\w-])", "[guidance]", text)
        text = re.sub(r"(?<=[\\/])pr(?=[\\/])|^pr(?=[\\/])", "[guidance]", text, flags=re.M)
        text = re.sub(r"git-guardrails|guardrails skill|superpowers|\bobra\b|Pocock|"
                      r"\bandino\b|Andino|`pr` skill|\bpr skill", "[guidance]", text)
        return re.sub(r"\bSKILL\.md\b|\bGUIDE\.md\b", "[guidance]", text)

    guide_lines = set()
    guide = Path(run_dir) / "guide"
    guide_names = sorted((p.name for p in guide.iterdir() if p.is_dir() and len(p.name) > 3),
                         key=len, reverse=True) if guide.is_dir() else []
    if guide.is_dir():
        for path in guide.rglob("*"):
            guide_lines.update({path.name, path.name + "/", path.relative_to(guide).as_posix()})
            if path.is_file():
                guide_lines.update(line.strip() for line in
                                   path.read_text(encoding="utf-8", errors="ignore").splitlines()
                                   if len(line.strip()) >= 8)

    def strip_guidance(text: str) -> str:
        """Drop output lines copied from the guidance files (a runner may cat them)."""
        kept, dropping = [], False
        for line in text.splitlines():
            bare = re.sub(r"^\s*\d+\t", "", line).strip().replace("\\", "/")
            listed = re.sub(r"\s+\d+(\.\d+)?[KMG]?B?$", "", bare)  # "name  8.5K" in a listing
            in_guide_tree = any(listed.startswith(n + "/") or listed.startswith("./" + n + "/")
                                for n in guide_names)
            if (bare in guide_lines or listed in guide_lines or in_guide_tree
                    or bare in ("guide/", "guide")):
                if not dropping:
                    kept.append("[guidance text removed]")
                dropping = True
                continue
            dropping = False
            kept.append(line)
        return "\n".join(kept)

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
                    if item["name"] in ("Bash", "PowerShell"):
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
                text = clip(blind(strip_guidance(result_text(item.get("content")))))
                blocks.append(f"Result of step {pending.get(item.get('tool_use_id'), '?')}:\n```\n{text}\n```")
    out.write_text("# Runner transcript\n\n" + "\n\n".join(blocks) + "\n", encoding="utf-8")
    print(f"wrote {out} ({step} tool calls, {len(hidden)} guidance reads hidden)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
