"""Keep andino-optimize-prompt's bundled patterns identical to README's How to Prompt rules."""

import os
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
RESOURCE = 'skills/optimize-prompt/resources/prompt-patterns.md'
WORKED_EXAMPLE = 'skills/optimize-prompt/resources/worked-example.md'
SLOTS = ('Skills', 'Tools/MCP', 'Mode', 'Task', 'Context/evidence', 'Done when', 'Constraints')
HEADER_SLOTS = SLOTS[:3]


def runtime_resource(path=RESOURCE):
    directory = os.environ.get('ANDINO_RUNTIME_DIR')
    if directory:
        return (Path(directory) / path).read_text(encoding='utf-8')
    ref = os.environ.get('ANDINO_RUNTIME_REF', 'origin/andino-workflow')
    return subprocess.check_output(['git', 'show', f'{ref}:{path}'], cwd=ROOT).decode('utf-8')


def layout_problems(block):
    """Layout rules from How to Prompt: grouped header slots, blank lines, bullets, no hand wrap."""
    problems, slot, bullets = [], None, 0
    lines = block.rstrip('\n').split('\n')
    for number, line in enumerate(lines, 1):
        label = line.split(':', 1)[0]
        if label in SLOTS:
            if slot is not None and lines[number - 2].strip() and label not in HEADER_SLOTS:
                problems.append(f'line {number}: no blank line before {label}')
            if slot is not None and label in HEADER_SLOTS and not lines[number - 2].strip():
                problems.append(f'line {number}: blank line inside the Skills/Tools/MCP/Mode group')
            if slot and slot.endswith(':') and bullets < 2:
                problems.append(f'{slot} has fewer than two bullets')
            slot, bullets = (label + ':' if line == label + ':' else label), 0
        elif line.startswith('- '):
            if not (slot or '').endswith(':'):
                problems.append(f'line {number}: bullet outside a multi-item slot')
            bullets += 1
        elif line.strip():
            problems.append(f'line {number}: not a slot, bullet or blank line: {line!r}')
    if slot and slot.endswith(':') and bullets < 2:
        problems.append(f'{slot} has fewer than two bullets')
    return problems


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


class PromptLayoutIsReadable(unittest.TestCase):
    def assert_readable(self, source, blocks):
        self.assertTrue(blocks, source)
        for block in blocks:
            with self.subTest(source=source, prompt=block.splitlines()[0]):
                self.assertEqual(layout_problems(block), [])

    def test_readme_template_and_examples(self):
        readme = (ROOT / 'README.md').read_text(encoding='utf-8').replace('\r\n', '\n')
        self.assert_readable('README Layer 2', text_blocks(section(readme, '### Layer 2: the task, seven slots')))
        self.assert_readable('README Examples', text_blocks(section(readme, '### Examples')))

    def test_prompt_examples_doc(self):
        doc = (ROOT / 'docs' / 'prompt-examples.md').read_text(encoding='utf-8').replace('\r\n', '\n')
        self.assert_readable('docs/prompt-examples.md', text_blocks(doc))

    def test_bundled_skill_resources(self):
        resource = runtime_resource().replace('\r\n', '\n')
        self.assert_readable('prompt-patterns slot contract', text_blocks(section(resource, '## Slot contract')))
        self.assert_readable('prompt-patterns examples', text_blocks(section(resource, '## Examples')))
        worked = runtime_resource(WORKED_EXAMPLE).replace('\r\n', '\n')
        self.assert_readable('worked-example output', text_blocks(section(worked, '## Output')))

    def test_checker_rejects_the_old_layout(self):
        old = ('Mode: just do it\nTask: fix it.\nContext/evidence: repro: open /id.\n'
               '  Error: [paste]\nDone when:\n- one check\n')
        self.assertEqual(len(layout_problems(old)), 5)


if __name__ == '__main__':
    unittest.main()
