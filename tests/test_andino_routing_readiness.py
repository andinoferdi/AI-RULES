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
        asking = section(self.skill, 'Investigate before asking')
        self.assertRegex(asking, r'(?i)phase readiness')
        self.assertRegex(asking, r'(?i)user-owned')
        self.assertRegex(asking, r'(?i)does not override phase readiness')

    def test_method_index_covers_mixed_execution_and_uncertainty(self):
        self.assertRegex(row(self.index, '[brainstorming]'), r'(?i)build request')
        self.assertRegex(row(self.index, '[brainstorming]'), r'(?i)running or understanding')
        self.assertRegex(row(self.index, '[decision-interview]'), r'(?i)open product direction')


class UnchangedContractsTest(unittest.TestCase):
    """Readiness must not weaken Focus, debugging, Search First, TDD, verification or thesis routes."""

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

    def test_focus_and_debugging_entry_contracts_are_unchanged(self):
        for paragraph in ('At every invocation, select `focus`', 'When the request already establishes an unknown-cause bug',
                          'Setup also installs `search-first`'):
            start = self.base_skill.index(paragraph)
            end = self.base_skill.index('\n\n', start)
            self.assertIn(self.base_skill[start:end], self.skill)
        start = self.base_routing.index('`focus` is the required default')
        end = self.base_routing.index('\n\n', start)
        self.assertIn(self.base_routing[start:end], self.routing)


if __name__ == '__main__':
    unittest.main()
