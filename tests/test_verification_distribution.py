import contextlib
import io
import re
import tempfile
import unittest
from pathlib import Path

from ai_rules import cli


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills/andino-workflow/skills/verification'
QUOTED = 'Withhold completion while any required criterion lacks passing evidence.'


class VerificationDistributionTests(unittest.TestCase):
    def test_guide_mirrors_skill_and_keeps_the_quoted_rule(self):
        skill = (SOURCE / 'SKILL.md').read_text(encoding='utf-8')
        guide = (SOURCE / 'GUIDE.md').read_text(encoding='utf-8')
        self.assertEqual(skill.split('---\n', 2)[2], guide)
        # README.md and the marketing pages quote this sentence.
        self.assertIn(QUOTED, ' '.join(skill.split()))

    def test_setup_preserves_both_entrypoints_and_local_resources(self):
        paths = ('SKILL.md', 'GUIDE.md', 'resources/contract.md', 'resources/worked-example.md',
                 'references/license.md')
        expected = {path: (SOURCE / path).read_bytes() for path in paths}
        hosts = {
            'codex': '.agents/skills',
            'claude-code': '.claude/skills',
            'opencode': '.agents/skills',
            'antigravity-cli': '.agents/skills',
            'antigravity-ide': '.agents/skills',
        }
        with tempfile.TemporaryDirectory() as temporary:
            for host, relative in hosts.items():
                with self.subTest(host=host):
                    project = Path(temporary) / host
                    project.mkdir()
                    with contextlib.redirect_stdout(io.StringIO()):
                        result = cli.main([
                            'setup', '--host', host, '--scope', 'project',
                            '--project-root', str(project), '--state-dir', str(project / 'state'),
                            '--capability', 'andino-workflow', '--source', 'bundled',
                            '--yes', '--non-interactive',
                        ])
                    self.assertEqual(0, result)
                    skills = project / relative
                    for entrypoint in (skills / 'andino-verification',
                                       skills / 'andino-workflow/skills/verification'):
                        for path, content in expected.items():
                            installed = entrypoint / path
                            self.assertEqual(content, installed.read_bytes(), str(installed))
                        for filename in ('SKILL.md', 'GUIDE.md', 'resources/contract.md'):
                            for destination in re.findall(
                                r'\[[^\]]+\]\(([^)]+)\)',
                                (entrypoint / filename).read_text(encoding='utf-8'),
                            ):
                                if '://' not in destination and not destination.startswith('#'):
                                    base = (entrypoint / filename).parent
                                    self.assertTrue(
                                        (base / destination.split('#')[0]).is_file(),
                                        f'{entrypoint}/{filename}: {destination}',
                                    )


if __name__ == '__main__':
    unittest.main()
