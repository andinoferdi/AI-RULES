"""Verify the real setup entrypoint preserves delegation's reviewed tree."""

import contextlib
import io
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest
from urllib.parse import unquote, urlsplit

from ai_rules import cli


ROOT = Path(__file__).resolve().parents[1]


class DelegationDistributionTests(unittest.TestCase):
    def git(self, *arguments):
        result = subprocess.run(['git', *arguments], cwd=ROOT, capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr.decode('utf-8'))
        return result.stdout

    def test_setup_preserves_complete_native_and_nested_skill(self):
        package = ROOT / 'skills/andino-workflow' / 'skills/delegation'
        relative_paths = sorted(item.relative_to(package).as_posix()
                                for item in package.rglob('*') if item.is_file())
        self.assertIn('resources/contract.md', relative_paths)
        self.assertIn('resources/worked-example.md', relative_paths)
        self.assertIn('scripts/task_brief.py', relative_paths)
        expected = {path: (package / path).read_bytes() for path in relative_paths}

        hosts = {
            'codex': '.agents/skills', 'claude-code': '.claude/skills',
            'opencode': '.agents/skills', 'antigravity-cli': '.agents/skills',
            'antigravity-ide': '.agents/skills',
        }
        source = os.environ.get('AI_RULES_DELEGATION_SETUP_SOURCE', 'bundled')
        self.assertIn(source, ('bundled', 'latest'))
        # Live publication smoke uses one adapter; bundled exercises all adapters.
        if source == 'latest':
            hosts = {'codex': hosts['codex']}
        with tempfile.TemporaryDirectory() as temporary:
            for host, relative in hosts.items():
                with self.subTest(host=host, source=source):
                    project = Path(temporary) / host
                    project.mkdir()
                    with contextlib.redirect_stdout(io.StringIO()):
                        result = cli.main([
                            'setup', '--host', host, '--scope', 'project',
                            '--project-root', str(project), '--state-dir', str(project / 'state'),
                            '--capability', 'andino-workflow', '--source', source,
                            '--yes', '--non-interactive',
                        ])
                    self.assertEqual(0, result)
                    skills = project / relative
                    for entrypoint in (skills / 'andino-delegation',
                                       skills / 'andino-workflow/skills/delegation'):
                        for path, content in expected.items():
                            installed = entrypoint / path
                            self.assertTrue(installed.is_file(), str(installed))
                            self.assertEqual(content, installed.read_bytes(), str(installed))
                            if installed.suffix != '.md':
                                continue
                            for destination in re.findall(
                                r'\[[^\]]+\]\(([^)]+)\)', installed.read_text(encoding='utf-8')
                            ):
                                link = urlsplit(destination)
                                if not link.scheme and not link.netloc and link.path:
                                    self.assertTrue(
                                        (installed.parent / unquote(link.path)).is_file(),
                                        f'{installed}: {destination}',
                                    )


if __name__ == '__main__':
    unittest.main()
