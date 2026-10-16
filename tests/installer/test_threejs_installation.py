import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ai_rules import cli
from ai_rules.catalog import load_catalog
from ai_rules.profiles import load_profiles
from ai_rules.execution import copy_tree_atomic
from ai_rules.release.latest import contents


class ThreejsInstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.remote = self.root / 'remote'
        self.remote.mkdir()
        self.git('init', '-b', 'andino-workflow')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.commits = {}
        for name in ('andino-workflow', 'focus', 'search-first'):
            if name != 'andino-workflow':
                self.git('checkout', '-b', name)
            self.write_skill(self.remote, name)
            self.commits[name] = self.commit(name)
        self.git('checkout', '-b', 'threejs-skills')
        self.catalog = load_catalog()
        self.names = []
        for capability in self.catalog.capabilities.values():
            capability.source['repository'] = str(self.remote)
            if capability.source['branch'] == 'threejs-skills':
                self.names.append(capability.id)
                folder = self.remote / capability.source['subpath']
                self.write_skill(folder, capability.id)
                (folder / 'assets').mkdir()
                (folder / 'assets/field.bin').write_bytes(b'\x00\xff\x00\x01')
                (folder / 'scripts').mkdir()
                (folder / 'scripts/probe_asset_credentials.sh').write_text('printf SET\n', encoding='utf-8')
        self.head = self.commit('family')
        self.project = self.root / 'project'
        self.home = self.root / 'home'
        self.state = self.root / 'state'
        self.patch = patch.object(cli, 'load_catalog', return_value=self.catalog)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.home_patch = patch.object(Path, 'home', return_value=self.home)
        self.home_patch.start()
        self.addCleanup(self.home_patch.stop)
        self.manifest = {'release_sequence': 12, 'first_party': {
            name: {'branch': capability.source['branch'],
                   'commit': self.head if name in self.names else self.commits.get(name, self.head),
                   **({'subpath': capability.source['subpath']} if 'subpath' in capability.source else {})}
            for name, capability in self.catalog.capabilities.items()}}

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.remote), *args],
                                       text=True, encoding='utf-8', stderr=subprocess.PIPE).strip()

    def commit(self, message):
        self.git('add', '.')
        self.git('commit', '-m', message)
        return self.git('rev-parse', 'HEAD')

    def write_skill(self, folder, name):
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Fixture\n---\nMethod\n', encoding='utf-8')
        (folder / 'README.md').write_text('Fixture\n', encoding='utf-8')

    def run_cli(self, command='setup', source='latest', scope='project', selections=('--profile', 'threejs')):
        output = io.StringIO()
        def local_export(ref, destination, repo_root=None, subpath=None):
            from ai_rules.release.bundles import export_git_ref
            return export_git_ref(ref, destination, self.remote, subpath=subpath)
        with patch.object(cli, '_release_manifest', return_value=self.manifest), \
             patch('ai_rules.capabilities.adapters._load_release_manifest', return_value=self.manifest), \
             patch.object(cli, 'packaged_bundle', return_value=None), \
             patch.object(cli, 'export_git_ref', side_effect=local_export), \
             contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = cli.main([command, '--host', 'codex', '--scope', scope,
                '--project-root', str(self.project), '--state-dir', str(self.state),
                '--source', source, '--yes', '--non-interactive', *selections])
        return result, output.getvalue()

    def target(self, name, scope='project'):
        return (self.project if scope == 'project' else self.home) / '.agents/skills' / name

    def test_profile_latest_installs_all_packages_without_nested_discovery_and_is_noop(self):
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.assertEqual(49, len(list((self.project / '.agents/skills').iterdir())))
        for name in self.names:
            self.assertTrue((self.target(name) / 'SKILL.md').is_file())
            self.assertEqual(b'\x00\xff\x00\x01', (self.target(name) / 'assets/field.bin').read_bytes())
            self.assertFalse((self.target(name) / 'skills').exists())
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        lock = json.loads((self.state / 'lock.json').read_text())
        self.assertTrue(all(t['action'] == 'NO_OP' for t in lock['targets']))
        records = json.loads((self.state / 'managed-installations.json').read_text())['installations']
        self.assertEqual('skills/threejs-shaders', records['threejs-shaders:codex:project']['source']['subpath'])

    def test_single_and_multiple_selection_leave_other_skills_untouched(self):
        for names in (('threejs-shaders',), ('threejs-shaders', 'threejs-lighting')):
            selection = tuple(x for name in names for x in ('--capability', name))
            result, output = self.run_cli(selections=selection)
            self.assertEqual(0, result, output)
        self.assertEqual({'threejs-shaders', 'threejs-lighting'},
                         {p.name for p in (self.project / '.agents/skills').iterdir()})

    def test_bundled_profile_project_and_global_scopes(self):
        for scope in ('project', 'global'):
            result, output = self.run_cli(source='bundled', scope=scope)
            self.assertEqual(0, result, output)
            for name in self.names:
                self.assertTrue((self.target(name, scope) / 'SKILL.md').is_file())
            result, output = self.run_cli(source='bundled', scope=scope)
            self.assertEqual(0, result, output)
            self.assertNotIn('APPLIED INSTALL', output)

    def test_update_backups_changed_member_and_preserves_unselected_files(self):
        selection = ('--capability', 'threejs-shaders')
        self.assertEqual(0, self.run_cli(selections=selection)[0])
        (self.remote / 'skills/threejs-shaders/new.txt').write_text('revision two', encoding='utf-8')
        self.commit('update shaders')
        result, output = self.run_cli('update', selections=selection)
        self.assertEqual(0, result, output)
        self.assertEqual('revision two', (self.target('threejs-shaders') / 'new.txt').read_text())
        self.assertTrue(list((self.state / 'backups').glob('*/threejs-shaders/SKILL.md')))
        self.assertFalse(self.target('threejs-lighting').exists())

    def test_latest_preserves_modified_managed_and_unmanaged_conflicts(self):
        selection = ('--capability', 'threejs-shaders')
        self.assertEqual(0, self.run_cli(selections=selection)[0])
        personal = self.target('threejs-shaders') / 'personal.txt'
        personal.write_text('mine', encoding='utf-8')
        result, output = self.run_cli('update', selections=selection)
        self.assertNotEqual(0, result, output)
        self.assertEqual('mine', personal.read_text())

        result, output = self.run_cli('remove', source='bundled', selections=selection)
        self.assertNotEqual(0, result, output)
        self.assertEqual('mine', personal.read_text())
        target = self.target('threejs-lighting')
        self.write_skill(target, 'personal-lighting')
        before = contents(target)
        result, output = self.run_cli(selections=('--capability', 'threejs-lighting'))
        self.assertNotEqual(0, result, output)
        self.assertEqual(before, contents(target))

    def test_atomic_replacement_rolls_back_failed_binary_verification(self):
        source, target = self.root / 'source', self.root / 'target'
        self.write_skill(source, 'threejs-shaders')
        self.write_skill(target, 'threejs-shaders')
        (target / 'personal.bin').write_bytes(b'\xff\x00')
        before = contents(target)
        with self.assertRaisesRegex(RuntimeError, 'rolled back'):
            copy_tree_atomic(source, target, self.root / 'backups',
                             verify=lambda path: path != target)
        self.assertEqual(before, contents(target))
        self.assertTrue(list((self.root / 'backups').glob('*/target/personal.bin')))

    def test_doctor_repair_remove_and_global_latest_keep_selected_identity(self):
        selection = ('--capability', 'threejs-shaders')
        self.assertEqual(0, self.run_cli(scope='global', selections=selection)[0])
        self.assertTrue((self.target('threejs-shaders', 'global') / 'SKILL.md').is_file())
        self.assertEqual(0, self.run_cli(source='bundled', selections=selection)[0])
        result, output = self.run_cli('doctor', source='bundled', selections=selection)
        self.assertEqual(0, result, output)
        (self.target('threejs-shaders') / 'SKILL.md').unlink()
        result, output = self.run_cli('doctor', source='bundled', selections=(*selection, '--repair'))
        self.assertEqual(0, result, output)
        self.assertTrue((self.target('threejs-shaders') / 'SKILL.md').is_file())
        result, output = self.run_cli('remove', source='bundled', selections=selection)
        self.assertEqual(0, result, output)
        self.assertFalse(self.target('threejs-shaders').exists())
        self.assertTrue(self.target('threejs-shaders', 'global').exists())

    def test_bundled_update_and_remove_preserve_user_modified_files(self):
        selection = ('--capability', 'threejs-shaders')
        self.assertEqual(0, self.run_cli(source='bundled', selections=selection)[0])
        personal = self.target('threejs-shaders') / 'personal.txt'
        personal.write_text('mine', encoding='utf-8')
        (self.remote / 'skills/threejs-shaders/new.txt').write_text('update', encoding='utf-8')
        self.manifest['first_party']['threejs-shaders']['commit'] = self.commit('bundle update')
        result, output = self.run_cli('update', source='bundled', selections=selection)
        self.assertNotEqual(0, result, output)
        self.assertEqual('mine', personal.read_text())

        result, output = self.run_cli('remove', source='bundled', selections=selection)
        self.assertNotEqual(0, result, output)
        self.assertEqual('mine', personal.read_text())

    def test_legacy_bundled_record_without_fingerprints_requires_explicit_review(self):
        selection = ('--capability', 'threejs-shaders')
        self.assertEqual(0, self.run_cli(source='bundled', selections=selection)[0])
        record_path = self.state / 'managed-installations.json'
        records = json.loads(record_path.read_text())
        del records['installations']['threejs-shaders:codex:project']['files']
        record_path.write_text(json.dumps(records), encoding='utf-8')
        personal = self.target('threejs-shaders') / 'personal.txt'
        personal.write_text('legacy personal edit', encoding='utf-8')
        (self.remote / 'skills/threejs-shaders/new.txt').write_text('new release', encoding='utf-8')
        self.manifest['first_party']['threejs-shaders']['commit'] = self.commit('legacy upgrade')
        result, output = self.run_cli('update', source='bundled', selections=selection)
        self.assertNotEqual(0, result, output)
        self.assertEqual('legacy personal edit', personal.read_text())
        result, output = self.run_cli('remove', source='bundled', selections=selection)
        self.assertNotEqual(0, result, output)
        self.assertEqual('legacy personal edit', personal.read_text())
