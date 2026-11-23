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
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        # The fixture is clone-shaped: bundled installs read its skills/ folder.
        marker = self.remote / 'src/ai_rules/catalog/data/capabilities.json'
        marker.parent.mkdir(parents=True)
        marker.write_text('{}\n', encoding='utf-8')
        for name in ('andino-workflow', 'focus', 'search-first'):
            self.write_skill(self.remote / 'skills' / name, name)
        self.catalog = load_catalog()
        self.names = ['threejs-skills']
        for capability in self.catalog.capabilities.values():
            capability.source['repository'] = str(self.remote)
        self.pkg = self.remote / 'skills/threejs-skills'
        self.write_skill(self.pkg, 'threejs-skills')
        (self.pkg / 'assets').mkdir()
        (self.pkg / 'assets/field.bin').write_bytes(b'\x00\xff\x00\x01')
        (self.pkg / 'scripts').mkdir()
        (self.pkg / 'scripts/probe_asset_credentials.sh').write_text('printf SET\n', encoding='utf-8')
        inventory = json.loads((Path(__file__).resolve().parents[2] / 'src/ai_rules/verification/data/threejs_inventory.json').read_text())
        for member in inventory['skills']:
            target = self.pkg / 'skills' / member['name']
            target.mkdir(parents=True)
            (target / 'GUIDE.md').write_text('Internal method fixture\n', encoding='utf8')
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
        with patch.object(cli, 'packaged_bundle', return_value=None), contextlib.chdir(self.remote), \
             contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = cli.main([command, '--host', 'codex', '--scope', scope,
                '--project-root', str(self.project), '--state-dir', str(self.state),
                '--source', source, '--yes', '--non-interactive', *selections])
        return result, output.getvalue()

    def target(self, name, scope='project'):
        return (self.project if scope == 'project' else self.home) / '.agents/skills' / name

    def test_profile_latest_installs_one_complete_family_and_is_noop(self):
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.assertEqual(4, len(list((self.project / '.agents/skills').iterdir())))
        family = self.target('threejs-skills')
        self.assertTrue((family / 'SKILL.md').is_file())
        self.assertEqual(b'\x00\xff\x00\x01', (family / 'assets/field.bin').read_bytes())
        self.assertEqual(45, len(list(family.glob('skills/*/GUIDE.md'))))
        self.assertEqual(1, len(list(family.rglob('SKILL.md'))))
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        lock = json.loads((self.state / 'lock.json').read_text())
        self.assertTrue(all(t['action'] == 'NO_OP' for t in lock['targets']))
        records = json.loads((self.state / 'managed-installations.json').read_text())['installations']
        self.assertEqual('skills/threejs-skills', records['threejs-skills:codex:project']['source']['subpath'])

    def test_family_selection_leaves_legacy_and_unselected_skills_untouched(self):
        legacy = self.target('threejs-shaders')
        self.write_skill(legacy, 'threejs-shaders')
        (legacy / 'personal.txt').write_text('preserve me', encoding='utf8')
        before = contents(legacy)
        result, output = self.run_cli(selections=('--capability', 'threejs-skills'))
        self.assertEqual(0, result, output)
        self.assertEqual({'threejs-shaders', 'threejs-skills'},
                         {p.name for p in (self.project / '.agents/skills').iterdir()})
        self.assertEqual(before, contents(legacy))
        self.assertFalse(self.target('andino-workflow').exists())

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
        selection = ('--capability', 'threejs-skills')
        self.assertEqual(0, self.run_cli(selections=selection)[0])
        (self.pkg / 'new.txt').write_text('revision two', encoding='utf-8')
        self.commit('update shaders')
        result, output = self.run_cli('update', selections=selection)
        self.assertEqual(0, result, output)
        self.assertEqual('revision two', (self.target('threejs-skills') / 'new.txt').read_text())
        self.assertTrue(list((self.state / 'backups').glob('*/threejs-skills/SKILL.md')))
        self.assertFalse(self.target('threejs-lighting').exists())

    def test_latest_preserves_modified_managed_and_unmanaged_conflicts(self):
        selection = ('--capability', 'threejs-skills')
        self.assertEqual(0, self.run_cli(selections=selection)[0])
        personal = self.target('threejs-skills') / 'personal.txt'
        personal.write_text('mine', encoding='utf-8')
        result, output = self.run_cli('update', selections=selection)
        self.assertNotEqual(0, result, output)
        self.assertEqual('mine', personal.read_text())

        result, output = self.run_cli('remove', source='bundled', selections=selection)
        self.assertNotEqual(0, result, output)
        self.assertEqual('mine', personal.read_text())
        self.project = self.root / 'unmanaged-project'
        target = self.target('threejs-skills')
        self.write_skill(target, 'personal-lighting')
        before = contents(target)
        result, output = self.run_cli(selections=('--capability', 'threejs-skills'))
        self.assertNotEqual(0, result, output)
        self.assertEqual(before, contents(target))

    def test_atomic_replacement_rolls_back_failed_binary_verification(self):
        source, target = self.root / 'source', self.root / 'target'
        self.write_skill(source, 'threejs-skills')
        self.write_skill(target, 'threejs-skills')
        (target / 'personal.bin').write_bytes(b'\xff\x00')
        before = contents(target)
        with self.assertRaisesRegex(RuntimeError, 'rolled back'):
            copy_tree_atomic(source, target, self.root / 'backups',
                             verify=lambda path: path != target)
        self.assertEqual(before, contents(target))
        self.assertTrue(list((self.root / 'backups').glob('*/target/personal.bin')))

    def test_doctor_repair_remove_and_global_latest_keep_selected_identity(self):
        selection = ('--capability', 'threejs-skills')
        self.assertEqual(0, self.run_cli(scope='global', selections=selection)[0])
        self.assertTrue((self.target('threejs-skills', 'global') / 'SKILL.md').is_file())
        self.assertEqual(0, self.run_cli(source='bundled', selections=selection)[0])
        result, output = self.run_cli('doctor', source='bundled', selections=selection)
        self.assertEqual(0, result, output)
        (self.target('threejs-skills') / 'SKILL.md').unlink()
        result, output = self.run_cli('doctor', source='bundled', selections=(*selection, '--repair'))
        self.assertEqual(0, result, output)
        self.assertTrue((self.target('threejs-skills') / 'SKILL.md').is_file())
        result, output = self.run_cli('remove', source='bundled', selections=selection)
        self.assertEqual(0, result, output)
        self.assertFalse(self.target('threejs-skills').exists())
        self.assertTrue(self.target('threejs-skills', 'global').exists())

    def test_bundled_update_and_remove_preserve_user_modified_files(self):
        selection = ('--capability', 'threejs-skills')
        self.assertEqual(0, self.run_cli(source='bundled', selections=selection)[0])
        personal = self.target('threejs-skills') / 'personal.txt'
        personal.write_text('mine', encoding='utf-8')
        (self.pkg / 'new.txt').write_text('update', encoding='utf-8')
        self.commit('bundle update')
        result, output = self.run_cli('update', source='bundled', selections=selection)
        self.assertNotEqual(0, result, output)
        self.assertEqual('mine', personal.read_text())

        result, output = self.run_cli('remove', source='bundled', selections=selection)
        self.assertNotEqual(0, result, output)
        self.assertEqual('mine', personal.read_text())

    def test_legacy_bundled_record_without_fingerprints_requires_explicit_review(self):
        selection = ('--capability', 'threejs-skills')
        self.assertEqual(0, self.run_cli(source='bundled', selections=selection)[0])
        record_path = self.state / 'managed-installations.json'
        records = json.loads(record_path.read_text())
        del records['installations']['threejs-skills:codex:project']['files']
        record_path.write_text(json.dumps(records), encoding='utf-8')
        personal = self.target('threejs-skills') / 'personal.txt'
        personal.write_text('legacy personal edit', encoding='utf-8')
        (self.pkg / 'new.txt').write_text('new release', encoding='utf-8')
        self.commit('legacy upgrade')
        result, output = self.run_cli('update', source='bundled', selections=selection)
        self.assertNotEqual(0, result, output)
        self.assertEqual('legacy personal edit', personal.read_text())
        result, output = self.run_cli('remove', source='bundled', selections=selection)
        self.assertNotEqual(0, result, output)
        self.assertEqual('legacy personal edit', personal.read_text())
