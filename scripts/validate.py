"""Local artifact checks and isolated adapter behavior tests; no model/API calls."""
from pathlib import Path
import importlib.util, json, re, tempfile, tomllib, unittest, shutil
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / filename)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result

sync = module('andino_sync', 'sync-workflow.py')
mcp = module('andino_mcp', 'mcp-toggle.py')
harden = module('andino_harden', 'harden-runtime.py')

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
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Adapters)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
