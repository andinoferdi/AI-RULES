"""Keep andino-optimize-prompt consistent with README and its own contract."""

import os
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RESOURCE = 'skills/optimize-prompt/resources/prompt-patterns.md'
WORKED_EXAMPLE = 'skills/optimize-prompt/resources/worked-example.md'
SKILL = 'skills/optimize-prompt/SKILL.md'
GUIDE = 'skills/optimize-prompt/GUIDE.md'
SLOTS = ('Skills', 'Tools/MCP', 'Mode', 'Task', 'Context/evidence', 'Done when', 'Constraints')
HEADER_SLOTS = SLOTS[:3]


def runtime_resource(path=RESOURCE):
    directory = os.environ.get('ANDINO_RUNTIME_DIR') or ROOT / 'skills/andino-workflow'
    return (Path(directory) / path).read_text(encoding='utf-8')


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

    def test_skill_and_mcp_pickers_match(self):
        self.assertEqual(table(section(self.readme, '### Which skill do I name?')),
                         table(section(self.resource, '## Which skill to name')))
        self.assertEqual(table(section(self.readme, '### Which MCP do I name?')),
                         table(section(self.resource, '## Which MCP to name')))

    def test_skill_fit_notes_match(self):
        note = next(line for line in section(self.readme, '### Which skill do I name?').splitlines()
                    if line.startswith('`council` runs five advisors'))
        self.assertIn(note, self.resource)


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

    def test_checker_rejects_the_old_layout(self):
        old = ('Mode: just do it\nTask: fix it.\nContext/evidence: repro: open /id.\n'
               '  Error: [paste]\nDone when:\n- one check\n')
        self.assertEqual(len(layout_problems(old)), 5)


class LightEditorContract(unittest.TestCase):
    TOKEN = re.compile(r'https?://[^\s,;)]+|[A-Za-z]:\\[^\s,;)]+|\b[a-z0-9]+(?:-[a-z0-9]+)+\b')

    def test_skill_and_guide_share_one_body(self):
        def body(text):
            return text.replace('\r\n', '\n').split('## Purpose and selection', 1)[1]
        self.assertEqual(body(runtime_resource(SKILL)), body(runtime_resource(GUIDE)))

    def test_no_rule_drops_or_adds_user_choices(self):
        skill = runtime_resource(SKILL)
        for phrase in ('Phase routing', 'Missing owner', 'Remove them from `Skills`', 'seven-slot'):
            self.assertNotIn(phrase, skill)
        self.assertIn('never a reason to drop, merge or reorder them', skill)

    def test_worked_examples_keep_every_named_token_in_order(self):
        worked = runtime_resource(WORKED_EXAMPLE).replace('\r\n', '\n')
        examples = re.split(r'^## Example \d+', worked, flags=re.M)[1:]
        self.assertGreaterEqual(len(examples), 2)
        for example in examples:
            raw = text_blocks(section(example, '### Raw prompt'))[0]
            out = text_blocks(section(example, '### Output'))[0]
            with self.subTest(raw=raw.splitlines()[0]):
                for token in self.TOKEN.findall(raw):
                    self.assertIn(token, out)
                header = [out.index(token) for token in self.TOKEN.findall(raw.splitlines()[0])]
                self.assertEqual(sorted(header), header)


if __name__ == '__main__':
    unittest.main()
