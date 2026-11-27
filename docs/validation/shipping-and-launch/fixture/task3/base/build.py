"""Render content/*.md to site/*.html with the shared footer."""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def render_line(line):
    if line.startswith("# "):
        return f"<h1>{html.escape(line[2:])}</h1>"
    text = LINK.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', html.escape(line, quote=False))
    return f"<li>{text[2:]}</li>" if line.startswith("- ") else f"<p>{text}</p>"


def build(out=ROOT / "site"):
    footer = (ROOT / "templates" / "footer.html").read_text(encoding="utf-8").strip()
    for source in (ROOT / "content").rglob("*.md"):
        lines = [render_line(l) for l in source.read_text(encoding="utf-8").splitlines() if l.strip()]
        target = out / source.relative_to(ROOT / "content").with_suffix(".html")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("<html><body>\n" + "\n".join(lines) + f"\n{footer}\n</body></html>\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    print(f"built {build(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'site')}")
