import contextlib
import io
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from ai_rules import cli


ROOT = Path(__file__).resolve().parents[2]


class BrainstormingDistributionTests(unittest.TestCase):
    def test_setup_preserves_both_entrypoints_and_local_resources(self):
        manifest = json.loads(
            (ROOT / 'src/ai_rules/release/data/release_manifest.json').read_text(encoding='utf-8')
        )
        commit = manifest['first_party']['andino-workflow']['commit']
        paths = ('SKILL.md', 'GUIDE.md', 'resources/worked-example.md')
        expected = {
            path: subprocess.check_output(
                ['git', 'show', f'{commit}:skills/brainstorming/{path}'], cwd=ROOT
            )
            for path in paths
        }
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
                    for entrypoint in (skills / 'andino-brainstorming',
                                       skills / 'andino-workflow/skills/brainstorming'):
                        for path, content in expected.items():
                            installed = entrypoint / path
                            self.assertEqual(content, installed.read_bytes(), str(installed))
                        for filename in ('SKILL.md', 'GUIDE.md'):
                            for destination in re.findall(
                                r'\[[^\]]+\]\(([^)]+)\)',
                                (entrypoint / filename).read_text(encoding='utf-8'),
                            ):
                                if '://' not in destination and not destination.startswith('#'):
                                    self.assertTrue(
                                        (entrypoint / destination.split('#')[0]).is_file(),
                                        f'{entrypoint}/{filename}: {destination}',
                                    )


if __name__ == '__main__':
    unittest.main()
