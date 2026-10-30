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
from ai_rules.release.bundles import export_git_ref, validate_subpath
from ai_rules.events import emit


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
            if path.suffix.lower() in {".md", ".json", ".txt", ".yaml", ".yml", ".py"}:
                data = data.replace(b"\r\n", b"\n")
            result[path.relative_to(root).as_posix()] = hashlib.sha1(
                b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    return result


def canonical_source(value: str) -> str:
    if "://" not in value and not value.startswith("git@"):
        return str(Path(value).resolve())
    return value.rstrip("/").removesuffix(".git")


class LatestSources:
    def __init__(self, catalog, capability_ids, reporter=None):
        self.reporter = reporter
        emit(reporter, "Checking source configuration")
        self.workspace = tempfile.TemporaryDirectory(prefix="ai-rules-sources-")
        self.root = Path(self.workspace.name)
        self.sources = {}
        self.entries = {}
        self.installers = {}
        self.expected = {}
        self.expected_members = {}
        self._trees = {}
        self.subpaths = {}
        try:
            groups = {}
            for identifier in dict.fromkeys(capability_ids):
                capability = catalog.require_capability(identifier)
                self.subpaths[identifier] = validate_subpath(capability.source.get("subpath"))
                repository = capability.source["repository"]
                branch = capability.source["branch"]
                groups.setdefault(repository, []).append((identifier, branch))
            bundle_total = sum(len(selections) for selections in groups.values())
            bundle_completed = 0
            for index, (repository, selections) in enumerate(groups.items()):
                emit(reporter, "Fetching remote branches", completed=index, total=len(groups))
                local = self.root / f"source-{index}"
                local.mkdir()
                git(local, "init", "--bare")
                for _, branch in selections:
                    git(local, "check-ref-format", f"refs/heads/{branch}")
                refs = [f"+refs/heads/{branch}:refs/heads/{branch}" for _, branch in selections]
                git(local, "fetch", "--no-tags", "--", repository, *dict.fromkeys(refs))
                emit(reporter, "Remote branches fetched", completed=index + 1, total=len(groups))
                for identifier, branch in selections:
                    emit(reporter, "Preparing source bundle", capability=identifier,
                         completed=bundle_completed, total=bundle_total)
                    commit = git(local, "rev-parse", f"refs/heads/{branch}^{{commit}}")
                    self.entries[identifier] = (local, repository, branch, commit)
                    self.sources[identifier] = self.bundle(identifier)
                    bundle_completed += 1
                    emit(reporter, "Source bundle prepared", capability=identifier,
                         completed=bundle_completed, total=bundle_total)
        except BaseException:
            self.close()
            raise

    def close(self):
        self.workspace.cleanup()

    def tree(self, local, commit, subpath=None):
        subpath = validate_subpath(subpath)
        key = (str(local), commit, subpath)
        if key not in self._trees:
            result = {}
            tree_ref = f"{commit}:{subpath}" if subpath else commit
            for entry in git(local, "ls-tree", "-rz", tree_ref).split("\0"):
                if not entry:
                    continue
                metadata, name = entry.split("\t", 1)
                mode, kind, blob = metadata.split()
                path = PurePosixPath(name)
                validate_subpath(name)
                if mode not in {"100644", "100755"} or kind != "blob":
                    raise ValueError(f"Unsupported source entry: {name}")
                if path.is_absolute() or any(part in {"..", ".git"} for part in path.parts) or "\\" in name or ":" in name:
                    raise ValueError("Unsafe path in skill source")
                result[name] = blob
            self._trees[key] = result
        return self._trees[key]

    def bundle(self, identifier):
        local, _, _, commit = self.entries[identifier]
        files = self.tree(local, commit, self.subpaths[identifier])
        if "SKILL.md" not in files:
            raise ValueError(f"Source branch for {identifier} has no SKILL.md")
        target = self.root / "bundles" / identifier
        export_git_ref(commit, target, repo_root=local, subpath=self.subpaths[identifier])
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
            if self.tree(local, commit, self.subpaths[identifier]) == actual:
                return commit
        return None

    def known_member(self, local, head, name, actual):
        for revision in git(local, "rev-list", "--max-count=256", head).splitlines():
            try:
                if actual == self.tree(local, revision, f"skills/{name}"):
                    return True
            except ValueError:
                # A member may not exist in older revisions of the workflow.
                continue
        return False

    def reconcile(self, plan, catalog, args):
        adapters = build_host_adapters(catalog.hosts)
        targets = []
        for index, target in enumerate(plan.targets):
            emit(self.reporter, "Reconciling installed content", host=target.host_id, capability=target.capability_id,
                 completed=index, total=len(plan.targets))
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
                    if self.subpaths[identifier]:
                        raise ValueError("Git checkout for a subpath package is preserved; use a managed directory installation")
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
                elif before == self.tree(local, head, self.subpaths[identifier]) and (not is_git or installed == head):
                    action, reason = ReconciliationAction.NO_OP, "full content matches the freshly fetched branch"
                else:
                    action, reason = ReconciliationAction.UPDATE, "clean official installation is behind the source branch"
                self.expected[key] = self.tree(local, head, self.subpaths[identifier])
                members = {}
                if identifier == "andino-workflow":
                    for member in sorted((self.sources[identifier] / "skills").glob("*")):
                        if not (member / "SKILL.md").is_file():
                            continue
                        native = destination.parent / f"andino-{member.name}"
                        observed = contents(native)
                        desired = contents(member)
                        if observed != desired:
                            if native.exists():
                                if (native / ".git").exists() or not self.known_member(local, head, member.name, observed):
                                    raise ValueError(f"Native member {native.name} is modified or unrecognized; preserved")
                        members[native] = (member, observed, desired)
                    if any(observed != desired for _, observed, desired in members.values()) and action == ReconciliationAction.NO_OP:
                        action, reason = ReconciliationAction.UPDATE, "native workflow members need synchronization"
                self.expected_members[key] = {native: desired for native, (_, _, desired) in members.items()}
                self.installers[key] = self._installer(identifier, original, destination, before, is_git, installed, args.state_dir, members)
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
        emit(self.reporter, "Reconciliation complete", completed=len(targets), total=len(plan.targets))
        return InstallationPlan(plan.schema_version, plan.profile_id, tuple(targets))

    def matches(self, identifier, host, destination):
        key = (identifier, host)
        try:
            return (contents(destination) == self.expected[key]
                    and all(contents(native) == desired
                            for native, desired in self.expected_members.get(key, {}).items()))
        except (ValueError, OSError):
            return False

    def _installer(self, identifier, original, destination, before, is_git, installed, state_dir, members):
        def install():
            emit(self.reporter, "Checking target before installation", capability=identifier)
            local, _, branch, commit = self.entries[identifier]
            expected = self.tree(local, commit, self.subpaths[identifier])
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
            for native, (_, observed, desired) in members.items():
                if contents(native) not in (observed, desired):
                    raise ValueError("Native member changed after planning; preserved")

            def sync_members():
                for native, (source, _, desired) in members.items():
                    if contents(native) != desired:
                        copy_tree_atomic(source, native, state_dir / "backups",
                                         verify=lambda path, wanted=desired: contents(path) == wanted,
                                         reporter=self.reporter)
            # Another selected host may share this exact path through a junction.
            if current == expected and (not is_git or git(destination, "rev-parse", "HEAD") == commit):
                sync_members()
                return original
            if current != before:
                raise ValueError("Skill changed after planning; rerun setup after reviewing local edits")
            if is_git:
                if git(destination, "rev-parse", "HEAD") != installed or git(destination, "branch", "--show-current") != branch:
                    raise ValueError("Git checkout changed after planning")
                backup = state_dir / "backups" / uuid.uuid4().hex / identifier
                emit(self.reporter, "Backing up Git checkout", capability=identifier)
                shutil.copytree(destination, backup)
                emit(self.reporter, "Fetching resolved revision into checkout", capability=identifier)
                git(destination, "fetch", "--no-tags", str(local), f"{commit}:refs/remotes/origin/{branch}")
                emit(self.reporter, "Fast-forwarding checkout", capability=identifier)
                git(destination, "merge", "--ff-only", commit)
            else:
                copy_tree_atomic(self.sources[identifier], destination, state_dir / "backups",
                                 verify=lambda path: contents(path) == expected, reporter=self.reporter)
            sync_members()
            emit(self.reporter, "Verifying installed content", capability=identifier)
            if contents(destination) != expected:
                raise ValueError("Installed content differs from the resolved source; backup retained")
            return original
        return install
