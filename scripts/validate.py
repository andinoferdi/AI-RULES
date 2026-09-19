"""Local artifact checks and isolated adapter behavior tests; no model/API calls."""
from pathlib import Path
import importlib.util, json, re, tempfile, tomllib, unittest, shutil, subprocess, sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PLAN_STATUSES = {'TODO', 'IN_PROGRESS', 'BLOCKED', 'DONE', 'SKIPPED'}
PLAN_DEPTHS = {'LITE', 'STANDARD', 'DEEP'}

def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / filename)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result

sync = module('andino_sync', 'sync-workflow.py')
managed = module('managed_sync', 'sync-skills.py')
mcp = module('andino_mcp', 'mcp-toggle.py')
harden = module('andino_harden', 'harden-runtime.py')

def section(text, heading):
    match = re.search(rf'(?ms)^## {re.escape(heading)}\s*$\n(.*?)(?=^#{1,2} |\Z)', text)
    return match.group(1).strip() if match else ''

def validate_plan(path):
    text = path.read_text(encoding='utf-8-sig')
    errors = []
    header = lambda name: re.search(rf'(?m)^{re.escape(name)}:\s*(.+)$', text)
    status_match, depth_match, current_match = header('Status'), header('Plan Depth'), header('Current Phase')
    status = status_match.group(1).strip() if status_match else ''
    depth = depth_match.group(1).strip() if depth_match else ''
    current = current_match.group(1).strip() if current_match else ''
    if status not in PLAN_STATUSES: errors.append(f'invalid Status: {status or "missing"}')
    if depth not in PLAN_DEPTHS: errors.append(f'invalid Plan Depth: {depth or "missing"}')
    required = ['Objective', 'Acceptance Criteria', 'Execution Board', 'NEXT ACTION']
    if depth in {'STANDARD', 'DEEP'}: required.insert(0, 'Executive Snapshot')
    for name in required:
        if not section(text, name): errors.append(f'missing or empty section: {name}')
    board = section(text, 'Execution Board')
    rows = re.findall(r'(?m)^\|\s*(Phase\s+\d+\s+[—-]\s+[^|]+?)\s*\|\s*([A-Z_]+)\s*\|', board)
    board_status = {name.strip(): value for name, value in rows}
    for name, value in board_status.items():
        if value not in PLAN_STATUSES: errors.append(f'invalid phase status: {name}={value}')
    if current and current not in board_status: errors.append('Current Phase is absent from Execution Board')
    in_progress = sum(value == 'IN_PROGRESS' for value in board_status.values())
    if status == 'IN_PROGRESS' and in_progress != 1:
        errors.append(f'active plan must have exactly one IN_PROGRESS phase, found {in_progress}')
    if status == 'TODO' and in_progress > 1:
        errors.append(f'TODO plan may have at most one IN_PROGRESS phase, found {in_progress}')
    details = re.findall(r'(?ms)^## (Phase\s+\d+\s+[—-]\s+[^\n]+)\n\nStatus:\s*([A-Z_]+)(.*?)(?=^## Phase\s+\d+\s+[—-]|^## [^P]|\Z)', text)
    for name, value, body in details:
        name = name.strip()
        if name in board_status and board_status[name] != value:
            errors.append(f'board/detail mismatch: {name}')
        if value == 'DONE' and not re.search(r'(?m)^### Result / Evidence\s*$', body):
            errors.append(f'DONE phase lacks Result / Evidence: {name}')
        if value == 'BLOCKED' and not re.search(r'(?i)blocker', body):
            errors.append(f'BLOCKED phase lacks blocker: {name}')
    next_action = section(text, 'NEXT ACTION')
    if status != 'DONE' and (not next_action or re.fullmatch(r'(?i)(pending|tbd|none)[.!]?', next_action)):
        errors.append('active plan lacks concrete NEXT ACTION')
    if status == 'DONE' and any(value in {'TODO', 'IN_PROGRESS', 'BLOCKED'} for value in board_status.values()):
        errors.append('completed plan contains pending phase')
    placeholders = re.findall(r'\[(?:TICKET|TITLE|name|goal|scope|path|Observable[^]]*)\]', text, re.I)
    if placeholders: errors.append('mature plan contains template placeholders')
    if errors: raise ValueError(f'{path.name}: ' + '; '.join(errors))
    return {'depth': depth, 'phases': board_status, 'lines': len(text.splitlines())}

