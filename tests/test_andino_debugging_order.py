"""Debugging-guide load order of the andino-workflow runtime branch.

A host may read the runtime and the task files in one parallel batch, before any
SKILL.md body text is in context. Only the frontmatter description is visible at
that point, so it carries the ordering; the Claude safe-mode harness must show it
the way native skill discovery would. ANDINO_RUNTIME_REF picks the ref.
"""

import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from run_andino_capability_eval import entry_metadata, skill_metadata

REF = os.environ.get('ANDINO_RUNTIME_REF', 'andino-workflow')


def show(ref, path):
    directory = os.environ.get('ANDINO_RUNTIME_DIR')
    if directory and ref == REF:
        return (Path(directory) / path).read_text(encoding='utf-8')
    result = subprocess.run(['git', 'show', f'{ref}:{path}'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        raise unittest.SkipTest(f'{ref}:{path} unavailable')
    return result.stdout.replace('\r\n', '\n')


def flat(text):
    return re.sub(r'\s+', ' ', text)


def description(skill):
    return re.search(r'^description: (.*)$', skill_metadata(skill), re.M).group(1)


class DebuggingOrderContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = show(REF, 'SKILL.md')
        cls.routing = show(REF, 'references/routing.md')

    def test_description_orders_runtime_and_guide_before_task_files(self):
        text = description(self.skill)
        self.assertRegex(text, r'(?i)unknown-cause bugs')
        self.assertRegex(text, r'(?i)read it and any guide it selects before inspecting task files')
        self.assertRegex(text, r'(?i)not in the same parallel batch')
        self.assertLessEqual(len(text), 1024)

    def test_body_requires_the_guide_before_the_first_diagnostic_read(self):
        body = flat(self.skill.split('---', 2)[2])
        self.assertIn('[debugging method](skills/debugging/GUIDE.md)', body)
        self.assertRegex(body, r'before the first diagnostic log/source read')
        self.assertRegex(body, r'same parallel batch does not satisfy this ordering')

    def test_unknown_bug_route_requires_the_debugging_guide(self):
        line = next(line for line in self.routing.splitlines() if line.startswith('| Unknown bug root cause'))
        self.assertIn('REQUIRED', line)
        self.assertIn('skills/debugging/GUIDE.md', line)


class HarnessEntryMetadataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = {'SKILL.md': show(REF, 'SKILL.md')}

    def test_claude_safe_mode_shows_the_entry_description(self):
        metadata = entry_metadata('claude-code', 'isolated', self.files, {})
        self.assertTrue(metadata.startswith('\nRuntime metadata:\n'))
        self.assertIn(description(self.files['SKILL.md']), metadata)

    def test_native_discovery_hosts_and_search_first_entry_add_nothing(self):
        for host, isolation in (('claude-code', 'host-config'), ('codex', 'isolated'),
                                ('antigravity-cli', 'isolated'), ('opencode', 'isolated')):
            self.assertEqual('', entry_metadata(host, isolation, self.files, {}))
        self.assertEqual('', entry_metadata('claude-code', 'isolated', {}, {'entry_skill': 'search-first'}))


if __name__ == '__main__':
    unittest.main()
