"""Export notes to a Markdown file, oldest first."""
import argparse
import json
import sys
from pathlib import Path


def load_notes(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def to_markdown(notes) -> str:
    lines = []
    for note in sorted(notes, key=lambda item: item["created"]):
        lines.append(f"## {note['title']}")
        lines.append("")
        lines.append(note["body"].strip()))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("--out", default="notes.md")
    args = parser.parse_args(argv)
    Path(args.out).write_text(to_markdown(load_notes(args.source)), encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
