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
PLANNING_PATHS = (
    'SKILL.md', 'GUIDE.md', 'resources/contract.md', 'resources/worked-example.md',
)
WORKFLOW_PATHS = (
    'references/execution-plan.md', 'references/execution-plan-template.md',
)


class PlanningDistributionTests(unittest.TestCase):
    def workflow_bytes(self, ref, path):
        result = subprocess.run(
            ['git', 'show', f'{ref}:{path}'], cwd=ROOT,
            capture_output=True,
        )
        self.assertEqual(0, result.returncode, result.stderr.decode('utf-8'))
        return result.stdout

    def planning_bytes(self, ref, path):
        return self.workflow_bytes(ref, f'skills/planning/{path}')

    def test_setup_preserves_both_entrypoints_and_resolves_local_links(self):
        manifest = json.loads(
            (ROOT / 'src/ai_rules/release/data/release_manifest.json').read_text(encoding='utf-8')
        )
        commit = manifest['first_party']['andino-workflow']['commit']
        # Release checks can detect a stale pin without requiring a branch in CI.
        expected_ref = os.environ.get('AI_RULES_EXPECTED_PLANNING_REF', commit)
        expected = {
            path: self.planning_bytes(expected_ref, path)
            for path in PLANNING_PATHS
        }
        for path, content in expected.items():
            self.assertEqual(
                content, self.planning_bytes(commit, path),
                f'manifest pin {commit}: skills/planning/{path}',
            )
        workflow_expected = {
            path: self.workflow_bytes(expected_ref, path) for path in WORKFLOW_PATHS
        }
        for path, content in workflow_expected.items():
            self.assertEqual(content, self.workflow_bytes(commit, path),
                             f'manifest pin {commit}: {path}')

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
                    for path, content in workflow_expected.items():
                        installed = skills / 'andino-workflow' / path
                        self.assertEqual(content, installed.read_bytes(), str(installed))
                    for entrypoint in (skills / 'andino-planning',
                                       skills / 'andino-workflow/skills/planning'):
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
