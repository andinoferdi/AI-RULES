import copy
import json
import hashlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_andino_unified import validate_coverage, validate_ownership, validate_method_evidence
from validate_skills import package_files
from validate_andino_capabilities import CAPABILITIES, SUPERPOWERS, AGENT_SKILLS, MCPS, FIELDS, validate_registry


class InternalRegistryTests(unittest.TestCase):
    def fixture(self):
        aliases = {'test-driven-development': 'tdd', 'agent-skills-test-driven-development': 'tdd',
                   'systematic-debugging': 'debugging', 'debugging-and-error-recovery': 'debugging',
                   'verification-before-completion': 'verification', 'brainstorming': 'decision-interview',
                   'interview-me': 'decision-interview', 'writing-plans': 'planning',
                   'planning-and-task-breakdown': 'planning', 'requesting-code-review': 'code-review',
                   'receiving-code-review': 'code-review', 'code-review-and-quality': 'code-review',
                   'dispatching-parallel-agents': 'delegation', 'using-git-worktrees': 'git-isolation',
                   'finishing-a-development-branch': 'delivery', 'spec-driven-development': 'specification'}
        blocks = []
        for identity in sorted(CAPABILITIES):
            values = dict.fromkeys(FIELDS, 'bounded current need')
            internal = identity in SUPERPOWERS | AGENT_SKILLS
            values['Type'] = 'method' if internal else 'MCP' if identity in MCPS else 'native' if identity == 'native-capabilities' else 'skill'
            values['Activation policy'] = 'CONDITIONAL_AUTO'
            if internal:
                values['Internal method'] = f"skills/{aliases.get(identity, identity)}/GUIDE.md"
            blocks.append('## ' + identity + '\n\n' + '\n'.join(f'- {k}: {v}' for k, v in values.items()) + '\n')
        return '\n'.join(blocks)

    def test_legacy_names_resolve_to_one_local_canonical_method(self):
        self.assertEqual([], validate_registry(self.fixture()))

    def test_wrong_alias_path_or_missing_method_cannot_pass(self):
        text = self.fixture().replace('skills/tdd/GUIDE.md', 'skills/other/GUIDE.md', 1)
        self.assertTrue(validate_registry(text))
        self.assertTrue(validate_registry(self.fixture().replace('- Internal method: skills/tdd/GUIDE.md\n', '', 1)))

    def test_sibling_cannot_be_retyped_as_internal_method(self):
        self.assertTrue(validate_registry(self.fixture().replace('## focus\n\n- Type: skill', '## focus\n\n- Type: method')))

    def test_legacy_registry_stays_revision_scoped_but_new_package_requires_methods(self):
        import re
        legacy = re.sub(r'^- Internal method: .*\n', '', self.fixture(), flags=re.M).replace('- Type: method', '- Type: skill')
        self.assertEqual([], validate_registry(legacy))
        self.assertTrue(validate_registry(legacy, require_internal=True))


class AndinoPackageTests(unittest.TestCase):
    def setUp(self):
        self.files = {
            'SKILL.md': '---\nname: andino-workflow\ndescription: Adaptive methods\n---\n[guide](skills/tdd/GUIDE.md)\n',
            'README.md': '# Installation\n',
            'skills/tdd/GUIDE.md': '# TDD\n[example](references/seams.md)\n',
            'skills/tdd/references/seams.md': '# Public seams\n',
        }

    def test_complete_internal_method_installs_as_one_native_identity(self):
        self.assertEqual([], package_files(self.files, 'andino-workflow'))

    def test_method_resource_policy_does_not_extend_other_skills(self):
        self.files['SKILL.md'] = self.files['SKILL.md'].replace('andino-workflow', 'focus')
        self.assertTrue(package_files(self.files, 'focus'))

    def test_unsafe_or_unneeded_files_are_rejected(self):
        for path in ('skills/tdd/SKILL.md', 'references/hidden/SKILL.md', 'skills/tdd/run.exe', 'skills/tdd/run.py',
                     'skills/../GUIDE.md', 'skills/tdd/references/C:escape.md',
                     'skills/tdd/references/CON.md', 'skills/tdd/references/.hidden.md',
                     'skills/tdd/references/trailing./x.md', '/skills/tdd/GUIDE.md'):
            with self.subTest(path=path):
                files = dict(self.files, **{path: 'untrusted'})
                self.assertTrue(package_files(files, 'andino-workflow'))

    def test_symlink_mode_and_broken_resource_are_rejected(self):
        modes = {'skills/tdd/references/seams.md': '120000'}
        self.assertTrue(package_files(self.files, 'andino-workflow', modes))
        del self.files['skills/tdd/references/seams.md']
        self.assertTrue(any('broken link' in e for e in package_files(self.files, 'andino-workflow')))

    def test_windows_aliases_and_nested_native_names_are_rejected(self):
        for extra in ({'references/skill.md': '# hidden identity'},
                      {'references/Foo.md': '# first', 'references/foo.md': '# collision'}):
            self.assertTrue(package_files(dict(self.files, **extra), 'andino-workflow'))

    def test_missing_image_resource_is_rejected(self):
        self.files['skills/tdd/GUIDE.md'] += '\n![example](resources/missing.png)\n'
        self.assertTrue(any('broken link' in e for e in package_files(self.files, 'andino-workflow')))


