import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_skripsi_live import audit


class LiveEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.cases = [{'id':'A','kind':'behavior'}]
        self.reviews = {'A':{'verdict':'PASS','reason':'Reviewed against actual oracle'}}
        self.records = {'A':{'case':'A','runtime_revision':'abc','oracle_hidden':True,
            'execution_status':'EXECUTED','observed_output':'Observed answer',
            'tool_actions':[{'command':'Get-Content SKILL.md','exit_code':0}]}}

    def test_successful_process_alone_is_not_behavior_proof(self):
        self.assertTrue(audit(self.cases, {}, self.records))

    def test_pass_requires_successful_skill_read(self):
        self.records['A']['tool_actions'][0]['exit_code'] = 1
        self.assertTrue(audit(self.cases, self.reviews, self.records))

    def test_negative_trigger_can_correctly_avoid_skill_read(self):
        self.cases[0]['kind'] = 'negative-trigger'
        self.records['A']['tool_actions'] = []
        self.assertEqual(audit(self.cases, self.reviews, self.records), [])

    def test_unavailable_execution_cannot_pass(self):
        self.records['A']['execution_status'] = 'ENVIRONMENT_UNAVAILABLE'
        self.assertTrue(audit(self.cases, self.reviews, self.records))

    def test_missing_case_fails_closed(self):
        self.cases.append({'id':'B','kind':'behavior'})
        self.assertTrue(audit(self.cases, self.reviews, self.records))

    def test_explicit_unverified_remains_honest(self):
        self.reviews['A']['verdict'] = 'NOT_VERIFIED'
        self.records['A']['tool_actions'] = []
        self.assertEqual(audit(self.cases, self.reviews, self.records), [])
