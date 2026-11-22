"""Package boundaries of the consolidated 31-member andino-workflow runtime; fresh consumer evidence is separate."""
import json
import os
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
# Pre-migration ownership wording that members must not reintroduce.
OLD_OWNERSHIP = (
    'Andino Workflow governs overall lifecycle,',
    'Read the accepted task/contract, current repository and relevant evidence first. Andino owns',
    'Andino retains discovery, reasoning depth,',
    'Andino owns routing, depth,',
    'Andino owns selection, depth, scope,',
    'Andino owns scope, depth, routing,',
    'Andino remains the automatic capability router and sole lifecycle owner.',
)


class ThinCoordinatorContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        runtime = Path(os.environ.get('ANDINO_RUNTIME_DIR') or ROOT / 'skills/andino-workflow')
        cls.files = {path.relative_to(runtime).as_posix(): path.read_text(encoding='utf-8')
                     for path in runtime.rglob('*')
                     if path.is_file() and path.suffix in ('.md', '.json') and '.git' not in path.parts}

    def members(self):
        return json.loads(self.files['references/portfolio.json'])['members']

    def test_all_member_techniques_survive_ownership_migration(self):
        # The 31-member consolidation rewrote member bodies, so the pre-consolidation
        # baseline no longer applies; the portfolio is the member source of truth.
        guides = {path.split('/')[1] for path in self.files if re.fullmatch(r'skills/[^/]+/GUIDE.md', path)}
        self.assertEqual(sorted(self.members()), sorted(guides))
        for member in self.members():
            for path in (f'skills/{member}/GUIDE.md', f'skills/{member}/SKILL.md'):
                with self.subTest(path=path):
                    self.assertTrue(self.files[path].strip())
                    for phrase in OLD_OWNERSHIP:
                        self.assertNotIn(phrase, self.files[path])
            skill = self.files[f'skills/{member}/SKILL.md']
            self.assertRegex(skill, rf'(?m)^name: andino-{re.escape(member)}\r?$')
            self.assertIn('> **Andino Workflow Member Skill**', skill)

    def test_guard_inventory_and_artifact_exception_are_explicit(self):
        guards = self.files['references/anti-loop.md']
        self.assertEqual(list(range(1, 11)),
                         [int(n) for n in re.findall(r'^\| (\d+)\.', guards, re.M)])
        self.assertIn('at most twice with backoff', guards)
        self.assertIn('permission or daily-quota failures unchanged', guards)
        self.assertIn('never claim already-injected definitions were unloaded', guards)
        self.assertIn('Required code, specs and plans remain complete', guards)
        self.assertIn('no nested spawning', guards)
        self.assertIn('turn incomplete work into a DONE claim', guards)

    def test_registry_and_host_do_not_deny_member_native_identity(self):
        index = self.files['references/internal-method-index.md']
        public = index.split('## Selective resources')[0]
        linked = re.findall(r'\(\.\./skills/([^/]+)/SKILL.md\)', public)
        self.assertEqual(sorted(self.members()), sorted(linked))
        self.assertNotIn('not native skills', index)
        host = self.files['references/invocation-adapter.md']
        self.assertIn('native `andino-<id>` SKILL.md', host)
        self.assertIn('explicit native provider', host)


if __name__ == '__main__':
    unittest.main()
