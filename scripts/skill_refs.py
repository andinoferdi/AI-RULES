"""Point skill branch refs at the commits pinned in the release manifest.

Validators and tests read skill content through `origin/<branch>` (and in CI
`<branch>`). `pin` makes those names resolve to the pinned commit, so a push to a
skill branch cannot change what main validates. `drift` lists branches whose
head has moved past their pin; it is informational and always exits 0.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path("src/ai_rules/release/data/release_manifest.json")


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], text=True, encoding="utf-8",
                          capture_output=True, check=check)


def pins(manifest: dict) -> dict[str, str]:
    """Branch -> pinned commit for every first-party skill and validation source."""
    result = {}
    for section in ("first_party", "validation_refs"):
        for name, entry in manifest.get(section, {}).items():
            branch = entry.get("branch", name)
            if branch in result and result[branch] != entry["commit"]:
                raise ValueError(f"{branch}: two different pins in the manifest")
            result[branch] = entry["commit"]
    return result


def load_manifest(repo: Path) -> dict:
    return json.loads((repo / MANIFEST).read_text(encoding="utf-8"))


def pin(repo: Path, remote: str = "origin", local_branches: bool = False, fetch: bool = True) -> dict[str, str]:
    pinned = pins(load_manifest(repo))
    if fetch:
        refs = [f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}" for branch in pinned]
        git(repo, "fetch", "--no-tags", remote, *refs)
    for branch, commit in pinned.items():
        if git(repo, "cat-file", "-e", f"{commit}^{{commit}}", check=False).returncode:
            if not fetch:
                raise ValueError(f"{branch}: pinned commit {commit} is not in this repository")
            git(repo, "fetch", "--no-tags", remote, commit)
        git(repo, "update-ref", f"refs/remotes/{remote}/{branch}", commit)
        if local_branches:
            current = git(repo, "symbolic-ref", "-q", "--short", "HEAD", check=False).stdout.strip()
            if current == branch:
                raise ValueError(f"{branch} is checked out here; run pin in a separate worktree")
            git(repo, "update-ref", f"refs/heads/{branch}", commit)
    return pinned


def drift(repo: Path, remote: str = "origin") -> list[tuple[str, str, str, int]]:
    rows = []
    for branch, commit in pins(load_manifest(repo)).items():
        head = git(repo, "ls-remote", remote, f"refs/heads/{branch}").stdout.split()
        head = head[0] if head else ""
        ahead = -1
        if head and not git(repo, "cat-file", "-e", f"{head}^{{commit}}", check=False).returncode:
            ahead = int(git(repo, "rev-list", "--count", f"{commit}..{head}").stdout.strip())
        rows.append((branch, commit, head, ahead))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--remote", default="origin")
    sub = parser.add_subparsers(dest="command", required=True)
    pin_parser = sub.add_parser("pin", help="point skill refs at pinned commits")
    pin_parser.add_argument("--local-branches", action="store_true",
                            help="also move refs/heads/<branch>; only for CI or disposable worktrees")
    pin_parser.add_argument("--no-fetch", action="store_true")
    sub.add_parser("drift", help="list skill branches ahead of their pin (always exits 0)")
    args = parser.parse_args()
    if args.command == "pin":
        try:
            pinned = pin(args.repo, args.remote, args.local_branches, not args.no_fetch)
        except (ValueError, subprocess.CalledProcessError) as exc:
            detail = getattr(exc, "stderr", "") or ""
            print(f"FAIL: {exc} {detail}".strip(), file=sys.stderr)
            return 1
        for branch, commit in pinned.items():
            print(f"{branch} -> {commit[:12]}")
        return 0
    print("| Skill branch | Pinned | Branch head | Unpromoted commits |")
    print("| --- | --- | --- | --- |")
    for branch, commit, head, ahead in drift(args.repo, args.remote):
        state = "unknown" if ahead < 0 else str(ahead)
        print(f"| {branch} | {commit[:7]} | {head[:7] or 'missing'} | {state} |")
    print("\nPromote a branch with `python scripts/promote_skill.py <skill>`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
