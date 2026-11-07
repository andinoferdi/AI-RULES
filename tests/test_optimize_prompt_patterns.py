"""Keep andino-optimize-prompt's bundled patterns identical to README's How to Prompt rules."""

import os
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
RESOURCE = 'skills/optimize-prompt/resources/prompt-patterns.md'


def runtime_resource():
    directory = os.environ.get('ANDINO_RUNTIME_DIR')
    if directory:
        return (Path(directory) / RESOURCE).read_text(encoding='utf-8')
    ref = os.environ.get('ANDINO_RUNTIME_REF', 'origin/andino-workflow')
    return subprocess.check_output(['git', 'show', f'{ref}:{RESOURCE}'], cwd=ROOT).decode('utf-8')


def section(text, heading):
    start = text.index(heading + '\n')
    rest = text[start + len(heading) + 1:]
    end = re.search(r'^#{2,3} ', rest, re.M)
    return rest[:end.start()] if end else rest


def table(text):
    return [line for line in text.splitlines() if line.startswith('|')]


def text_blocks(text):
    return re.findall(r'```text\n(.*?)```', text, re.S)


class PromptPatternsMatchReadme(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = (ROOT / 'README.md').read_text(encoding='utf-8').replace('\r\n', '\n')
        cls.resource = runtime_resource().replace('\r\n', '\n')

    def test_slot_contract_is_the_readme_layer_two_block(self):
        readme = text_blocks(section(self.readme, '### Layer 2: the task, seven slots'))[0]
        self.assertEqual(readme, text_blocks(section(self.resource, '## Slot contract'))[0])

    def test_skill_and_mcp_pickers_match(self):
        self.assertEqual(table(section(self.readme, '### Which skill do I name?')),
                         table(section(self.resource, '## Which skill to name')))
        self.assertEqual(table(section(self.readme, '### Which MCP do I name?')),
                         table(section(self.resource, '## Which MCP to name')))

    def test_skill_fit_notes_match(self):
        note = next(line for line in section(self.readme, '### Which skill do I name?').splitlines()
                    if line.startswith('`council` runs five advisors'))
        self.assertIn(note, self.resource)

    def test_every_bundled_example_is_a_readme_example(self):
        examples = '\n'.join(text_blocks(section(self.readme, '### Examples')))
        bundled = text_blocks(section(self.resource, '## Examples'))
        self.assertTrue(bundled)
        for block in bundled:
            with self.subTest(example=block.splitlines()[0]):
                self.assertIn(block.strip('\n'), examples)


if __name__ == '__main__':
    unittest.main()