class CoverageGateTests(unittest.TestCase):
    def setUp(self):
        self.row = {
            'source_id': 'local:skills/test/SKILL.md', 'upstream': 'local',
            'source_path': 'skills/test/SKILL.md', 'original_skill_name': 'test',
            'source_status': 'stable', 'source_sha256': 'a' * 64,
            'snapshot_commit_or_tree': 'b' * 40, 'snapshot_tree': 'c' * 40,
            'snapshot_dirty_fingerprint': 'd' * 64, 'purpose_and_trigger': 'Check an observable result',
            'unique_techniques': ['literal expected public result'], 'essential_assets': [],
            'dependencies_and_host_assumptions': ['Python'], 'potential_conflicts': ['one plan'],
            'disposition': 'ADAPT', 'andino_method_ids_and_paths': [{'id': 'sample', 'path': 'skills/sample/GUIDE.md'}],
            'rationale': 'Preserve technique', 'license_notice_references': ['references/legal/local-license.md'],
            'test_ids': ['sample:positive|negative|operational'], 'verification_state': 'PLANNED',
        }
        self.document = {'rows': [self.row]}
        self.paths = {'local': {'skills/test/SKILL.md'}}

    def test_source_driven_inventory_accepts_exact_source_set(self):
        self.assertEqual([], validate_coverage(self.document, source_paths=self.paths))

    def test_omitted_source_cannot_silently_reduce_denominator(self):
        self.paths['local'].add('skills/forgotten/SKILL.md')
        self.assertTrue(any('unaccounted source' in e for e in validate_coverage(self.document, source_paths=self.paths)))

    def test_duplicate_identity_is_rejected(self):
        self.document['rows'].append(copy.deepcopy(self.row))
        self.assertTrue(any('duplicate' in e for e in validate_coverage(self.document)))

    def test_duplicate_source_path_cannot_hide_behind_another_identity(self):
        duplicate = dict(self.row, source_id='local:pretend-other-identity')
        self.document['rows'].append(duplicate)
        self.assertTrue(validate_coverage(self.document, source_paths=self.paths))

    def test_excluding_stable_item_does_not_count_as_coverage(self):
        self.row['disposition'] = 'EXCLUDE'
        self.assertTrue(any('eligible' in e for e in validate_coverage(self.document)))

    def test_runtime_missing_mapped_procedure_is_rejected(self):
        self.assertTrue(any('missing method' in e for e in validate_coverage(self.document, runtime_files={})))

    def test_runtime_path_escape_is_rejected(self):
        self.row['andino_method_ids_and_paths'][0]['path'] = '../outside/GUIDE.md'
        self.assertTrue(any('path' in e for e in validate_coverage(self.document)))

    def test_invalid_or_empty_rows_cannot_pass(self):
        for value in ({}, {'rows': []}, {'rows': [None]}):
            with self.subTest(value=value):
                self.assertTrue(validate_coverage(value))


