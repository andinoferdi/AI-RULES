"""Offline regression tests; all mutations and Git writes stay in disposable fixtures."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_lens_fixture(destination):
    paths = ['SKILL.md', 'references/method-dispatch.md',
             'references/internal-method-index.md',
             'tests/fixtures/decision_lens_cases.json',
             'tests/fixtures/decision_lens_contract.json',
             'docs/specs/skill-system-refinement.md',
             'scripts/verify_decision_lens.py']
    paths += [str(p.relative_to(ROOT)) for p in (ROOT / 'skills').glob('*/SKILL.md')]
    for relative in paths:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)


class DecisionLensRegression(unittest.TestCase):
    def run_lens(self, root):
        return subprocess.run([sys.executable, '-B', str(root / 'scripts/verify_decision_lens.py')],
                              cwd=root, capture_output=True, text=True, encoding='utf-8', timeout=20)

    def test_real_debugging_route_mutation_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copy_lens_fixture(root)
            control = self.run_lens(root)
            self.assertEqual(control.returncode, 0, f"Unmutated control failed: {control.stdout + control.stderr}")
            for relative in ('SKILL.md', 'references/method-dispatch.md'):
                path = root / relative
                text = path.read_text(encoding='utf-8')
                old = '| Diagnostic | `andino-debugging` |'
                self.assertIn(old, text)
                path.write_text(text.replace(old, '| Diagnostic | `andino-delegation` |'), encoding='utf-8')
            result = self.run_lens(root)
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('Diagnostic', result.stderr, f"Failure must target Diagnostic mismatch: {result.stderr}")


class DelegationSafetyRegression(unittest.TestCase):
    def test_helpers_do_not_leave_source_import_caches(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for relative in ('scripts/verify_delegation_elevation.py',
                             'skills/delegation/scripts/delegation_workspace.py',
                             'skills/delegation/scripts/task_brief.py',
                             'skills/delegation/scripts/review_package.py',
                             'skills/delegation/scripts/delegation-workspace',
                             'skills/delegation/scripts/task-brief',
                             'skills/delegation/scripts/review-package'):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, target)
            plan = root / 'docs/exec-plans/active/delegation-elevation.md'
            plan.parent.mkdir(parents=True)
            plan.write_text('# Test Plan\n\n### Task 1: Isolate\nKeep task content.\n', encoding='utf-8')
            code = "import runpy; m=runpy.run_path('scripts/verify_delegation_elevation.py'); m['test_helper_scripts']()"
            result = subprocess.run([sys.executable, '-B', '-c', code], cwd=root,
                                    capture_output=True, text=True, encoding='utf-8', timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(list((root / 'skills').rglob('*.pyc')), [], 'helper imports leaked bytecode into source')


class DebuggingPreservationRegression(unittest.TestCase):
    DEBUGGING_PATHS = [
        'skills/debugging/SKILL.md',
        'skills/debugging/GUIDE.md',
        'skills/debugging/resources/contract.md',
        'skills/debugging/resources/defense-and-recovery.md',
    ]

    DANGEROUS_PATTERNS = [
        r'git\s+checkout\s+(?:\.|--\s+\.)',
        r'git\s+reset\s+--hard',
        r'git\s+clean\s+-[a-zA-Z]*f',
        r'git\s+restore\s+\.',
        r'whole[- ]tree\s+(?:checkout|reset|clean)',
        r'(?:reset|checkout|clean)\s+(?:the\s+)?whole\s+working\s+tree',
    ]

    PROHIBITION_PATTERN = re.compile(
        r'\b(never|forbidden|forbid(?:s)?|prohibit(?:ed|s)?|do\s+not|don[\'’]t|must\s+not|without)\b',
        re.IGNORECASE
    )

    @classmethod
    def check_debugging_doc(cls, path_or_text):
        if isinstance(path_or_text, Path):
            text = path_or_text.read_text(encoding='utf-8')
        else:
            text = str(path_or_text)

        has_preservation = (
            re.search(r'preserve.*(?:user|pre-existing).*edits', text, re.IGNORECASE) or
            re.search(r'restore.*(?:only\s+)?verified.*changes', text, re.IGNORECASE) or
            re.search(r'restore.*attempt-owned', text, re.IGNORECASE)
        )
        if not has_preservation:
            raise AssertionError("Missing required attempt-owned restoration / user edit preservation clause")

        for line_no, line in enumerate(text.splitlines(), start=1):
            for pat in cls.DANGEROUS_PATTERNS:
                if re.search(pat, line, re.IGNORECASE):
                    if not cls.PROHIBITION_PATTERN.search(line):
                        raise AssertionError(
                            f"Line {line_no} contains whole-tree instruction without explicit prohibition wording: {line.strip()!r}"
                        )

    def test_debugging_docs_forbid_whole_tree_checkout(self):
        for rel in self.DEBUGGING_PATHS:
            full_path = ROOT / rel
            self.assertTrue(full_path.is_file(), f"Debugging doc missing: {rel}")
            self.check_debugging_doc(full_path)

    def test_affirmative_whole_tree_checkout_mutation_fails(self):
        bad_text = (
            "Restore only verified attempt-owned changes and preserve user edits.\n"
            "Run git checkout . to revert all changes.\n"
        )
        with self.assertRaises(AssertionError) as ctx:
            self.check_debugging_doc(bad_text)
        self.assertIn("whole-tree instruction without explicit prohibition wording", str(ctx.exception))

    def test_missing_preservation_clause_mutation_fails(self):
        bad_text = "Whole-tree checkout is forbidden, but no attempt-owned restoration mentioned.\n"
        with self.assertRaises(AssertionError) as ctx:
            self.check_debugging_doc(bad_text)
        self.assertIn("Missing required attempt-owned restoration", str(ctx.exception))


if __name__ == '__main__':
    unittest.main()
