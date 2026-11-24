import json
import re
import tempfile
import unittest
from pathlib import Path

from ai_rules.catalog import load_catalog
from ai_rules.interactive import build_capability_choices
from ai_rules.profiles import load_profiles
from ai_rules.release.bundles import export_git_ref

ROOT = Path(__file__).resolve().parents[1]


class SingleThreejsFamilyTests(unittest.TestCase):
    METHODS = {s['name'] for s in json.loads((ROOT / 'src/ai_rules/verification/data/threejs_inventory.json').read_text())['skills']}
    INDEXES = ('skills/threejs-skills/references/specialists.md',
               'skills/andino-workflow/references/threejs-specialists.md')

    def test_menu_offers_one_family_instead_of_internal_methods(self):
        catalog = load_catalog()
        choices = build_capability_choices(catalog.capabilities)
        names = {c.value for c in choices}
        members = {s['name'] for s in json.loads((ROOT / 'src/ai_rules/verification/data/threejs_inventory.json').read_text())['skills']}
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
        inventory = json.loads((ROOT / 'src/ai_rules/verification/data/threejs_inventory.json').read_text())
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'threejs-skills'
            # The committed skills/ folder, exported the way release staging does it.
            export_git_ref('HEAD', target, ROOT, subpath=capability.source['subpath'])
            self.assertEqual(['SKILL.md'], [p.relative_to(target).as_posix() for p in target.rglob('SKILL.md')])
            self.assertEqual(len(inventory['skills']), len(list(target.glob('skills/*/GUIDE.md'))))
            for member in inventory['skills']:
                folder = target / 'skills' / member['name']
                for item in member['files']:
                    self.assertTrue((folder / item.get('runtime_path', item['path'])).is_file(), (member['name'], item['path']))

    def test_named_methods_exist(self):
        pattern = re.compile(r'`\$?((?:threejs|nixie-fx)-[a-z0-9-]+)`')
        for rel in ('skills/threejs-skills/SKILL.md', 'skills/threejs-skills/README.md', *self.INDEXES):
            named = set(pattern.findall((ROOT / rel).read_text(encoding='utf-8')))
            self.assertEqual(set(), named - self.METHODS - {'threejs-skills'}, rel)

    def test_every_method_is_indexed(self):
        for rel in self.INDEXES:
            text = (ROOT / rel).read_text(encoding='utf-8')
            self.assertEqual(set(), {m for m in self.METHODS if f'`{m}`' not in text and f'[{m}]' not in text}, rel)

    def test_root_contract_requires_target_and_selection_record(self):
        text = (ROOT / 'skills/threejs-skills/SKILL.md').read_text(encoding='utf-8')
        for literal in ('## Selection record', 'Target: stylized | photoreal', 'Renderer: WebGL | WebGPU',
                        'Selected:', 'Not needed:', '`threejs-realism-director`', 'read in full'):
            self.assertIn(literal, text)
