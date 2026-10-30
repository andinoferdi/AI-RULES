import contextlib
import io
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

from ai_rules import cli


ROOT = Path(__file__).resolve().parents[2]
PLAN_EXECUTION_PATHS = (
    'SKILL.md', 'GUIDE.md', 'resources/contract.md', 'resources/worked-example.md',
)


class PlanExecutionDistributionTests(unittest.TestCase):
    def plan_execution_bytes(self, ref, path):
        result = subprocess.run(
            ['git', 'show', f'{ref}:skills/plan-execution/{path}'], cwd=ROOT,
            capture_output=True,
        )
        self.assertEqual(0, result.returncode, result.stderr.decode('utf-8'))
        return result.stdout

    def test_setup_preserves_both_entrypoints_and_resolves_local_links(self):
        manifest = json.loads(
            (ROOT / 'src/ai_rules/release/data/release_manifest.json').read_text(encoding='utf-8')
        )
        commit = manifest['first_party']['andino-workflow']['commit']
        expected_ref = os.environ.get('AI_RULES_EXPECTED_PLAN_EXECUTION_REF', commit)
        expected = {
            path: self.plan_execution_bytes(expected_ref, path)
            for path in PLAN_EXECUTION_PATHS
        }
        for path, content in expected.items():
            self.assertEqual(
                content, self.plan_execution_bytes(commit, path),
                f'manifest pin {commit}: skills/plan-execution/{path}',
            )

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
                    for entrypoint in (skills / 'andino-plan-execution',
                                       skills / 'andino-workflow/skills/plan-execution'):
                        for path, content in expected.items():
                            installed = entrypoint / path
                            with self.subTest(installed=str(installed)):
                                self.assertTrue(installed.is_file(), str(installed))
                                self.assertEqual(content, installed.read_bytes(), str(installed))
                                for destination in re.findall(
                                    r'\[[^\]]+\]\(([^)]+)\)',
                                    installed.read_text(encoding='utf-8'),
                                ):
                                    link = urlsplit(destination)
                                    if not link.scheme and not link.netloc and link.path:
                                        self.assertTrue(
                                            (installed.parent / unquote(link.path)).is_file(),
                                            f'{installed}: {destination}',
                                        )


if __name__ == '__main__':
    unittest.main()
