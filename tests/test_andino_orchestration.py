"""Guard andino-workflow's multi-unit orchestration against silent loss.

The anchors cover the loop the coordinator adopted from Claude Code's dynamic workflows (a
counted work list, batch-written results, refutation with three outcomes, a second sweep until
a dry round, a coverage line with the stop reason), the ultracode defaults it excludes, the
guard mapping, and the approval wording shared by the guards, delegation and the coexistence
rules. A failing anchor means a rule was dropped. The test reads the real folder.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = 'skills/andino-workflow'
REFERENCE = f'{WORKFLOW}/references/orchestration.md'

HEADINGS = ['## When it applies', '## The loop', '## Unit ledger', '## Patterns',
            '## Agents and engines', '## What this loop does not take from ultracode',
            '## Composition', '## Guard mapping']
STEPS = ['**Scout and list the units.**', '**Pick the rigor.**', '**Work the units.**',
         '**Try to clear every consequential finding.**',
         '**Sweep again by a different method.**', '**Report.**']


def read(path):
    """Return a repository file's text, or '' when it does not exist yet."""
    file = ROOT / path
    return file.read_text(encoding='utf-8') if file.is_file() else ''


def flat(text):
    """Collapse line breaks and runs of spaces so wrapped phrases still match."""
    return ' '.join(text.split())


def section(text, heading):
    """Return the text under a level-2 heading, up to the next level-2 heading."""
    start = text.find(heading + '\n')
    if start < 0:
        return ''
    end = text.find('\n## ', start + len(heading))
    return text[start:end if end >= 0 else len(text)]


class OrchestrationContract(unittest.TestCase):
    def test_skill_trigger_is_short_and_placed(self):
        skill = read(f'{WORKFLOW}/SKILL.md')
        body = section(skill, '## Orchestrate multi-unit work')
        self.assertIn('## Orchestrate multi-unit work', skill)
        self.assertLess(skill.index('## Select work methods first'),
                        skill.index('## Communication support'))
        self.assertLess(skill.index('## Coordinate progress and evidence'),
                        skill.index('## Orchestrate multi-unit work'))
        self.assertLess(skill.index('## Orchestrate multi-unit work'),
                        skill.index('## Bounded execution'))
        self.assertLessEqual(len([line for line in body.splitlines()[1:] if line.strip()]), 12)
        for phrase in ('references/orchestration.md', 'work list', 'in batches', 'different method',
                       'three rounds at most', 'UNVERIFIED', 'delegation envelope',
                       'Single-unit work skips this'):
            self.assertIn(phrase, flat(body))
        self.assertIn('ultracode keyword or mode is not approval',
                      flat(section(skill, '## Bounded execution')))

    def test_reference_keeps_the_loop(self):
        reference = read(REFERENCE)
        for heading in HEADINGS:
            self.assertIn(heading + '\n', reference)
        self.assertEqual(HEADINGS, [line for line in reference.splitlines() if line in HEADINGS])
        for step in STEPS:
            self.assertIn(step, reference)
        for phrase in ('**Standard** is the default', 'self-checked', 'CONFIRMED', 'REFUTED',
                       'UNVERIFIED', 'Results held only in context are lost at a usage limit',
                       'no silent caps', 'Coverage: <done> of <total> units', 'three rounds',
                       'more than about 20 tool turns', 'CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS',
                       'same session'):
            self.assertIn(phrase, flat(reference))

    def test_report_reconciles_every_unit_with_the_count(self):
        report = flat(read(REFERENCE))
        self.assertIn('List every unit once with its verdict', report)
        self.assertIn('every unit appears exactly once in the report or its ledger', report)
        self.assertIn('the coverage total equals that count', report)

    def test_reference_excludes_ultracode_defaults(self):
        excluded = flat(section(read(REFERENCE), '## What this loop does not take from ultracode'))
        for phrase in ('every substantive task', '"Token cost is not a constraint"',
                       'three at once', 'states its model and effort', 'is not approval'):
            self.assertIn(phrase, excluded)

    def test_guards_name_loop_exits_and_one_approval(self):
        guards = flat(read(f'{WORKFLOW}/references/anti-loop.md'))
        self.assertIn('names its exit before it starts', guards)
        self.assertIn('one approval covers the waves it lists', guards)
        self.assertIn('ultracode keyword or mode) is not approval', guards)
        self.assertIn('results held only in context are lost at a usage limit', guards)
        self.assertNotIn('Before each wave', guards)

    def test_unit_ledger_in_checkpoint_and_resume(self):
        plan = read(f'{WORKFLOW}/references/execution-plan.md')
        self.assertIn('## Unit ledger for multi-unit work', plan)
        self.assertIn('## Unit Ledger (multi-unit work only)',
                      read(f'{WORKFLOW}/references/execution-plan-template.md'))
        self.assertIn('reopen only the units that changed',
                      flat(read(f'{WORKFLOW}/references/handoff.md')))

    def test_coexistence_registry_and_readme(self):
        coexist = read(f'{WORKFLOW}/references/capability-coexistence.md')
        self.assertIn('Workflow tool / ultracode / Andino orchestration', coexist)
        self.assertIn('search-first Full mode / orchestration', coexist)
        registry = read(f'{WORKFLOW}/references/capability-registry.md')
        self.assertIn('| [rea](#rea) | MCP |', registry)
        self.assertRegex(registry, r'(?m)^## rea\n\n- Type: MCP$')
        self.assertIn('Workflow tool', section(registry, '## native-capabilities'))
        self.assertIn('references/orchestration.md', read(f'{WORKFLOW}/README.md'))

    def test_delegation_host_notes(self):
        notes = flat(read(f'{WORKFLOW}/skills/delegation/resources/host-cost-calibration.md'))
        for phrase in ('CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS',
                       'CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS', 'backticks', 'same session only',
                       'CLAUDE_CODE_EFFORT_LEVEL'):
            self.assertIn(phrase, notes)
        self.assertIn('holds the 3-agent limit',
                      flat(read(f'{WORKFLOW}/skills/delegation/resources/contract.md')))

    def test_guard_mapping_covers_all_ten(self):
        mapping = section(read(REFERENCE), '## Guard mapping')
        self.assertEqual(list(range(1, 11)),
                         [int(n) for n in re.findall(r'^\| (\d+) ', mapping, re.M)])


if __name__ == '__main__':
    unittest.main()
