"""Ownership-aware, recoverable workflow-family installation.

Acquisition is deliberately outside this module. All callers supply immutable local
bytes. Transactions coordinate visibility (not an instantaneous multi-path rename).
Only explicit artifact paths in an inventory may be replaced or removed.
"""
from __future__ import annotations

from contextlib import ExitStack, contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import uuid

from ai_rules.hosts.invocation import invocation_paths, invocation_body

FAMILY = 'andino-workflow'


def linked(path):
    return path.is_symlink() or getattr(path, 'is_junction', lambda: False)()


def exists(path):
    return path.exists() or linked(path)


def safe_path(path):
    for parent in (path, *path.parents):
        if linked(parent):
            raise ValueError(f'Linked path is preserved: {parent}')


def git(root, *args):
    import subprocess
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    result = subprocess.run(["git", "-C", str(root), *args], env=env, text=True,
                            encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    if result.returncode:
        raise ValueError(f"Git check failed: {result.stderr.strip()}")
    return result.stdout.strip()


def _conflict(current, recorded):
    if current is None or recorded is None:
        return False
    if current.get('kind') != recorded.get('kind'):
        return True
    if current.get('kind') == 'file':
        return current.get('sha256') != recorded.get('sha256')
    if current.get('kind') == 'git':
        return current.get('commit') != recorded.get('commit')
    if current.get('kind') == 'tree':
        cur_entries = current.get('entries', {})
        rec_entries = recorded.get('entries', {})
        for rel_path, cur_entry in cur_entries.items():
            rec_entry = rec_entries.get(rel_path)
            if rec_entry is None or cur_entry != rec_entry:
                return True
        return False
    return True


def fingerprint(path):
    """Exact full-tree inventory, including empty directories and unexpected files."""
    safe_path(path)
    if not path.exists():
        return None
    if path.is_file():
        return {'kind': 'file', 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    if not path.is_dir():
        raise ValueError(f'Non-regular path is preserved: {path}')
    if (path / '.git').is_dir():
        if git(path, "status", "--porcelain", "--untracked-files=all", "--ignored=matching"):
            raise ValueError(f"Git checkout has local or ignored files; preserve them before updating: {path}")
        return {'kind': 'git', 'commit': git(path, 'rev-parse', 'HEAD')}
    entries = {}
    for directory, folders, files in os.walk(path, followlinks=False):
        for name in sorted(folders + files):
            child = Path(directory) / name
            if linked(child):
                raise ValueError(f'Nested link is preserved: {child}')
            relative = child.relative_to(path).as_posix()
            if name == '.git':
                raise ValueError(f'Nested Git checkout is preserved: {child}')
            if child.is_dir():
                entries[relative] = {'kind': 'directory'}
            elif child.is_file():
                entries[relative] = {'kind': 'file', 'sha256': hashlib.sha256(child.read_bytes()).hexdigest()}
            else:
                raise ValueError(f'Non-regular entry is preserved: {child}')
    return {'kind': 'tree', 'entries': entries}


def manifest(bundle):
    path = bundle / 'references/portfolio.json'
    if not path.exists():
        # Legacy packages install only members actually present; no inferred retirement.
        members = sorted(p.name for p in (bundle / 'skills').glob('*/SKILL.md') for p in [p.parent])
        return {'members': members, 'retired': [], 'resources': []}
    value = json.loads(path.read_text(encoding='utf-8'))
    if value.get('schema_version') != 1 or value.get('installer_protocol') != 1:
        raise ValueError('Unsupported portfolio schema or installer protocol (supported: 1)')
    for field in ('members', 'retired'):
        names = value.get(field)
        if (not isinstance(names, list) or any(not isinstance(n, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', n)
                                              or n.startswith('andino-') for n in names)
                or len(set(names)) != len(names)):
            raise ValueError(f'Invalid portfolio {field}: expected unique unprefixed slugs')
    if set(value['members']) & set(value['retired']):
        raise ValueError('Portfolio active and retired members overlap')
    actual = {p.parent.name for p in (bundle / 'skills').glob('*/SKILL.md')}
    if actual != set(value['members']):
        raise ValueError('Portfolio members differ from packaged entrypoints')
    for name in value['members']:
        body = (bundle / 'skills' / name / 'SKILL.md').read_text(encoding='utf-8-sig')
        if not re.search(rf'^name:\s*andino-{re.escape(name)}\s*$', body, re.M):
            raise ValueError(f'Portfolio member identity mismatch: {name}')
    resources = value.get('resources')
    if not isinstance(resources, list):
        raise ValueError('Invalid portfolio resources')
    for row in resources:
        resource = row.get('resource') if isinstance(row, dict) else None
        if (not isinstance(resource, str) or '\\' in resource or ':' in resource
                or any(p in {'', '.', '..', '.git'} for p in resource.split('/'))
                or not (bundle / resource).is_file()):
            raise ValueError(f'Invalid portfolio local resource: {resource}')
    return value


def _write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    with temporary.open('w', encoding='utf-8', newline='\n') as handle:
        json.dump(value, handle, sort_keys=True, indent=2)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _within(path, root):
    return path == root or root in path.parents


@contextmanager
def _lock(path):
    safe_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open('a+b')
    try:
        handle.seek(0)
        if os.name == 'nt':
            import msvcrt
            if path.stat().st_size == 0:
                handle.write(b'0')
                handle.flush()
            handle.seek(0)
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                raise ValueError('Another family setup holds the installation lock; retry after it completes') from exc
        else:
            import fcntl
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                raise ValueError('Another family setup holds the installation lock; retry after it completes') from exc
        yield
    finally:
        handle.close()  # OS releases the lock, including after process termination.


def _lock_paths(roots, state):
    paths = {state / 'family-state.lock'}
    for root in roots:
        key = hashlib.sha256(str(root.resolve()).casefold().encode()).hexdigest()[:20]
        paths.add(root.parent / f'.ai-rules-family-{key}.lock')
    return sorted(paths, key=str)


def _delete(path):
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink(missing_ok=True)


def _restore(journal):
    """Recover only when both installed and backup bytes still match the journal."""
    for row in reversed(journal['changes']):
        target, backup = Path(row['target']), Path(row['backup'])
        current = fingerprint(target)
        if current not in (None, row['before'], row['after']):
            raise ValueError(f'Recovery conflict; modified path is preserved: {target}')
        if exists(backup):
            if fingerprint(backup) != row['before']:
                raise ValueError(f'Recovery backup changed; preserved: {backup}')
            if exists(target):
                _delete(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(backup, target)
        elif row['before'] is None:
            if exists(target):
                _delete(target)
        elif current != row['before']:
            raise ValueError(f'Recovery backup missing; preserved: {target}')


def recover(state_dir):
    """Recover interrupted journals before a new applied setup (not during preview)."""
    directory = Path(state_dir).absolute() / 'families'
    if not directory.exists():
        return
    for path in sorted(directory.glob('*/journal.json')):
        journal = json.loads(path.read_text(encoding='utf-8'))
        if journal.get('status') != 'pending':
            continue
        roots = [Path(p) for p in journal['roots']]
        with ExitStack() as stack:
            for lock in _lock_paths(roots, Path(state_dir).absolute()):
                stack.enter_context(_lock(lock))
            _restore(journal)
            journal['status'] = 'rolled-back'
            _write(path, journal)


class FamilyPlan:
    def __init__(self, bundle, skill_root, state_dir, *, adapter=None, scope=None,
                 project_root=None, trusted=None, remove=False):
        self.bundle = Path(bundle) if bundle is not None else None
        self.root = Path(skill_root).absolute()
        self.state = Path(state_dir).absolute()
        self.adapter, self.scope, self.project = adapter, scope, project_root
        self.roots = tuple(dict.fromkeys(Path(p).absolute() for p in (
            adapter.skill_discovery_roots(scope, project_root) if adapter else (self.root,))))
        self.remove = remove
        self.trusted = trusted
        self.portfolio = manifest(self.bundle) if self.bundle else None
        for root in self.roots:
            safe_path(root)
            if _within(self.state.resolve(), root.resolve()):
                raise ValueError('Family journal/staging must be outside skill discovery roots')
        safe_path(self.state)
        key = hashlib.sha256(str(self.root.resolve()).casefold().encode()).hexdigest()
        self.inventory_path = self.state / 'family-inventories' / (key + '.json')
        self.inventory = json.loads(self.inventory_path.read_text(encoding='utf-8')) if self.inventory_path.exists() else {'artifacts': {}}
        if self.inventory.get('root', str(self.root)) != str(self.root):
            raise ValueError('Family inventory root differs; preserved')
        self.desired = {}
        self.kinds = {}
        self.ids = {}
        self._collect()
        self.before = {}
        self.after = {}
        self._preflight()

    def _artifact(self, path, source, identifier, kind='tree'):
        path = Path(path).absolute()
        self.desired[path] = source
        self.kinds[path], self.ids[path] = kind, identifier

    def _collect(self):
        old = self.inventory['artifacts']
        if self.remove:
            if not old:
                raise ValueError('Family ownership inventory is absent; legacy installation preserved. Run recognized setup before removal.')
            for name, row in old.items():
                self._artifact(Path(name), None, row['id'], row['kind'])
            return
        fingerprint(self.bundle)  # Includes links and hidden/unexpected files.
        self._artifact(self.root / FAMILY, self.bundle, FAMILY)
        for name in self.portfolio['members']:
            identifier = 'andino-' + name
            self._artifact(self.root / identifier, self.bundle / 'skills' / name, identifier)
        for name in self.portfolio['retired']:
            identifier = 'andino-' + name
            self._artifact(self.root / identifier, None, identifier)
        for path, row in old.items():
            if Path(path) not in self.desired and row['kind'] == 'tree':
                # Omission without explicit retirement is a package error, never deletion.
                raise ValueError(f'Previously owned member lacks explicit retirement: {row["id"]}')
        # Inspect aliases explicitly, never following a linked installed parent.
        identifiers = {FAMILY, *('andino-' + n for n in self.portfolio['members'] + self.portfolio['retired'])}
        for root in self.roots:
            if root.resolve() == self.root.resolve():
                continue
            for identifier in identifiers:
                path = root / identifier
                if exists(path):
                    if str(path) not in old:
                        raise ValueError(f'Discovery-root conflict is preserved: {path}')
                    self._artifact(path, None, identifier)
        if self.adapter:
            for identifier in sorted(identifiers):
                active = identifier == FAMILY or identifier.removeprefix('andino-') in self.portfolio['members']
                for path in invocation_paths(self.adapter, self.scope, identifier, self.project):
                    self._artifact(path, invocation_body(self.adapter, self.scope, identifier, self.project).encode('utf-8') if active else None,
                                   identifier, 'invocation')

    def _preflight(self):
        old = self.inventory['artifacts']
        for path, source in self.desired.items():
            current = fingerprint(path)
            row = old.get(str(path))
            if current is not None:
                if row is not None:
                    if _conflict(current, row['fingerprint']):
                        raise ValueError(f'Family artifact modified; preserved: {path}')
                elif not (self.trusted and self.trusted(path, self.ids[path], self.kinds[path])):
                    raise ValueError(f'Unowned family conflict is preserved: {path}')
            self.before[path] = current
            if source is None:
                desired = None
            elif isinstance(source, bytes):
                desired = {'kind': 'file', 'sha256': hashlib.sha256(source).hexdigest()}
            else:
                desired = fingerprint(source)
            self.after[path] = desired
        self.inventory_before = fingerprint(self.inventory_path)

    @property
    def changed(self):
        return any(self.before[p] != self.after[p] for p in self.desired) or not self.inventory_path.exists()

    def matches(self):
        try:
            return all(fingerprint(p) == value for p, value in self.after.items())
        except (ValueError, OSError):
            return False

    def apply(self, fault=None):
        with ExitStack() as stack:
            roots = (*self.roots, *(p.parent for p in self.desired if self.kinds[p] == 'invocation'))
            for path in _lock_paths(roots, self.state):
                stack.enter_context(_lock(path))
            pending = list((self.state / 'families').glob('*/journal.json'))
            if any(json.loads(p.read_text(encoding='utf-8')).get('status') == 'pending' for p in pending):
                raise ValueError('Unfinished family journal; run setup again to recover before planning')
            for path, expected in self.before.items():
                if fingerprint(path) != expected:
                    # A shared host may already have applied precisely this plan.
                    if self.matches():
                        return self.root / FAMILY
                    raise ValueError(f'Family artifact changed after planning; preserved: {path}')
            if fingerprint(self.inventory_path) != self.inventory_before:
                raise ValueError('Family ownership changed after planning; rerun setup')
            artifacts = {str(p): {'id': self.ids[p], 'kind': self.kinds[p], 'fingerprint': self.after[p]}
                         for p in self.desired if self.after[p] is not None}
            inventory = {'schema_version': 1, 'family': FAMILY, 'root': str(self.root), 'artifacts': artifacts}
            inventory_bytes = (json.dumps(inventory, sort_keys=True, indent=2)).encode('utf-8')
            if self.matches() and self.inventory_path.exists() and self.inventory_path.read_bytes() == inventory_bytes:
                return self.root / FAMILY
            work = self.state / 'families' / uuid.uuid4().hex
            work.mkdir(parents=True)
            changes = []
            sources = dict(self.desired)
            sources[self.inventory_path] = inventory_bytes
            for index, (target, source) in enumerate(sources.items()):
                before = fingerprint(target)
                after = self.after.get(target) if target != self.inventory_path else {'kind': 'file', 'sha256': hashlib.sha256(inventory_bytes).hexdigest()}
                if before == after:
                    continue
                stage, backup = work / f'stage-{index}', work / f'backup-{index}'
                if isinstance(source, bytes):
                    stage.write_bytes(source)
                elif source is not None:
                    shutil.copytree(source, stage)
                if source is not None and fingerprint(stage) != after:
                    raise ValueError('Staged family artifact differs from planned source')
                changes.append({'target': str(target), 'stage': str(stage), 'backup': str(backup), 'before': before, 'after': after})
            journal = {'schema_version': 1, 'status': 'pending', 'roots': [str(r) for r in roots], 'changes': changes}
            journal_path = work / 'journal.json'
            _write(journal_path, journal)  # Write ahead of *every* family mutation.
            try:
                for index, row in enumerate(changes):
                    target, backup, stage = Path(row['target']), Path(row['backup']), Path(row['stage'])
                    if fingerprint(target) != row['before']:
                        raise ValueError(f'Family changed during transaction; preserved: {target}')
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if exists(target):
                        os.replace(target, backup)
                    if row['after'] is not None:
                        os.replace(stage, target)
                    if fingerprint(target) != row['after']:
                        raise ValueError('Family verification failed')
                    if fault:
                        fault(index, target)
                if not self.matches():
                    raise ValueError('Family post-transaction verification failed')
                journal['status'] = 'committed'
                _write(journal_path, journal)
            except BaseException:
                _restore(journal)
                journal['status'] = 'rolled-back'
                _write(journal_path, journal)
                raise
            return self.root / FAMILY


def install(bundle, skill_root, state_dir=None, **kwargs):
    state = Path(state_dir) if state_dir else Path(skill_root).parent / '.ai-rules-family-state'
    return FamilyPlan(bundle, skill_root, state, **kwargs).apply()


def remove(skill_root, state_dir, **kwargs):
    return FamilyPlan(None, skill_root, state_dir, remove=True, **kwargs).apply()
