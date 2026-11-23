import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from import_skripsi_evals import parse_cases
from validate_skripsi_traceability import audit
from run_skripsi_smoke import make_prompt, runtime_names, codex_command


class CodexCommandTest(unittest.TestCase):
    def test_config_overrides_follow_isolation_flags(self):
        command = codex_command('codex', Path('/tmp/base'), Path('/tmp/base/answer.txt'),
                                ['windows.sandbox="elevated"'])
        self.assertIn('--ignore-user-config', command)
        self.assertEqual(command[command.index('-c') + 1], 'windows.sandbox="elevated"')
        self.assertEqual(command[command.index('--sandbox') + 1], 'read-only')
        self.assertEqual(command[-1], '-')

    def test_no_overrides_keeps_original_command(self):
        command = codex_command('codex', Path('/tmp/base'), Path('/tmp/base/answer.txt'), [])
        self.assertNotIn('-c', command)


class RuntimeLayoutTest(unittest.TestCase):
    def test_subdir_strips_prefix_and_ignores_other_files(self):
        names = ['README.md', 'skills/skripsi-skill/SKILL.md', 'skills/skripsi-skill/references/a.md',
                 'skills/skripsi-skill-extra/SKILL.md']
        self.assertEqual(runtime_names(names, 'skills/skripsi-skill'),
                         [('skills/skripsi-skill/SKILL.md', 'SKILL.md'),
                          ('skills/skripsi-skill/references/a.md', 'references/a.md')])

    def test_no_subdir_keeps_branch_layout(self):
        self.assertEqual(runtime_names(['SKILL.md', 'references/a.md'], ''),
                         [('SKILL.md', 'SKILL.md'), ('references/a.md', 'references/a.md')])


class SRSImportTest(unittest.TestCase):
    def test_live_actor_does_not_receive_oracle(self):
        case={'prompt':'Actual user request','expected':'SECRET_EXPECTED_SENTINEL','forbidden':'SECRET_FORBIDDEN_SENTINEL'}
        prompt=make_prompt(case,'Synthetic raw context')
        self.assertIn('Actual user request',prompt)
        self.assertIn('Synthetic raw context',prompt)
        self.assertNotIn('SECRET_EXPECTED_SENTINEL',prompt)
        self.assertNotIn('SECRET_FORBIDDEN_SENTINEL',prompt)

    def source(self):
        return 'AO. INITIAL EVALUATION CASES\n'+'\n'.join(
            f'Case {n} — Example {n}\nPrompt:\nRequest {n}\nExpected:\nExpected {n}\nForbidden:\nForbidden {n}\n----------\n'
            for n in range(1,111))+'AP. FUTURE EXPANSION MODEL'

    def test_preserves_case_content_and_negative_trigger(self):
        cases=parse_cases(self.source())
        self.assertEqual(cases[9]['kind'],'negative-trigger')
        self.assertEqual(cases[-1]['forbidden'],'Forbidden 110')

    def test_missing_oracle_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_cases(self.source().replace('Forbidden:\nForbidden 55','Missing oracle'))

    def test_missing_case_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_cases(self.source().replace('Case 55 —','Scenario 55 —'))


class TraceabilityTest(unittest.TestCase):
    def setUp(self):
        self.report=json.loads((ROOT/'docs/validation/skripsi-skill/traceability.json').read_text(encoding='utf-8'))
        rows=self.report['requirements']+self.report['capabilities']+self.report['evals']
        self.runtime={r['implementation']['path'] for r in rows if r['implementation']['branch']=='skripsi-skill'}
        self.main={r['implementation']['path'] for r in rows if r['implementation']['branch']=='main'}
        self.cases={c['id'] for c in json.loads((ROOT/'evals/skripsi-skill.json').read_text(encoding='utf-8'))}

    def check(self,report=None):
        return audit(report or self.report,self.runtime,self.main,self.cases)

    def test_complete_ownership_inventory(self):
        self.assertEqual(self.check(),[])

    def test_missing_requirement_is_not_hidden_by_duplicate(self):
        self.report['requirements'][0]=copy.deepcopy(self.report['requirements'][1])
        self.assertTrue(self.check())

    def test_uncreated_owner_rejected(self):
        self.report['requirements'][0]['implementation']['path']='references/nonexistent.md'
        self.assertTrue(self.check())

    def test_behavioral_pass_requires_execution_evidence(self):
        self.report['requirements'][0]['behavioral_verdict']='PASS'
        self.assertTrue(self.check())

    def test_missing_eval_rejected(self):
        self.cases.remove('EVAL-110')
        self.assertTrue(self.check())

    def test_pending_final_task_status_rejected(self):
        self.report['tasks'][0]['status']='IMPLEMENTED_REVIEW_PENDING'
        self.assertTrue(self.check())

    def test_not_verified_task_requires_evidence(self):
        self.report['tasks'][0]['status']='NOT_VERIFIED'
        self.report['tasks'][0]['evidence']=''
        self.assertTrue(self.check())


if __name__=='__main__':
    unittest.main()
