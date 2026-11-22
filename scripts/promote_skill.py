"""Promote a skill branch to main: pin it, run main's checks, open a pull request.

Usage:
  python scripts/promote_skill.py <skill> [--ref REF] [--dry-run] [--auto-merge]

Run it from any checkout of main. It works in its own clone at
`.git/promote/<skill>`, never in your checkout. It pins `origin/<branch>` (or
--ref) in release_manifest.json on a `promote/<skill>` branch made from
origin/main, runs scripts/ci_checks.py with skill refs pointing at the pins, and
only when every check passes pushes the branch and opens a PR. Merge that PR after its CI is green; `ai-rules setup` then
installs the new pin. If a check fails, nothing is pushed and the clone is kept:
fix the skill on its branch, or fix main's tests inside the clone, then rerun.
"""

import argparse
import datetime
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path("src/ai_rules/release/data/release_manifest.json")


def _load(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(f"{name}.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], text=True, encoding="utf-8",
                            capture_output=True)
    if check and result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def gh(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], cwd=cwd, text=True, encoding="utf-8", capture_output=True)


def update_manifest(manifest: dict, skill: str, commit: str, today: str) -> dict:
    """Return a copy pinning `skill` at `commit`, with a new release sequence."""
    if skill not in manifest.get("first_party", {}):
        raise KeyError(skill)
    result = json.loads(json.dumps(manifest))
    sequence = int(result.get("release_sequence", 0)) + 1
    entry = result["first_party"][skill]
    entry["commit"] = commit
    entry["release_sequence"] = sequence
    result["release_sequence"] = sequence
    result["verified_at"] = today
    return result


def prepare_clone(root: Path, workdir: Path, branch: str, reuse: bool) -> None:
    if workdir.exists() and not reuse:
        shutil.rmtree(workdir, onerror=lambda func, path, _: (Path(path).chmod(0o700), func(path)))
    if not workdir.exists():
        url = git(root, "remote", "get-url", "origin")
        git(root, "clone", "-q", "--no-checkout", str(root), str(workdir))
        git(workdir, "remote", "set-url", "origin", url)
        # threejs-skills has deep example paths; Windows Git needs this to read them.
        git(workdir, "config", "core.longpaths", "true")
        git(workdir, "fetch", "-q", "--no-tags", "origin", "+refs/heads/main:refs/remotes/origin/main")
        git(workdir, "checkout", "-q", "-B", branch, "origin/main")


def open_pr(workdir: Path, branch: str, title: str, body: str, auto_merge: bool, run_gh=gh) -> str:
    existing = run_gh("pr", "view", branch, "--json", "url,state", cwd=workdir)
    if existing.returncode == 0 and json.loads(existing.stdout).get("state") == "OPEN":
        url = json.loads(existing.stdout)["url"]
    else:
        created = run_gh("pr", "create", "--base", "main", "--head", branch, "--title", title,
                         "--body", body, cwd=workdir)
        if created.returncode:
            raise RuntimeError(f"gh pr create failed: {created.stderr.strip()}")
        url = created.stdout.strip().splitlines()[-1]
    if auto_merge:
        merged = run_gh("pr", "merge", url, "--auto", "--squash", cwd=workdir)
        if merged.returncode:
            raise RuntimeError(f"gh pr merge --auto failed: {merged.stderr.strip()}")
    return url


def promote(skill: str, ref: str | None = None, dry_run: bool = False, auto_merge: bool = False,
            root: Path = ROOT, checks=None, run_gh=gh, today: str | None = None) -> int:
    skill_refs = _load("skill_refs")
    checks = checks or _load("ci_checks").run
    branch = f"promote/{skill}"
    # Inside the shared .git directory: never tracked by any branch, one per repository.
    workdir = Path(git(root, "rev-parse", "--path-format=absolute", "--git-common-dir")) / "promote" / skill

    git(root, "fetch", "-q", "--no-tags", "origin", "+refs/heads/main:refs/remotes/origin/main")
    manifest = json.loads(git(root, "show", f"origin/main:{MANIFEST.as_posix()}"))
    pin = manifest.get("first_party", {}).get(skill)
    if pin is None:
        print(f"FAIL: {skill} is not pinned on main. A new skill is added on main first; "
              "see AGENTS.md, 'Adding or removing a skill'.", file=sys.stderr)
        return 2
    source = pin["branch"]
    git(root, "fetch", "-q", "--no-tags", "origin", f"+refs/heads/{source}:refs/remotes/origin/{source}")
    target = git(root, "rev-parse", f"{ref or 'origin/' + source}^{{commit}}")

    reuse = False
    if workdir.exists():
        view = run_gh("pr", "view", branch, "--json", "state", cwd=workdir)
        is_open = view.returncode == 0 and json.loads(view.stdout).get("state") == "OPEN"
        reuse = is_open or bool(git(workdir, "status", "--porcelain", check=False))
    prepare_clone(root, workdir, branch, reuse=reuse)
    if reuse:
        print(f"Reusing {workdir} (open PR or local fixes present)")

    current = json.loads((workdir / MANIFEST).read_text(encoding="utf-8"))
    old = current["first_party"][skill]["commit"]
    if old != target:
        updated = update_manifest(current, skill, target, today or datetime.date.today().isoformat())
        (workdir / MANIFEST).write_text(json.dumps(updated, indent=2) + "\n", encoding="utf-8", newline="\n")
    changed = git(workdir, "status", "--porcelain")
    if not changed and not git(workdir, "rev-list", "origin/main..HEAD"):
        print(f"{skill} on main already pins {target[:12]}; nothing to promote.")
        return 0

    print(f"Pinning {skill}: {old[:12]} -> {target[:12]}")
    try:
        skill_refs.pin(workdir)
    except (ValueError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: cannot read pinned commits ({exc}). Push the skill branch first.", file=sys.stderr)
        return 1
    passed, step = checks(workdir)
    if not passed:
        print(f"\nFAIL at '{step}'. Nothing was pushed.\n"
              f"- Skill problem: fix it on branch {source}, push, and rerun this command.\n"
              f"- Main's tests or data are out of date: edit them in {workdir} and rerun;\n"
              f"  your edits are committed together with the pin.", file=sys.stderr)
        return 1
    if dry_run:
        print("Dry run: checks passed; nothing committed or pushed.")
        return 0

    log = git(workdir, "log", "--oneline", "--no-decorate", f"{old}..{target}") if old != target else ""
    if changed:
        git(workdir, "add", "-A")
        git(workdir, "commit", "-q", "-m", f"Promote {skill} to {target[:7]}")
    git(workdir, "push", "-q", "--force-with-lease", "origin", f"HEAD:refs/heads/{branch}")
    body = (f"Pins `{skill}` at `{target}` (was `{old}`).\n\n"
            f"Skill commits:\n```\n{log or '(no new skill commits)'}\n```\n\n"
            "`scripts/ci_checks.py` passed locally against the new pins. "
            "Merge when CI is green; `ai-rules setup` installs the new pin after the merge.\n")
    url = open_pr(workdir, branch, f"Promote {skill} to {target[:7]}", body, auto_merge, run_gh)
    print(f"PR: {url}\nWatch its checks; merge when they are green.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("skill")
    parser.add_argument("--ref", help="commit or ref to pin instead of the branch head on origin")
    parser.add_argument("--dry-run", action="store_true", help="run the checks but do not commit, push or open a PR")
    parser.add_argument("--auto-merge", action="store_true", help="ask GitHub to merge the PR once its checks pass")
    args = parser.parse_args()
    try:
        return promote(args.skill, args.ref, args.dry_run, args.auto_merge)
    except RuntimeError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
