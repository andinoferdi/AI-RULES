#!/usr/bin/env python3
"""
delegation_workspace.py — Cross-platform workspace resolver for Andino Delegation.
Resolves and initializes an isolated scratch workspace for a given plan file.
Zero external dependencies (Python 3.8+ stdlib).
"""

import os
import subprocess
import sys
from pathlib import Path

def get_repo_root() -> Path:
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True
        )
        return Path(res.stdout.strip()).resolve()
    except Exception:
        # Fallback to traversing upwards for .git
        curr = Path.cwd().resolve()
        for p in [curr] + list(curr.parents):
            if (p / ".git").exists():
                return p
        return curr

def resolve_workspace(plan_path_str: str) -> Path:
    plan_file = Path(plan_path_str).resolve()
    if not plan_file.exists():
        sys.stderr.write(f"Error: plan file not found: {plan_file}\n")
        sys.exit(2)

    repo_root = get_repo_root()
    override = os.environ.get("ANDINO_WORKSPACE_OVERRIDE")
    if override:
        base_dir = Path(override).resolve()
    else:
        base_dir = repo_root / ".andino" / "delegation"
    base_dir.mkdir(parents=True, exist_ok=True)

    # Ensure self-protecting .gitignore (repo root only, not when overridden)
    if not override:
        gitignore = repo_root / ".andino" / ".gitignore"
        if not gitignore.exists() or "*" not in gitignore.read_text(encoding="utf-8", errors="ignore"):
            try:
                gitignore.write_text("*\n!.gitignore\n", encoding="utf-8")
            except Exception:
                pass

    slug = plan_file.stem
    if not slug or slug in (".", ".."):
        slug = "workspace"

    try:
        plan_id = str(plan_file.relative_to(repo_root)).replace("\\", "/")
    except ValueError:
        plan_id = str(plan_file).replace("\\", "/")

    def owns(d: Path) -> bool:
        marker = d / "plan-path"
        if marker.exists():
            try:
                return marker.read_text(encoding="utf-8").strip() == plan_id
            except Exception:
                return False
        d.mkdir(parents=True, exist_ok=True)
        marker.write_text(plan_id + "\n", encoding="utf-8")
        return True

    target_dir = base_dir / slug
    if not owns(target_dir):
        parent_slug = plan_file.parent.name or "plan"
        target_dir = base_dir / f"{slug}-{parent_slug}"
        if not owns(target_dir):
            counter = 2
            while not owns(base_dir / f"{slug}-{parent_slug}-{counter}"):
                counter += 1
            target_dir = base_dir / f"{slug}-{parent_slug}-{counter}"

    return target_dir.resolve()

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: delegation_workspace.py PLAN_FILE\n")
        sys.exit(2)

    workspace = resolve_workspace(sys.argv[1])
    print(str(workspace).replace("\\", "/"))

if __name__ == "__main__":
    main()
