"""Phase-readiness routing contract of the andino-workflow runtime branch.

Reads the runtime through git like the other validators. ANDINO_RUNTIME_REF picks
the ref (default: local andino-workflow); unchanged-contract checks compare with
the pre-readiness release when that commit is available.
"""

import os
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = os.environ.get('ANDINO_RUNTIME_REF', 'andino-workflow')
BASE = '634585a45866261e0d981a68098fa7f1b4bf4c0e'


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


def row(text, first_cell):
    for line in text.splitlines():
        if line.startswith('| ' + first_cell):
            return line
    raise AssertionError(f'missing table row: {first_cell}')


def section(text, heading):
    match = re.search(rf'^## {re.escape(heading)}\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    if not match:
        raise AssertionError(f'missing section: {heading}')
    return flat(match.group(1))


class PhaseReadinessContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.routing = show(REF, 'references/routing.md')
        cls.skill = show(REF, 'SKILL.md')
        cls.index = show(REF, 'references/internal-method-index.md')

    def test_precedence_places_readiness_before_required_routes(self):
        precedence = re.search(r'Apply explicit user choices and exclusions first,(.*?)\.', flat(self.routing)).group(1)
        self.assertLess(precedence.find('phase readiness'), precedence.find('REQUIRED'))
        self.assertGreaterEqual(precedence.find('phase readiness'), 0)
        self.assertIn('current', precedence[precedence.find('REQUIRED'):])

    def test_readiness_distinguishes_what_is_open(self):
        readiness = section(self.routing, 'Phase readiness')
        for method in ('brainstorming', 'decision-interview', 'idea-refine', 'plain-language-repitch',
                       'learning-workspace', 'human-procedure'):
            self.assertIn(f'skills/{method}/GUIDE.md', readiness)
        self.assertRegex(readiness, r'(?i)delegat')
        self.assertRegex(readiness, r'(?i)accepted')
        self.assertRegex(readiness, r'(?i)not a (trigger|keyword)')
        self.assertRegex(readiness, r'(?i)unresolved material user decision')
        self.assertRegex(readiness, r'(?i)not a sequence|alternatives')

    def test_exploratory_routes_are_required_only_under_their_condition(self):
        brainstorming = row(self.routing, 'Uncertain goal')
        self.assertIn('REQUIRED', brainstorming)
        self.assertRegex(brainstorming, r'(?i)not delegated')
        interview = row(self.routing, 'Unclear product requirements')
        self.assertIn('REQUIRED', interview)
        self.assertRegex(interview, r'(?i)inspect evidence')

    def test_design_routes_wait_for_a_resolved_or_delegated_direction(self):
        for first_cell in ('New visual direction', 'UI/UX design or evaluation', 'Both a new visual direction'):
            line = row(self.routing, first_cell)
            self.assertIn('REQUIRED', line)
            self.assertRegex(line, r'(?i)resolved or delegated')

    def test_entrypoint_separates_discoverable_facts_from_user_owned_direction(self):
        if '## Coordinate progress and evidence' in self.skill:
            asking = section(self.skill, 'Coordinate progress and evidence')
            selection = section(self.skill, 'Select work methods first')
            self.assertRegex(asking, r'(?i)Resolve discoverable facts before asking')
            self.assertRegex(asking, r'(?i)missing material user-owned')
            self.assertRegex(selection, r'(?i)does not override phase readiness')
        else:
            asking = section(self.skill, 'Investigate before asking')
            self.assertRegex(asking, r'(?i)phase readiness')
            self.assertRegex(asking, r'(?i)user-owned')
            self.assertRegex(asking, r'(?i)does not override phase readiness')

    def test_method_index_covers_mixed_execution_and_uncertainty(self):
        self.assertRegex(row(self.index, '[brainstorming]'), r'(?i)build request')
        self.assertRegex(row(self.index, '[brainstorming]'), r'(?i)running or understanding')
        self.assertRegex(row(self.index, '[decision-interview]'), r'(?i)open product direction')


class UnchangedContractsTest(unittest.TestCase):
    """Protect required support; the user intentionally replaces the old Focus-first order."""

    @classmethod
    def setUpClass(cls):
        cls.base_routing = show(BASE, 'references/routing.md')
        cls.base_skill = show(BASE, 'SKILL.md')
        cls.routing = show(REF, 'references/routing.md')
        cls.skill = show(REF, 'SKILL.md')

    def test_required_route_rows_are_unchanged(self):
        for first_cell in ('New feature with likely reusable solutions', 'Thesis/research status', 'Unknown bug root cause',
                           'Behavior change needing a regression', 'Consequential claim that implementation',
                           'Explicit Council request', 'Acceptance needs browser interaction'):
            self.assertEqual(row(self.base_routing, first_cell), row(self.routing, first_cell))

    def test_research_contract_preserved_and_task_guides_precede_focus(self):
        if '## Ownership and precedence' in self.skill:
            # Thin entry delegates the full research procedure to its real owner.
            # Required route rows remain separately protected above.
            communication = section(self.skill, 'Communication support')
            self.assertIn('Setup also installs `search-first`', communication)
            self.assertRegex(communication, r'Select and activate it.*before.*solution research')
            self.assertIn('actual procedure and resource requirements', communication)
            self.assertIn('unavailable access leaves external claims unverified', communication)
        else:
            start = self.base_skill.index('Setup also installs `search-first`')
            end = self.base_skill.index('\n\n', start)
            self.assertIn(self.base_skill[start:end], self.skill)
        # Older immutable snapshots retain their historical order. Candidate checks
        # opt into working bytes, where the user-authorized policy is internal-first.
        if '## Select work methods first' in self.skill:
            self.assertLess(self.skill.index('## Select work methods first'),
                            self.skill.index('## Communication support'))
            self.assertIn('before Focus', self.skill)
            self.assertIn('default communication layer', self.skill)
            self.assertIn('before the first diagnostic log/source read', self.skill)
            self.assertIn('permission', self.routing)
            communication = section(self.skill, 'Communication support')
            self.assertRegex(communication, r'Activate.*through the \[host contract\]')
            self.assertIn('reusing valid activation', communication)
            self.assertIn('user style overrides', communication)
            self.assertIn('absence does not block authorized task work', communication)
            self.assertRegex(communication, r'disclose the boundary without claiming it was loaded')
        else:
            self.assertIn('before the first diagnostic log/source read', self.skill)


if __name__ == '__main__':
    unittest.main()
