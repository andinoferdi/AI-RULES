import json
import tempfile
import unittest
from pathlib import Path

from ai_rules.catalog import load_catalog
from ai_rules.interactive import build_capability_choices
from ai_rules.profiles import load_profiles
from ai_rules.release.bundles import export_git_ref

ROOT = Path(__file__).resolve().parents[2]


class SingleThreejsFamilyTests(unittest.TestCase):
    def test_menu_offers_one_family_instead_of_internal_methods(self):
        catalog = load_catalog()
        choices = build_capability_choices(catalog.capabilities)
        names = {c.value for c in choices}
        members = {s['name'] for s in json.loads((ROOT / 'docs/threejs/inventory.json').read_text())['skills']}
        self.assertIn('threejs-skills', names)
        self.assertFalse(names & members)
        self.assertEqual(8, len(names))

    def test_profile_installs_one_family_alongside_workflow_dependencies(self):
        catalog = load_catalog()
        profile = load_profiles(catalog).require('threejs')
        self.assertEqual({'threejs-skills', 'andino-workflow', 'focus', 'search-first'}, set(profile.capabilities))
        self.assertEqual(8, len(load_profiles(catalog).require('everything').capabilities))

    def test_installer_source_exports_all_methods_in_one_discoverable_package(self):
        capability = load_catalog().require_capability('threejs-skills')
        inventory = json.loads((ROOT / 'docs/threejs/inventory.json').read_text())
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'threejs-skills'
            manifest = json.loads((ROOT / 'src/ai_rules/release/data/release_manifest.json').read_text())
            export_git_ref(manifest['first_party']['threejs-skills']['commit'], target, ROOT, subpath=capability.source.get('subpath'))
            self.assertEqual(['SKILL.md'], [p.relative_to(target).as_posix() for p in target.rglob('SKILL.md')])
            self.assertEqual(45, len(list(target.glob('skills/*/GUIDE.md'))))
            for member in inventory['skills']:
                folder = target / 'skills' / member['name']
                for item in member['files']:
                    self.assertTrue((folder / item.get('runtime_path', item['path'])).is_file(), (member['name'], item['path']))
