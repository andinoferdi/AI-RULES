import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / 'evals/andino-workflow.json'
PREVIOUS_CASE_COUNT = 66
CRUD_UNCERTAIN_PROMPT = 'gunakan andino-workflow dan metode metode yang ada , disini tolong buatkan saya web crud , tapi saya bingung gimana'

NEW_CASE_IDS = [
    'crud-uncertain-id',
    'uncertain-website-en',
    'crud-technical-confusion-id',
    'explanation-repair-id',
    'crud-delegated-id',
    'crud-accepted-spec',
    'inventory-material-req',
    'minor-detail-default',
    'unknown-bug-id',
    'explicit-internal-method-id',
    'ui-accepted-direction',
    'code-quality-comments',
    'thesis-status-id',
    'explicit-exclusion-id',
    'resume-checkpoint-id',
    'completion-verify-id',
]
SCHEMA_KEYS = ['id', 'kind', 'mode', 'coverage', 'prompt', 'fixture', 'fixture_files', 'capabilities', 'expected', 'forbidden']
KINDS = {'behavior', 'negative-trigger'}
MODES = {'read-only', 'isolated-writable'}
COVERAGES = {'routing', 'application'}
CAPABILITY_IDS = {
    'brainstorming', 'decision-interview', 'idea-refine', 'debugging', 'tdd', 'verification',
    'decision-map', 'plain-language-repitch', 'learning-workspace', 'focus', 'search-first',
    'design-taste-frontend', 'impeccable', 'antislop', 'antislop-code', 'skripsi-skill',
    'council', 'native-capabilities', 'human-procedure',
}
METHOD_IDS = [
    'brainstorming', 'decision-interview', 'idea-refine', 'decision-map', 'plain-language-repitch',
    'learning-workspace', 'debugging', 'tdd', 'verification', 'search-first', 'design-taste-frontend',
    'impeccable', 'antislop', 'skripsi-skill',
]
EXPLICIT_CASE_IDS = {'explicit-internal-method-id', 'explicit-exclusion-id'}
METHOD_PATTERNS = {
    method: re.compile(r'\b' + re.escape(method) + r'\b', re.IGNORECASE)
    for method in METHOD_IDS
}


def model_visible_text(case):
    """Everything the evaluated agent receives: prompt, fixture line and fixture file names and contents."""
    parts = [case['prompt'], case['fixture']]
    for name, content in case['fixture_files'].items():
        parts.append(name)
        parts.append(content)
    return parts


class AndinoReadinessCasesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(CASES_PATH.read_text(encoding='utf-8'))
        cls.new_cases = cls.cases[PREVIOUS_CASE_COUNT:]
        cls.by_id = {case['id']: case for case in cls.cases}

    def test_total_count_is_previous_count_plus_new_cases(self):
        self.assertEqual(PREVIOUS_CASE_COUNT + len(NEW_CASE_IDS), len(self.cases))
        self.assertEqual(82, len(self.cases))

    def test_new_ids_are_present_exactly_once(self):
        counts = Counter(case['id'] for case in self.cases)
        for case_id in NEW_CASE_IDS:
            with self.subTest(case=case_id):
                self.assertEqual(1, counts[case_id])
        self.assertEqual([], [case_id for case_id, count in counts.items() if count > 1])

    def test_new_cases_are_appended_in_order(self):
        self.assertEqual(NEW_CASE_IDS, [case['id'] for case in self.new_cases])

    def test_schema_keys_are_present_in_order(self):
        for case in self.new_cases:
            with self.subTest(case=case['id']):
                self.assertEqual(SCHEMA_KEYS, list(case.keys()))

    def test_enumerated_fields_have_valid_values(self):
        for case in self.new_cases:
            with self.subTest(case=case['id']):
                self.assertIn(case['kind'], KINDS)
                self.assertIn(case['mode'], MODES)
                self.assertIn(case['coverage'], COVERAGES)
                self.assertIsInstance(case['capabilities'], list)
                self.assertTrue(case['expected'].strip())
                self.assertTrue(case['forbidden'].strip())

    def test_fixture_files_are_small_string_maps(self):
        for case in self.new_cases:
            files = case['fixture_files']
            with self.subTest(case=case['id']):
                self.assertIsInstance(files, dict)
                for name, content in files.items():
                    self.assertIsInstance(name, str)
                    self.assertIsInstance(content, str)
                    self.assertLess(len(content.splitlines()), 40, name)

    def test_capabilities_are_known_ids(self):
        for case in self.new_cases:
            with self.subTest(case=case['id']):
                self.assertTrue(set(case['capabilities']) <= CAPABILITY_IDS,
                                set(case['capabilities']) - CAPABILITY_IDS)

    def test_crud_uncertain_prompt_is_byte_exact(self):
        prompt = self.by_id['crud-uncertain-id']['prompt']
        self.assertEqual(CRUD_UNCERTAIN_PROMPT, prompt)
        self.assertEqual(CRUD_UNCERTAIN_PROMPT.encode('utf-8'), prompt.encode('utf-8'))

    def test_expected_and_forbidden_text_never_reaches_the_agent(self):
        for case in self.new_cases:
            for text in model_visible_text(case):
                with self.subTest(case=case['id']):
                    self.assertNotIn(case['expected'], text)
                    self.assertNotIn(case['forbidden'], text)

    def test_method_ids_are_hidden_from_agent_visible_input(self):
        for case in self.new_cases:
            if case['id'] in EXPLICIT_CASE_IDS:
                continue
            for text in model_visible_text(case):
                for method, pattern in METHOD_PATTERNS.items():
                    with self.subTest(case=case['id'], method=method):
                        self.assertIsNone(pattern.search(text), f'{method} leaked into {case["id"]}')

    def test_explicit_cases_name_only_their_own_method(self):
        self.assertIn('decision-map', self.by_id['explicit-internal-method-id']['prompt'])
        self.assertIn('impeccable', self.by_id['explicit-exclusion-id']['prompt'])

    def test_exact_prompts_match_the_readiness_contract(self):
        expected_prompts = {
            'uncertain-website-en': 'I want to build a website, but I don\'t know what kind.',
            'resume-checkpoint-id': 'lanjutkan',
        }
        for case_id, prompt in expected_prompts.items():
            with self.subTest(case=case_id):
                self.assertEqual(prompt, self.by_id[case_id]['prompt'])


if __name__ == '__main__':
    unittest.main()