class Adapters(unittest.TestCase):
    def test_installs_resolve_references_without_source(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory); source = base / 'editable-source'; home = base / 'home'
            shutil.copytree(sync.SOURCE, source)
            previous = sync.SOURCE
            try:
                sync.SOURCE = source
                sync.sync(home)
                source.rename(base / 'source-unavailable')
                for relative in sync.DESTINATIONS:
                    installed = home / relative
                    for path in installed.rglob('*.md'):
                        for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                            if ':' not in link:
                                self.assertTrue((path.parent / link).is_file(), (path, link))
            finally:
                sync.SOURCE = previous

    def test_hardening_preserves_mcp_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            sync.sync(home)
            for host, (rules, installed, workers) in harden.HOSTS.items():
                path = home / rules; path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('Keep project constraints.\nUI coexistence reference: C:/old/Downloads/AI-RULES/policy.md\n')
                for name in harden.CORE:
                    skill = home / workers / name / 'SKILL.md'
                    skill.parent.mkdir(parents=True, exist_ok=True)
                    skill.write_text(f'---\nname: {name}\ndescription: Test method\n---\n\nPreserve worker body.\n')
            path = home / '.config/opencode/opencode.json'
            original = {'mcp': {'context7': {'enabled': True, 'url': 'fixture'}}, 'model': 'unchanged'}
            path.write_text(json.dumps(original))
            harden.harden(home)
            changed = json.loads(path.read_text())
            self.assertEqual(changed['mcp'], original['mcp'])
            self.assertEqual(changed['model'], original['model'])
            self.assertEqual(harden.harden(home), [])
            for host, (rules, installed, workers) in harden.HOSTS.items():
                self.assertNotIn('Downloads/AI-RULES', (home / rules).read_text())
                self.assertTrue((home / installed / 'references/ui-coexistence.md').is_file())
                for name in harden.CORE:
                    self.assertIn('Preserve worker body.', (home / workers / name / 'SKILL.md').read_text())

    def test_sync_is_identical_idempotent_and_rejects_local_edits(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            sync.sync(home); sync.sync(home, check=True)
            paths = [home / p for p in sync.DESTINATIONS]
            mtimes = [p.stat().st_mtime_ns for p in paths]
            sync.sync(home)
            self.assertEqual(mtimes, [p.stat().st_mtime_ns for p in paths])
            modified = paths[0] / 'SKILL.md'
            modified.write_text(modified.read_text() + '\nLocal user edit\n')
            with self.assertRaisesRegex(RuntimeError, 'locally edited'):
                sync.sync(home)
            self.assertIn('Local user edit', modified.read_text())

    def test_codex_toggle_preserves_nested_environment_and_unrelated_tables(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory); path = home / '.codex/config.toml'
            path.parent.mkdir()
            path.write_text('model = "unchanged"\n[mcp_servers."example-server"]\ncommand = "local"\n[mcp_servers."example-server".env]\nAPI_KEY = "synthetic-fixture-only"\n[features]\nhooks = true\n')
            before = tomllib.loads(path.read_text())
            mcp.toggle(home, 'codex', 'example-server', False)
            after = tomllib.loads(path.read_text())
            self.assertFalse(after['mcp_servers']['example-server'].pop('enabled'))
            self.assertEqual(before, after)
            mcp.toggle(home, 'codex', 'example-server', True)
            self.assertTrue(tomllib.loads(path.read_text())['mcp_servers']['example-server']['enabled'])

    def test_claude_manual_roundtrip_is_lossless(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory); path = home / '.claude.json'
            original = {'unrelated': {'preserve': True}, 'mcpServers': {'example': {'command': 'local', 'env': {'KEY': 'synthetic-fixture-only'}}}}
            path.write_text(json.dumps(original))
            mcp.toggle(home, 'claude', 'example', False)
            self.assertEqual(json.loads(path.read_text())['mcpServers'], {})
            mcp.toggle(home, 'claude', 'example', True)
            self.assertEqual(json.loads(path.read_text()), original)

    def test_json_hosts_preserve_server_options(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            for host in ['opencode', 'antigravity']:
                path = home / mcp.FILES[host]; path.parent.mkdir(parents=True, exist_ok=True)
                key = 'mcp' if host == 'opencode' else 'mcpServers'
                path.write_text(json.dumps({key: {'sample': {'command': ['local'], 'env': {'KEY': 'synthetic-fixture-only'}}}, 'unrelated': 42}))
                mcp.toggle(home, host, 'sample', False)
                mcp.toggle(home, host, 'sample', True)
                data = json.loads(path.read_text())
                self.assertEqual(data['unrelated'], 42)
                self.assertEqual(data[key]['sample']['env'], {'KEY': 'synthetic-fixture-only'})
                with self.assertRaises(ValueError):
                    mcp.toggle(home, host, 'not-configured', True)

    def test_unmanaged_workflow_install_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory); destination = home / sync.DESTINATIONS[0]
            destination.mkdir(parents=True); (destination / 'SKILL.md').write_text('user-owned')
            with self.assertRaisesRegex(RuntimeError, 'Unmanaged'):
                sync.sync(home)
            self.assertEqual((destination / 'SKILL.md').read_text(), 'user-owned')

class ManagedSkills(unittest.TestCase):
    def test_legacy_marker_update_and_backup_with_source_override(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory); home = base / 'home'; source = base / 'editable-source'
            shutil.copytree(sync.SOURCE, source)
            original = managed.hashes(source)
            # Existing on-disk format, without using the new implementation to install it.
            for relative in sync.DESTINATIONS:
                target = home / relative
                shutil.copytree(source, target)
                (target / '.andino-generated.json').write_text(json.dumps({
                    'source': 'previous-location/andino-workflow', 'files': original}))
            (source / 'SKILL.md').write_text((source / 'SKILL.md').read_text() + '\nNew canonical content\n')
            previous = sync.SOURCE
            try:
                sync.SOURCE = source
                with self.assertRaisesRegex(RuntimeError, 'Drift'):
                    sync.sync(home, check=True)
                sync.sync(home); sync.sync(home, check=True)
            finally:
                sync.SOURCE = previous
            backups = list((home / '.andino/backups/sync').glob('previous-*/andino-workflow'))
            self.assertEqual(len(backups), 4)
            for backup in backups:
                self.assertEqual(managed.hashes(backup), original)
            self.assertFalse(list(home.rglob('ai-codebase-rescue')))

    def test_complete_trees_metadata_links_and_idempotence(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            managed.sync(home)
            before = {p.relative_to(home): (p.read_bytes(), p.stat().st_mtime_ns)
                      for p in home.rglob('*') if p.is_file()}
            managed.sync(home, check=True)
            managed.sync(home)
            self.assertEqual(before, {p.relative_to(home): (p.read_bytes(), p.stat().st_mtime_ns)
                                     for p in home.rglob('*') if p.is_file()})
            for name in managed.MANAGED_SKILLS:
                source = ROOT / 'skills' / name
                for root in managed.HOST_ROOTS:
                    target = home / root / name
                    self.assertEqual(managed.hashes(target), managed.hashes(source))
                    marker = json.loads((target / '.andino-generated.json').read_text())
                    self.assertEqual(marker, {'source': str(source), 'files': managed.hashes(source)})
                    for path in target.rglob('*.md'):
                        for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                            if ':' not in link:
                                self.assertTrue((path.parent / link).is_file(), (path, link))

    def test_source_drift_update_backup_and_skill_isolation(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory); home = base / 'home'; sources = base / 'sources'
            for name in managed.MANAGED_SKILLS:
                shutil.copytree(ROOT / 'skills' / name, sources / name)
            managed.sync(home, source_root=sources)
            andino_before = {p: p.read_bytes() for root in managed.HOST_ROOTS
                             for p in (home / root / 'andino-workflow').rglob('*') if p.is_file()}
            source = sources / 'ai-codebase-rescue'
            previous = managed.hashes(source)
            (source / 'SKILL.md').write_text((source / 'SKILL.md').read_text() + '\nFixture change\n')
            with self.assertRaisesRegex(RuntimeError, 'Drift'):
                managed.sync(home, check=True, source_root=sources)
            self.assertFalse((home / '.andino/backups').exists())
            managed.sync(home, skills=('ai-codebase-rescue',), source_root=sources)
            managed.sync(home, check=True, source_root=sources)
            self.assertEqual(andino_before, {p: p.read_bytes() for p in andino_before})
            backups = list((home / '.andino/backups/sync').glob('previous-*/ai-codebase-rescue'))
            self.assertEqual(len(backups), 4)
            for backup in backups:
                self.assertTrue(backup.resolve().is_relative_to(home.resolve()))
                self.assertEqual(managed.hashes(backup), previous)

    def test_refuses_unmanaged_and_local_drift_for_each_skill(self):
        for name in managed.MANAGED_SKILLS:
            for local in (False, True):
                with self.subTest(name=name, local=local), tempfile.TemporaryDirectory() as directory:
                    home = Path(directory); target = home / managed.HOST_ROOTS[0] / name
                    if local:
                        managed.sync(home, skills=(name,))
                    else:
                        target.mkdir(parents=True)
                    file = target / 'SKILL.md'; file.write_text('Preserve local contents')
                    with self.assertRaisesRegex(RuntimeError, 'Unmanaged or locally edited'):
                        managed.sync(home, skills=(name,))
                    self.assertEqual(file.read_text(), 'Preserve local contents')
                    self.assertFalse((home / '.andino/backups').exists())

    def test_identical_unmanaged_tree_is_not_adopted_or_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            for root in managed.HOST_ROOTS:
                shutil.copytree(sync.SOURCE, home / root / 'andino-workflow')
            sync.sync(home, check=True); sync.sync(home)
            self.assertFalse(list(home.rglob('.andino-generated.json')))
            self.assertFalse((home / '.andino').exists())

    def test_explicit_selection_and_missing_source_do_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / 'home'
            for skills in ((), ('experimental',), ('../escape',)):
                with self.assertRaises(ValueError):
                    managed.sync(home, skills=skills)
            with self.assertRaisesRegex(RuntimeError, 'Missing canonical'):
                managed.sync(home, source_root=Path(directory) / 'absent')
            self.assertFalse(home.exists())

    def test_legacy_cli_and_generic_cli_check_exit_and_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / 'home'
            def run(script, *args):
                return subprocess.run([sys.executable, '-B', str(ROOT / 'scripts' / script),
                                       '--home', str(home), *args], capture_output=True, text=True)
            self.assertNotEqual(run('sync-workflow.py', '--check').returncode, 0)
            self.assertFalse(home.exists())
            self.assertEqual(run('sync-workflow.py').returncode, 0)
            self.assertEqual(run('sync-workflow.py', '--check').returncode, 0)
            self.assertFalse(list(home.rglob('ai-codebase-rescue')))
            self.assertNotEqual(run('sync-skills.py', '--check').returncode, 0)
            self.assertEqual(run('sync-skills.py', '--skill', 'ai-codebase-rescue').returncode, 0)
            self.assertEqual(run('sync-skills.py', '--check').returncode, 0)
            file = home / managed.HOST_ROOTS[0] / 'andino-workflow/SKILL.md'
            file.write_text('Local edit')
            self.assertNotEqual(run('sync-workflow.py').returncode, 0)
            self.assertNotEqual(run('sync-workflow.py', '--check').returncode, 0)
            self.assertEqual(file.read_text(), 'Local edit')

class AdaptivePlans(unittest.TestCase):
    FIXTURES = ROOT / 'tests/fixtures/exec-plans'

    def test_standard_login_fixture_is_valid_and_bounded(self):
        result = validate_plan(self.FIXTURES / 'login-standard.md')
        self.assertEqual(result['depth'], 'STANDARD')
        self.assertLess(result['lines'], 250)

    def test_deep_resume_fixture_covers_handoff_contract(self):
        path = self.FIXTURES / 'remaster-deep-resume.md'
        result = validate_plan(path)
        text = path.read_text(encoding='utf-8')
        self.assertEqual(result['depth'], 'DEEP')
        self.assertEqual(list(result['phases'].values()), ['DONE', 'DONE', 'TODO'])
        for marker in ['Baseline / Starting Evidence', 'Architecture / Approach',
                       'Technical Contract', 'Plan Revisions', 'Verification Matrix',
                       'APPROVAL GATE', 'Handoff Notes', 'Do not repeat:', 'First inspect:']:
            self.assertIn(marker, text)

    def test_validator_rejects_board_detail_drift(self):
        original = (self.FIXTURES / 'remaster-deep-resume.md').read_text(encoding='utf-8')
        broken = original.replace('## Phase 2 — Shared weather contract\n\nStatus: DONE',
                                  '## Phase 2 — Shared weather contract\n\nStatus: BLOCKED')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'broken.md'; path.write_text(broken, encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'board/detail mismatch'):
                validate_plan(path)

def check_links():
    errors = []
    for path in ROOT.rglob('*.md'):
        # The archived personal collection contains literal example prompts, not repo links.
        if 'personal-prompt-library.md' == path.name:
            continue
        text = re.sub(r'(?ms)^(`{3,}|~{3,}).*?^\1[^\n]*$', '', path.read_text(encoding='utf-8-sig'))
        for raw in re.findall(r'\]\((<[^>]+>|[^)]+)\)', text):
            target = raw.strip('<>').split('#')[0]
            if not target or re.match(r'[a-z]+:', target) or '[' in target:
                continue
            target = unquote(target)
            if not (path.parent / target).exists():
                errors.append(f'{path.relative_to(ROOT)} -> {target}')
    if errors:
        raise RuntimeError('Broken links:\n' + '\n'.join(errors))
    print('Markdown file links: PASS')

if __name__ == '__main__':
    check_links()
    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Adapters))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ManagedSkills))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(AdaptivePlans))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
