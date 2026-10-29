"""Offline dispatch contracts; these checks do not execute or grade an AI actor."""
import os
import re
import subprocess
import sys
import unittest
import copy
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_andino_reliability as checker


def runtime_text(path):
    directory = os.environ.get('ANDINO_RUNTIME_DIR')
    if directory:
        target = Path(directory) / path
        return target.read_text(encoding='utf-8') if target.is_file() else ''
    result = subprocess.run(['git', 'show', 'andino-workflow:' + path], cwd=ROOT,
                            capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        return ''
    return result.stdout


class InternalDispatchContract(unittest.TestCase):
    def test_work_selection_precedes_communication(self):
        skill = runtime_text('SKILL.md')
        self.assertIn('## Select work methods first', skill)
        self.assertIn('## Communication support', skill)
        self.assertLess(skill.index('## Select work methods first'), skill.index('## Communication support'))
        self.assertIn('references/internal-method-index.md', skill)
        self.assertIn('references/method-dispatch.md', skill)
        self.assertNotIn('immediately after Focus', skill)

    def test_dispatch_applies_to_every_indexed_method_and_alias(self):
        contract = runtime_text('references/method-dispatch.md')
        for heading in ('Explicit requests', 'Implicit requests', 'Phase transitions', 'Evidence'):
            self.assertIn('## ' + heading, contract)
        for boundary in ('all internal methods', 'source-name aliases', 'quoted',
                         'required domain', 'native provider', 'UNAVAILABLE'):
            self.assertIn(boundary, contract)
        self.assertIn('before Focus', contract)
        self.assertIn('not a runtime router', contract)

    def test_accepted_plan_has_a_direct_execution_route(self):
        routing = runtime_text('references/routing.md')
        line = next((line for line in routing.splitlines()
                     if line.startswith('| Accepted plan ready')), '')
        self.assertIn('REQUIRED', line)
        self.assertIn('skills/plan-execution/GUIDE.md', line)

    def test_planning_handoff_does_not_grant_execution_authority(self):
        guide = runtime_text('skills/planning/GUIDE.md')
        self.assertIn('../plan-execution/GUIDE.md', guide)
        self.assertIn('execution is authorized', guide)

    def test_no_native_skill_expansion_or_missing_canonical_guide(self):
        index = runtime_text('references/internal-method-index.md').split('## Source-name compatibility')[0]
        ids = re.findall(r'\[([^]]+)\]\(\.\./skills/([^/]+)/GUIDE.md\)', index)
        self.assertEqual(59, len(ids))
        self.assertEqual(59, len({identity for identity, _ in ids}))
        for identity, directory in ids:
            self.assertEqual(identity, directory)
            self.assertTrue(runtime_text(f'skills/{identity}/GUIDE.md'), identity)
            self.assertFalse(runtime_text(f'skills/{identity}/SKILL.md'), identity)


class CatalogIntegrity(unittest.TestCase):
    def setUp(self):
        self.files = {'references/internal-method-index.md':
                      '| [planning](../skills/planning/GUIDE.md) | Accepted work | Simple edit |\n'
                      '## Source-name compatibility\n'
                      '| writing-plans | [planning](../skills/planning/GUIDE.md) |\n',
                      'skills/planning/GUIDE.md': '# Planning\n'}

    def test_alias_cannot_silently_resolve_to_an_absent_method(self):
        files = {'references/internal-method-index.md':
                 '| [planning](../skills/planning/GUIDE.md) | Accepted work | Simple edit |\n'
                 '## Source-name compatibility\n'
                 '| writing-plans | [missing](../skills/missing/GUIDE.md) |\n',
                 'skills/planning/GUIDE.md': '# Planning\n'}
        errors = checker.catalog_errors(files)
        self.assertTrue(any('missing' in error for error in errors), errors)

    def test_duplicate_canonical_and_alias_rows_are_rejected(self):
        self.files['references/internal-method-index.md'] = (
            self.files['references/internal-method-index.md'].splitlines()[0] + '\n' +
            self.files['references/internal-method-index.md'] +
            '| writing-plans | [planning](../skills/planning/GUIDE.md) |\n')
        errors = checker.catalog_errors(self.files)
        self.assertTrue(any('duplicate canonical' in e for e in errors))
        self.assertTrue(any('duplicate source alias' in e for e in errors))

    def test_registry_index_heading_does_not_hide_native_support_or_tools(self):
        self.files['references/capability-registry.md'] = (
            '# Registry\n\n## Index\n'
            '| [focus](#focus) | skill | AI-RULES | Communication |\n'
            '| [context7](#context7) | MCP | Upstash | Documentation |\n'
            '## focus\n- Type: skill\n')
        model = checker.catalog(self.files)
        self.assertIn('focus', model['siblings'])
        self.assertIn('context7', model['instruments'])

    def test_orphan_guide_and_alias_shadow_are_rejected(self):
        self.files['skills/tdd/GUIDE.md'] = '# TDD\n'
        self.files['references/internal-method-index.md'] += (
            '| planning | [tdd](../skills/tdd/GUIDE.md) |\n')
        errors = checker.catalog_errors(self.files)
        self.assertTrue(any('absent from index' in e for e in errors))
        self.assertTrue(any('shadows canonical' in e for e in errors))


class ManualCoverage(unittest.TestCase):
    def setUp(self):
        self.model = {'methods': {'planning': {'path': 'skills/planning/GUIDE.md'}},
                      'aliases': {'writing-plans': ['planning']}}
        self.cases = [dict(id='planning-' + variant, kind=('negative-trigger' if variant == 'negative' else 'behavior'),
                           prompt='Raw request', fixture='Raw fixture', expected='SECRET_ORACLE', forbidden='SECRET_FORBIDDEN',
                           capabilities=['planning'], variant=variant, method='planning')
                      for variant in ('explicit', 'implicit', 'negative')]
        self.cases.append(dict(self.cases[0], id='alias-writing-plans', variant='alias',
                               source_alias='writing-plans'))

    def test_positive_only_coverage_cannot_hide_missing_negative_or_alias(self):
        errors = checker.case_errors(self.cases[:2], self.model)
        self.assertTrue(any('negative' in e for e in errors), errors)
        self.assertTrue(any('writing-plans' in e for e in errors), errors)

    def test_multi_target_alias_needs_each_context_specific_destination(self):
        self.model['methods']['tdd'] = {'path': 'skills/tdd/GUIDE.md'}
        self.model['aliases']['writing-plans'].append('tdd')
        errors = checker.case_errors(self.cases, self.model)
        self.assertTrue(any('writing-plans' in e and 'tdd' in e for e in errors), errors)

    def test_actor_input_excludes_reviewer_expectations(self):
        text = checker.actor_input(self.cases[0], 'Candidate metadata')
        self.assertIn('Raw request', text)
        self.assertNotIn('SECRET_', text)

    def test_fixture_path_cannot_escape_a_manual_workspace(self):
        cases = copy.deepcopy(self.cases)
        cases[0]['fixture_files'] = {'../sentinel.txt': 'bad'}
        self.assertTrue(any('fixture' in e for e in checker.case_errors(cases, self.model)))

    def test_manual_export_preserves_existing_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'bundle'
            destination.mkdir()
            sentinel = destination / 'user.txt'
            sentinel.write_text('keep', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                checker.write_bundle(destination, {'SKILL.md': 'candidate'}, self.cases)
            self.assertEqual('keep', sentinel.read_text(encoding='utf-8'))

    def test_export_itself_rejects_escape_before_creating_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'bundle'
            cases = copy.deepcopy(self.cases)
            cases[0]['fixture_files'] = {'../sentinel.txt': 'bad'}
            with self.assertRaises(ValueError):
                checker.write_bundle(destination, {'SKILL.md': 'candidate'}, cases)
            self.assertFalse(destination.exists())
            self.assertFalse((Path(directory) / 'sentinel.txt').exists())

    def test_packet_separates_raw_actor_input_and_review_oracle(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'bundle'
            checker.write_bundle(destination, {'SKILL.md': 'candidate'}, self.cases)
            actor = (destination / 'workspaces/planning-explicit/prompt.txt').read_text(encoding='utf-8')
            oracle = (destination / 'reviewer/cases.json').read_text(encoding='utf-8')
            self.assertNotIn('SECRET_', actor)
            self.assertIn('SECRET_ORACLE', oracle)
            self.assertIn((destination / 'andino-workflow/SKILL.md').as_posix(), actor)

    def test_relative_destination_embeds_absolute_candidate_path(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'bundle'
            relative = Path(os.path.relpath(destination))
            checker.write_bundle(relative, {'SKILL.md': 'candidate'}, self.cases)
            actor = (destination / 'workspaces/planning-explicit/prompt.txt').read_text(encoding='utf-8')
            self.assertIn((destination.resolve() / 'andino-workflow/SKILL.md').as_posix(), actor)

    def test_exported_result_round_trips_through_existing_evidence_contract(self):
        from validate_andino_capabilities import validate_record
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'bundle'
            checker.write_bundle(destination, {'SKILL.md': 'candidate'}, self.cases)
            path = destination / 'reviewer/result-template.json'
            record = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual([], validate_record(record))
            record.update(case='planning-explicit', verdict='PASS', reason=None,
                          execution_status='EXECUTED', resulting_evidence='Recorded plan artifact',
                          review={'reviewer': 'human', 'reason': 'Inspected actual trace and artifact'},
                          invocations=[{'name': 'Read', 'path': 'skills/planning/GUIDE.md'}])
            self.assertEqual([], validate_record(record))
            path.write_text(json.dumps(record), encoding='utf-8')
            evidence = checker.evidence_map(self.model, self.cases, [path.parent], record['runtime_hash'])
            self.assertEqual(1, len(evidence['planning']['archived_guide_references']))

    def test_archived_path_reference_never_becomes_candidate_behavior_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'record.json'
            path.write_text(json.dumps(dict(case='old', host='Codex', runtime_hash='a' * 64,
                verdict='PASS', coverage='routing', invocations=[dict(name='Read',
                    path='skills/planning/GUIDE.md', error='denied')])), encoding='utf-8')
            evidence = checker.evidence_map(self.model, self.cases, [Path(directory)], 'a' * 64)['planning']
            self.assertEqual('NOT_VERIFIED', evidence['candidate_model_behavior'])
            self.assertEqual('GUIDE_PATH_REFERENCE_NOT_USE_PROOF',
                             evidence['archived_guide_references'][0]['evidence_class'])


class CandidateCoverage(unittest.TestCase):
    def test_complete_case_collection_and_application_fixtures(self):
        cases = json.loads((ROOT / 'evals/andino-method-routing.json').read_text(encoding='utf-8'))
        # Definition coverage is structural, not evidence of a model following it.
        methods = {case['method'] for case in cases}
        self.assertEqual(59, len(methods))
        for identity in methods:
            self.assertTrue({'explicit', 'implicit', 'negative'} <=
                            {case['variant'] for case in cases if case['method'] == identity}, identity)
        applications = [case for case in cases if case['coverage'] == 'application']
        self.assertEqual(2, len(applications))
        self.assertTrue(all(case['mode'] == 'isolated-writable' and case['fixture_files']
                            for case in applications))


if __name__ == '__main__':
    unittest.main()
