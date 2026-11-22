"""Find an AI-RULES clone and decide where setup reads skills from."""

from __future__ import annotations

from pathlib import Path

MARKER = Path("src/ai_rules/catalog/data/capabilities.json")
SOURCES = ("auto", "local", "latest", "bundled")


def find_checkout(start: Path) -> Path | None:
    """Closest folder at or above start that is an AI-RULES clone with a skills/ folder."""
    start = Path(start).resolve()
    for folder in (start, *start.parents):
        if (folder / MARKER).is_file() and any((folder / "skills").glob("*/SKILL.md")):
            return folder
    return None


def bundled_revision(cwd: Path | None = None) -> tuple[str, int] | None:
    """(commit, sequence) of the bundled skills; the sequence only grows along main.

    A release executable carries it in bundles/bundle-sources.json. A clone uses
    HEAD and its commit count. Anything else has no comparable revision.
    """
    from importlib import resources
    import json
    import subprocess

    try:
        packaged = resources.files("ai_rules.release.data").joinpath("bundles", "bundle-sources.json")
        data = json.loads(packaged.read_text(encoding="utf-8"))
        return str(data["commit"]), int(data["sequence"])
    except (FileNotFoundError, OSError, TypeError, KeyError, ValueError):
        pass
    checkout = find_checkout(Path.cwd() if cwd is None else cwd)
    if checkout is None:
        return None
    try:
        run = lambda *args: subprocess.run(["git", "-C", str(checkout), *args], text=True, check=True,
                                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.strip()
        return run("rev-parse", "HEAD"), int(run("rev-list", "--count", "HEAD"))
    except (OSError, subprocess.CalledProcessError, ValueError):
        return None


def resolve_source(choice: str, cwd: Path) -> tuple[str, Path | None]:
    """Turn --source into (local|latest|bundled, checkout or None)."""
    if choice not in SOURCES:
        raise ValueError(f"unknown skill source: {choice}")
    checkout = find_checkout(cwd) if choice != "latest" else None
    if choice == "local" and checkout is None:
        raise ValueError("--source local runs inside an AI-RULES clone (a folder with skills/ and src/ai_rules); "
                         "cd into your clone or use --source latest")
    if choice == "auto":
        return ("local", checkout) if checkout else ("latest", None)
    return choice, checkout
