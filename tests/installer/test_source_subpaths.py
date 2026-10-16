import subprocess
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from ai_rules.catalog import load_catalog
from ai_rules.domain.errors import ValidationError
from ai_rules.release.bundles import export_git_ref
from ai_rules.release.latest import LatestSources, contents
from ai_rules.resolver.engine import Resolver, ResolveRequest
from ai_rules.profiles import load_profiles


class SourceSubpathTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.remote = self.root / 'remote'
        self.remote.mkdir()
        self.git('init', '-b', 'family')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        for name in ('focus', 'search-first'):
            package = self.remote / 'skills' / name
            package.mkdir(parents=True)
            (package / 'SKILL.md').write_text(
                f'---\nname: {name}\ndescription: Fixture\n---\n', encoding='utf-8')
            (package / 'references').mkdir()
            (package / 'references/data.bin').write_bytes(b'\x00\xff\x01')
        (self.remote / 'SKILL.md').write_text('family root', encoding='utf-8')
        self.commit('initial')
        self.catalog = load_catalog()
        for name in ('focus', 'search-first'):
            self.catalog.require_capability(name).source.update(
                repository=str(self.remote), branch='family', subpath=f'skills/{name}')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.remote), *args],
                                       text=True, encoding='utf-8', stderr=subprocess.PIPE).strip()

    def commit(self, message):
        self.git('add', '.')
        self.git('commit', '-m', message)
        return self.git('rev-parse', 'HEAD')

    def sources(self, names=('focus', 'search-first')):
        result = LatestSources(self.catalog, names)
        self.addCleanup(result.close)
        return result

    def test_shared_branch_exports_independent_roots_and_binary_resources(self):
        from ai_rules.release.latest import git
        with patch('ai_rules.release.latest.git', wraps=git) as commands:
            sources = self.sources()
        fetches = [call for call in commands.call_args_list if call.args[1] == 'fetch']
        self.assertEqual(1, len(fetches))
        for name, root in sources.sources.items():
            self.assertIn(f'name: {name}', (root / 'SKILL.md').read_text())
            self.assertEqual(b'\x00\xff\x01', (root / 'references/data.bin').read_bytes())
            self.assertFalse((root / 'skills').exists())
            self.assertEqual(sources.tree(*[sources.entries[name][i] for i in (0, 3)],
                                          subpath=f'skills/{name}'), contents(root))

    def test_historical_revision_matching_uses_selected_package(self):
        sources = self.sources(('focus',))
        original = contents(sources.sources['focus'])
        old = self.git('rev-parse', 'HEAD')
        (self.remote / 'skills/focus/new.txt').write_text('new', encoding='utf-8')
        self.commit('new focus')
        updated = self.sources(('focus',))
        self.assertEqual(old, updated.known_revision('focus', original))

    def test_archive_subpath_preserves_binary_bytes_and_root_layout(self):
        target = self.root / 'export'
        export_git_ref('HEAD', target, self.remote, subpath='skills/focus')
        self.assertTrue((target / 'SKILL.md').is_file())
        self.assertEqual(b'\x00\xff\x01', (target / 'references/data.bin').read_bytes())
        self.assertFalse((target / 'skills').exists())

    def test_archive_preserves_git_blobs_under_windows_autocrlf(self):
        script = self.remote / 'skills/focus/references/runtime.js'
        script.write_bytes(b'export const fixture = 1;\n')
        self.git('-c', 'core.autocrlf=false', 'add', '.')
        self.git('commit', '-m', 'code resource')
        self.git('config', 'core.autocrlf', 'true')
        target = self.root / 'windows-export'
        export_git_ref('HEAD', target, self.remote, subpath='skills/focus')
        self.assertEqual(b'export const fixture = 1;\n', (target / 'references/runtime.js').read_bytes())

    def test_release_staging_exports_each_package_and_records_source_subpaths(self):
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
        from build_release import stage_bundles
        commit = self.git('rev-parse', 'HEAD')
        targets = {name: {'branch': 'family', 'commit': commit, 'subpath': f'skills/{name}'}
                   for name in ('focus', 'search-first')}
        stage = self.root / 'stage'
        evidence = stage_bundles(targets, stage, self.remote)
        self.assertEqual(targets, evidence)
        self.assertEqual(b'\x00\xff\x01', (stage / 'focus/references/data.bin').read_bytes())
        self.assertIn('name: search-first', (stage / 'search-first/SKILL.md').read_text())
        with self.assertRaises(FileExistsError):
            stage_bundles(targets, stage, self.remote)

    def test_unsafe_subpaths_fail_before_export(self):
        for value in ('../focus', '/skills/focus', 'C:/skills', 'skills\\focus',
                      'skills/../focus', 'skills//focus', './skills', '', '.git',
                      'skills/.git/x', 'skills/.GIT/x', 'skills/focus.', 'skills/CON', 'skills/focus '):
            with self.subTest(value=value):
                self.catalog.require_capability('focus').source['subpath'] = value
                with self.assertRaises((ValueError, ValidationError)):
                    self.sources(('focus',))

    def test_subpath_cannot_select_a_file_or_mismatched_identity(self):
        for value in ('SKILL.md', 'skills/search-first', 'missing'):
            with self.subTest(value=value):
                self.catalog.require_capability('focus').source['subpath'] = value
                with self.assertRaises((ValueError, ValidationError)):
                    self.sources(('focus',))

    def test_nested_git_symlink_is_rejected(self):
        blob = self.git('hash-object', '-w', '--stdin')
        self.git('update-index', '--add', '--cacheinfo', f'120000,{blob},skills/focus/link')
        self.git('commit', '-m', 'unsafe link')
        with self.assertRaises((ValueError, ValidationError)):
            self.sources(('focus',))
        with self.assertRaises((ValueError, ValidationError)):
            export_git_ref('HEAD', self.root / 'bad-export', self.remote, subpath='skills/focus')

    def test_release_manifest_cannot_write_capability_outside_staging_root(self):
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
        from build_release import stage_bundles
        with self.assertRaises((ValueError, ValidationError)):
            stage_bundles({'../escape': {'commit': self.git('rev-parse', 'HEAD'),
                                        'subpath': 'skills/focus'}}, self.root / 'stage', self.remote)
        self.assertFalse((self.root / 'escape').exists())


class TransitiveDependencyTests(unittest.TestCase):
    def test_selection_installs_transitive_dependencies_first_once(self):
        catalog = load_catalog()
        catalog.capabilities['council'] = replace(catalog.require_capability('council'),
                                                  requires=('andino-workflow',))
        resolver = Resolver(catalog, load_profiles(catalog), None)
        self.assertEqual(('focus', 'search-first', 'andino-workflow', 'council'),
                         resolver._expand_selection(ResolveRequest(hosts=('codex',),
                                                                  capabilities=('council',))))

    def test_dependency_cycle_is_reported_instead_of_partial_installation(self):
        catalog = load_catalog()
        catalog.capabilities['focus'] = replace(catalog.require_capability('focus'),
                                                requires=('andino-workflow',))
        resolver = Resolver(catalog, load_profiles(catalog), None)
        with self.assertRaises(ValidationError):
            resolver._expand_selection(ResolveRequest(hosts=('codex',), capabilities=('andino-workflow',)))
