"""Real CLI regressions for task extraction; no model-behavior claims."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'skills/delegation/scripts/task_brief.py'


class TaskBriefTests(unittest.TestCase):
    def extract(self, text, task='T1'):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plan, output = root / 'plan.md', root / 'out' / 'brief.md'
            plan.write_text(text, encoding='utf-8')
            result = subprocess.run(
                [sys.executable, '-B', str(SCRIPT), str(plan), task, str(output)],
                capture_output=True, text=True, encoding='utf-8',
                env={**os.environ, 'ANDINO_WORKSPACE_OVERRIDE': str(root / 'scratch')},
            )
            body = output.read_text(encoding='utf-8') if output.exists() else None
            return result, body, output.parent.exists()

    def test_canonical_planning_heading_and_nested_proof(self):
        selected = '#### T1 — export\nbody\n##### Proof\ncheck\n'
        result, body, _ = self.extract('## Phase 1\n' + selected + '#### T2 — next\nother\n')
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(selected, body)

    def test_legacy_heading_keeps_nested_verification(self):
        selected = '## Task T1: export\nbody\n### Verification\ncheck\n'
        result, body, _ = self.extract(selected + '## Appendix\nprivate context\n')
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(selected, body)

    def test_plain_identifier_colon_and_hyphen(self):
        for heading in ('### T1: export', '### T1 - export'):
            with self.subTest(heading=heading):
                result, body, _ = self.extract(heading + '\nbody\n### Footer\nother\n')
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(heading + '\nbody\n', body)

    def test_fake_headings_in_fences_are_not_tasks_or_boundaries(self):
        for fence in ('```', '~~~', '````'):
            with self.subTest(fence=fence):
                inner = '```\n' if len(fence) > 3 else ''
                selected = '## Task T1: export\n' + fence + 'text\n' + inner + '## Task T2: fake\n' + fence + '\nbody\n'
                result, body, _ = self.extract(fence + '\n## Task T1: fake\n' + fence + '\n' + selected + '## End\n')
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(selected, body)

    def test_missing_and_overlapping_ids_do_not_create_output(self):
        result, body, parent_exists = self.extract('## Task T10: other\nbody\n')
        self.assertEqual(3, result.returncode)
        self.assertIsNone(body)
        self.assertFalse(parent_exists)

    def test_duplicate_id_is_rejected_without_output(self):
        result, body, parent_exists = self.extract('## Task T1: first\na\n## Task T1: second\nb\n')
        self.assertEqual(3, result.returncode)
        self.assertIn('ambiguous', result.stderr.lower())
        self.assertIsNone(body)
        self.assertFalse(parent_exists)


if __name__ == '__main__':
    unittest.main(verbosity=2)
