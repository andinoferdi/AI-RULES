import copy
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_andino_capabilities import validate_registry, validate_cases, validate_record, case_prompt, runtime_files, historical_hashes
from run_andino_capability_eval import skill_resource_hash, fixture_contents


class CapabilityValidationTest(unittest.TestCase):
    def test_registry_rejects_duplicate_and_incomplete_contract(self):
        text = '## context7\n- Type: MCP\n## context7\n- Type: skill\n'
        errors = validate_registry(text)
        self.assertTrue(any('duplicate' in e for e in errors))
        self.assertTrue(any('Invocation method' in e for e in errors))

    def test_cases_reject_unknown_capability_and_duplicate(self):
        case = dict(id='unknown', kind='behavior', prompt='p', expected='e', forbidden='f',
                    capabilities=['invented-tool'], fixture='raw fact')
        errors = validate_cases([case, copy.deepcopy(case)], {'context7'})
        self.assertTrue(any('unknown capability' in e for e in errors))
        self.assertTrue(any('duplicate' in e for e in errors))

    def test_actor_input_hides_oracle(self):
        case = dict(id='case', prompt='Read evidence', fixture='Raw evidence',
                    expected='SECRET_EXPECTED', forbidden='SECRET_FORBIDDEN',
                    capabilities=['context7'])
        result = case_prompt(case, 'Runtime metadata', 'Catalog metadata')
        self.assertIn('Raw evidence', result)
        self.assertNotIn('SECRET_', result)
        self.assertNotIn('context7', result)

    def test_pass_requires_reviewer_and_observed_evidence(self):
        record = dict(case='case', scope='behavioral', host='Codex', model='UNKNOWN',
                      runtime_hash='a' * 64, discovered=[], selected=[], invocations=[],
                      fallback=[], resulting_evidence='', verdict='PASS')
        errors = validate_record(record)
        self.assertTrue(any('review' in e for e in errors))
        self.assertTrue(any('evidence' in e for e in errors))

    def test_smoke_pass_cannot_claim_behavioral_case(self):
        record = dict(case='case', scope='smoke', host='Codex', model='UNKNOWN',
                      runtime_hash='a' * 64, discovered=[], selected=[], invocations=[],
                      fallback=[], resulting_evidence='Transport responded', verdict='PASS',
                      review={'reason':'Connected', 'reviewer':'human'}, routing_verified=True)
        self.assertTrue(any('routing' in e for e in validate_record(record)))

    def test_not_verified_record_is_valid_without_fake_provider(self):
        record = dict(case='case', scope='behavioral', host='Codex', model='UNKNOWN',
                      runtime_hash='a' * 64, discovered=[], selected=[], invocations=[],
                      fallback=[], resulting_evidence='', verdict='NOT_VERIFIED')
        self.assertEqual(validate_record(record), [])

    def test_external_skill_csv_is_hashable_but_not_andino_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'SKILL.md').write_text('Skill',encoding='utf-8')
            (root/'data.csv').write_text('id,value\n1,x\n',encoding='utf-8')
            initial=skill_resource_hash(root)
            self.assertEqual(len(initial),64)
            (root/'data.csv').write_text('id,value\n1,y\n',encoding='utf-8')
            self.assertNotEqual(skill_resource_hash(root),initial)
            with self.assertRaisesRegex(ValueError,'Unexpected runtime'):
                runtime_files(root)

    def test_historical_lineage_cannot_accept_unrelated_current_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            destination=root/'docs/validation/andino-workflow'
            destination.mkdir(parents=True)
            (destination/'capability-runtime-lineage.json').write_text('{"current_runtime_hash":"known","historical_hashes":["older"]}',encoding='utf-8')
            with patch('validate_andino_capabilities.ROOT',root):
                self.assertEqual(historical_hashes('known',False),set())
                self.assertEqual(historical_hashes('known',True),{'older'})
                with self.assertRaisesRegex(ValueError,'Lineage'):
                    historical_hashes('unrelated',True)

    def test_fixture_overrides_do_not_mix_database_and_library_diagnoses(self):
        self.assertIn('column absent',fixture_contents('debugging-superpowers-route')['runtime.log'])
        self.assertIn('is not a function',fixture_contents('capability-rerouting')['runtime.log'])
        self.assertIn('no execution authorized',fixture_contents('cheatengine-permission')['proposal.txt'])


if __name__ == '__main__':
    unittest.main()
