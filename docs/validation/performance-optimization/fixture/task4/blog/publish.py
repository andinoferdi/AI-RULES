import argparse
import time
from pathlib import Path

from .slug import slugify

UPLOAD_SECONDS_PER_MB = 1.1  # measured CDN upload rate from the office connection


def render(markdown):
    html = []
    for line in markdown.splitlines():
        if line.startswith("# "):
            html.append(f"<h1>{line[2:]}</h1>")
        elif line.strip():
            html.append(f"<p>{line}</p>")
    return "\n".join(html)


def upload(payload_mb, dry_run):
    seconds = payload_mb * UPLOAD_SECONDS_PER_MB
    if not dry_run:
        time.sleep(seconds)
    return seconds


def main():
    parser = argparse.ArgumentParser(description="Publish one article.")
    parser.add_argument("article", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    markdown = args.article.read_text(encoding="utf-8")
    title = markdown.splitlines()[0].lstrip("# ").strip()

    start = time.perf_counter()
    slug = slugify(title)
    slug_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    html = render(markdown)
    render_ms = (time.perf_counter() - start) * 1000

    images_mb = 2.6  # typical article: three photos
    upload_s = upload(images_mb + len(html) / 1e6, args.dry_run)
    print(f"slug={slug} slug_ms={slug_ms:.3f} render_ms={render_ms:.3f} "
          f"upload_s={upload_s:.2f}{' (estimated, dry run)' if args.dry_run else ''}")


if __name__ == "__main__":
    main()