class OwnershipGateTests(unittest.TestCase):
    def setUp(self):
        self.concern = {
            'concern': 'planning', 'authoritative_owner': 'andino-workflow',
            'supporting_techniques': ['planning'], 'activation': 'dependent task',
            'precedence': 'host and user scope, accepted contracts, Andino, local method',
            'non_trigger': 'simple fact', 'permitted_side_effects': 'one plan',
            'permission_gate': 'task scope', 'fallback': 'local draft',
            'evidence': 'decision.md', 'negative_test_ids': ['single-plan'], 'unresolved_issue': None,
        }

    def test_unresolved_or_duplicate_operational_owner_blocks_acceptance(self):
        self.assertEqual([], validate_ownership({'concerns': [self.concern]}))
        duplicate = dict(self.concern, authoritative_owner='another-router')
        self.assertTrue(validate_ownership({'concerns': [self.concern, duplicate]}))
        self.concern['unresolved_issue'] = 'TDD conflict'
        self.assertTrue(validate_ownership({'concerns': [self.concern]}))

    def test_missing_negative_boundary_is_rejected(self):
        self.concern['negative_test_ids'] = []
        self.assertTrue(validate_ownership({'concerns': [self.concern]}))

    def test_precedence_is_required_for_each_concern(self):
        del self.concern['precedence']
        self.assertTrue(validate_ownership({'concerns': [self.concern]}))


class CurrentEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.methods = [{'id': 'sample', 'resources': [], 'positive_requests': ['Apply an executable contract'],
                         'negative_requests': ['Correct a spelling error']}]
        self.hashes = {'skills/sample/GUIDE.md': 'a' * 64}
        self.reports = [{'methods': [{'id': 'sample', 'status': 'PASS', 'guide_sha256': 'a' * 64,
                                      'resource_sha256': {}, 'observed': {'result': 15}}]}]
        self.reports[0]['methods'][0]['metadata_sha256'] = hashlib.sha256(
            json.dumps(self.methods[0], sort_keys=True, separators=(',', ':')).encode()).hexdigest()

    def test_current_procedure_and_distinct_trigger_pair_are_required(self):
        self.assertEqual([], validate_method_evidence(self.methods, self.reports, self.hashes))
        self.methods[0]['negative_requests'] = []
        self.assertTrue(validate_method_evidence(self.methods, self.reports, self.hashes))

    def test_stale_bytes_or_missing_operation_cannot_count_as_verified(self):
        self.hashes['skills/sample/GUIDE.md'] = 'b' * 64
        self.assertTrue(validate_method_evidence(self.methods, self.reports, self.hashes))
        self.assertTrue(validate_method_evidence(self.methods, [], self.hashes))

    def test_unmapped_or_duplicate_guide_is_rejected(self):
        self.hashes['skills/unreviewed/GUIDE.md'] = 'c' * 64
        self.assertTrue(validate_method_evidence(self.methods, self.reports, self.hashes))
        self.methods.append(copy.deepcopy(self.methods[0]))
        self.assertTrue(validate_method_evidence(self.methods, self.reports, self.hashes))

    def test_changed_operational_oracle_invalidates_old_evidence(self):
        self.methods[0]['operational'] = {'expected': 'changed contract'}
        self.assertTrue(validate_method_evidence(self.methods, self.reports, self.hashes))

    def test_stale_checker_or_manifest_invalidates_report(self):
        self.reports[0]['inputs'] = {'checker.py': 'a' * 64}
        self.assertTrue(validate_method_evidence(self.methods, self.reports, self.hashes,
                                               {'checker.py': 'b' * 64}))

    def test_partial_input_identity_cannot_omit_the_checker(self):
        manifest = 'docs/validation/andino-unified/addy-methods.json'
        self.reports[0].update(source_family='addy', inputs={manifest: 'a' * 64})
        self.assertTrue(validate_method_evidence(self.methods, self.reports, self.hashes,
                                               {manifest: 'a' * 64}))


class ExampleContainmentTests(unittest.TestCase):
    def test_path_mutations_outside_example_scope_are_blocked(self):
        import tempfile
        from check_andino_addy_methods import run_example
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'user.txt'
            for operation in ('chmod', 'truncate'):
                target.write_text('preserve me', encoding='utf-8')
                argument = '0o600' if operation == 'chmod' else '0'
                code = f'import os,json\nos.{operation}({str(target)!r}, {argument})\nprint(json.dumps(True))'
                self.assertFalse(run_example(code, False)['ok'])
                self.assertEqual('preserve me', target.read_text(encoding='utf-8'))
