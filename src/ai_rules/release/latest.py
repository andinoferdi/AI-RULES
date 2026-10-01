"""Resolve configured skill branches and reconcile observable installation content."""

from dataclasses import replace
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile
import uuid

from ai_rules.domain.models import ActualState, InstallationPlan, Operation
from ai_rules.domain.statuses import InstalledOwnership, ReconciliationAction, ReconciliationAssessment, TargetStatus
from ai_rules.execution.executor import copy_tree_atomic
from ai_rules.hosts.adapters import build_host_adapters
from ai_rules.release.bundles import export_git_ref


def git(root: Path, *args: str) -> str:
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    result = subprocess.run(["git", "-C", str(root), *args], env=env, text=True,
                            encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    if result.returncode:
        raise ValueError(f"Git source check failed: {result.stderr.strip()}")
    return result.stdout.strip()


def contents(root: Path) -> dict[str, str]:
    """Compare all installed files, including extras, while tolerating Git CRLF checkout."""
    if not root.exists():
        return {}
    result = {}
    for directory, folders, files in os.walk(root, followlinks=False):
        parent = Path(directory)
        if parent == root and ".git" in folders:
            folders.remove(".git")
        for name in folders + files:
            path = parent / name
            if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
                raise ValueError("Nested links are preserved; resolve them before updating this skill")
        for name in files:
            path = parent / name
            if parent == root and name == ".git":
                continue
            data = path.read_bytes()
            if path.suffix.lower() in {".md", ".json", ".txt", ".yaml", ".yml"}:
                data = data.replace(b"\r\n", b"\n")
            result[path.relative_to(root).as_posix()] = hashlib.sha1(
                b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    return result


def canonical_source(value: str) -> str:
    if "://" not in value and not value.startswith("git@"):
        return str(Path(value).resolve())
    return value.rstrip("/").removesuffix(".git")


class LatestSources:
    def __init__(self, catalog, capability_ids):
        self.workspace = tempfile.TemporaryDirectory(prefix="ai-rules-sources-")
        self.root = Path(self.workspace.name)
        self.sources = {}
        self.entries = {}
        self.installers = {}
        self.expected = {}
        self._trees = {}
        try:
            groups = {}
            for identifier in dict.fromkeys(capability_ids):
                capability = catalog.require_capability(identifier)
                repository = capability.source["repository"]
                branch = capability.source["branch"]
                groups.setdefault(repository, []).append((identifier, branch))
            for index, (repository, selections) in enumerate(groups.items()):
                local = self.root / f"source-{index}"
                local.mkdir()
                git(local, "init", "--bare")
                for _, branch in selections:
                    git(local, "check-ref-format", f"refs/heads/{branch}")
                refs = [f"+refs/heads/{branch}:refs/heads/{branch}" for _, branch in selections]
                git(local, "fetch", "--no-tags", "--", repository, *dict.fromkeys(refs))
                for identifier, branch in selections:
                    commit = git(local, "rev-parse", f"refs/heads/{branch}^{{commit}}")
                    self.entries[identifier] = (local, repository, branch, commit)
                    self.sources[identifier] = self.bundle(identifier)
        except Exception:
            self.close()
            raise

    def close(self):
        self.workspace.cleanup()

    def tree(self, local, commit):
        key = (str(local), commit)
        if key not in self._trees:
            result = {}
            for entry in git(local, "ls-tree", "-rz", commit).split("\0"):
                if not entry:
                    continue
                metadata, name = entry.split("\t", 1)
                mode, kind, blob = metadata.split()
                path = PurePosixPath(name)
                if mode not in {"100644", "100755"} or kind != "blob":
                    raise ValueError(f"Unsupported source entry: {name}")
                if path.is_absolute() or any(part in {"..", ".git"} for part in path.parts) or "\\" in name or ":" in name:
                    raise ValueError("Unsafe path in skill source")
                result[name] = blob
            self._trees[key] = result
        return self._trees[key]

    def bundle(self, identifier):
        local, _, _, commit = self.entries[identifier]
        files = self.tree(local, commit)
        if "SKILL.md" not in files:
            raise ValueError(f"Source branch for {identifier} has no SKILL.md")
        target = self.root / "bundles" / identifier
        export_git_ref(commit, target, repo_root=local)
        body = (target / "SKILL.md").read_text(encoding="utf-8")
        if not re.search(rf"^name:\s*{re.escape(identifier)}\s*$", body, re.M):
            raise ValueError(f"Skill identity does not match {identifier}")
        return target

    def version(self, identifier, commit=None):
        return f"git-branch:{identifier}@{commit or self.entries[identifier][3]}"

    def known_revision(self, identifier, actual):
        local, _, _, head = self.entries[identifier]
        # Adoption is bounded. Older/unrecognized copies remain protected, never assumed current.
        candidates = git(local, "rev-list", "--max-count=256", head).splitlines()
        for commit in candidates:
            if self.tree(local, commit) == actual:
                return commit
        return None

    def reconcile(self, plan, catalog, args):
        adapters = build_host_adapters(catalog.hosts)
        targets = []
        for target in plan.targets:
            if target.strategy_id is None:
                targets.append(target)
                continue
            identifier = target.capability_id
            local, repository, branch, head = self.entries[identifier]
            root = adapters[target.host_id].skill_target(target.scope, args.project_root)
            original = root / identifier
            destination = original.resolve()
            key = (identifier, target.host_id)
            version = self.version(identifier)
            try:
                if not original.exists():
                    aliases = adapters[target.host_id].skill_discovery_roots(target.scope, args.project_root)[1:]
                    if any((alias / identifier).exists() for alias in aliases):
                        raise ValueError("An installation in another discovery root is preserved; reconcile it explicitly")
                before = contents(destination)
                is_git = (destination / ".git").exists()
                installed = None
                if is_git:
                    if Path(git(destination, "rev-parse", "--show-toplevel")).resolve() != destination:
                        raise ValueError("Nested Git checkout is preserved")
                    if canonical_source(git(destination, "remote", "get-url", "origin")) != canonical_source(repository):
                        raise ValueError("Git origin differs from the configured skill source")
                    if git(destination, "branch", "--show-current") != branch:
                        raise ValueError("Git branch differs from the configured skill branch")
                    if git(destination, "status", "--porcelain", "--untracked-files=all", "--ignored=matching"):
                        raise ValueError("Git checkout has local or ignored files; preserve them before updating")
                    installed = git(destination, "rev-parse", "HEAD")
                    try:
                        git(local, "merge-base", "--is-ancestor", installed, head)
                    except ValueError as exc:
                        raise ValueError("Local Git revision is not an ancestor of the fetched branch; no automatic downgrade or history rewrite") from exc
                elif destination.exists():
                    installed = self.known_revision(identifier, before)
                    if installed is None:
                        raise ValueError("Local content is modified or unrecognized; preserved. Use explicit repair only after review")
                if not destination.exists():
                    action, reason = ReconciliationAction.INSTALL, "latest source revision resolved"
                elif before == self.tree(local, head) and (not is_git or installed == head):
                    action, reason = ReconciliationAction.NO_OP, "full content matches the freshly fetched branch"
                else:
                    action, reason = ReconciliationAction.UPDATE, "clean official installation is behind the source branch"
                self.expected[key] = self.tree(local, head)
                self.installers[key] = self._installer(identifier, original, destination, before, is_git, installed, args.state_dir)
                actual = ActualState(exists=destination.exists(), ownership=InstalledOwnership.MANAGED_BY_AI_RULES,
                                     installed_version=self.version(identifier, installed) if installed else None,
                                     healthy=bool(before), content_matches=action == ReconciliationAction.NO_OP)
                operations = () if action == ReconciliationAction.NO_OP else (Operation(
                    kind="capability_operation", capability_id=identifier, host_id=target.host_id, scope=target.scope,
                    action=action, source=repository, target=str(original), reason=reason,
                    backup=action == ReconciliationAction.UPDATE, reversible=True),)
                targets.append(replace(target, action=action, actual=actual, target_version=version, reason=reason,
                                       operations=operations, status=TargetStatus.VERIFIED if action == ReconciliationAction.NO_OP else TargetStatus.PLANNED,
                                       assessment=ReconciliationAssessment.CURRENT if action == ReconciliationAction.NO_OP else ReconciliationAssessment.UPDATE_AVAILABLE))
            except (ValueError, OSError) as exc:
                targets.append(replace(target, action=ReconciliationAction.BLOCK, target_version=version,
                                       status=TargetStatus.BLOCKED, assessment=ReconciliationAssessment.VERSION_UNKNOWN,
                                       reason=str(exc), operations=()))
        return InstallationPlan(plan.schema_version, plan.profile_id, tuple(targets))

    def _installer(self, identifier, original, destination, before, is_git, installed, state_dir):
        def install():
            local, _, branch, commit = self.entries[identifier]
            expected = self.tree(local, commit)
            if original.resolve() != destination:
                raise ValueError("Installation link changed after planning; refusing to replace it")
            if (destination / ".git").exists() != is_git:
                raise ValueError("Git ownership changed after planning")
            if is_git:
                if git(destination, "branch", "--show-current") != branch:
                    raise ValueError("Git branch changed after planning")
                if git(destination, "status", "--porcelain", "--untracked-files=all", "--ignored=matching"):
                    raise ValueError("Git checkout is no longer clean")
            current = contents(destination)
            # Another selected host may share this exact path through a junction.
            if current == expected and (not is_git or git(destination, "rev-parse", "HEAD") == commit):
                return original
            if current != before:
                raise ValueError("Skill changed after planning; rerun setup after reviewing local edits")
            if is_git:
                if git(destination, "rev-parse", "HEAD") != installed or git(destination, "branch", "--show-current") != branch:
                    raise ValueError("Git checkout changed after planning")
                backup = state_dir / "backups" / uuid.uuid4().hex / identifier
                shutil.copytree(destination, backup)
                git(destination, "fetch", "--no-tags", str(local), f"{commit}:refs/remotes/origin/{branch}")
                git(destination, "merge", "--ff-only", commit)
            else:
                copy_tree_atomic(self.sources[identifier], destination, state_dir / "backups",
                                 verify=lambda path: contents(path) == expected)
            if contents(destination) != expected:
                raise ValueError("Installed content differs from the resolved source; backup retained")
            return original
        return install
