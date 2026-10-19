"""Evolution contract regressions; procedure execution is checked separately."""
import sys
import unittest
import hashlib
import json
import subprocess
import tempfile
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_andino_capabilities import INTERNAL_METHODS
from build_andino_coverage import build_rows
from validate_andino_unified import validate_method_evidence
import check_andino_publication


class EvolutionContracts(unittest.TestCase):
    def test_brainstorming_is_exploration_not_requirements_interview(self):
        self.assertEqual('brainstorming', INTERNAL_METHODS['brainstorming'])

    def test_coverage_does_not_restore_obsolete_brainstorming_alias(self):
        audit = {
            'upstream': 'obra/superpowers',
            'snapshot': {'head': 'a' * 40, 'tree': 'b' * 40},
            'methods': [{
                'source_path': 'skills/brainstorming/SKILL.md',
                'original_name': 'brainstorming', 'source_status': 'stable',
                'canonical_methods': ['brainstorming', 'decision-interview'],
                'disposition': 'ADAPT',
            }],
        }
        rows = build_rows({'superpowers-audit.json': audit})
        self.assertEqual(['brainstorming', 'decision-interview'],
                         [m['id'] for m in rows[0]['andino_method_ids_and_paths']])


class CandidateEvidence(unittest.TestCase):
    def test_relative_candidate_audit_path_reports_instead_of_crashing(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(dir=root / 'docs/validation') as folder:
            audit = Path(folder)
            runtime = audit / 'runtime'
            runtime.mkdir()
            (runtime / 'SKILL.md').write_text('---\nname: andino-workflow\ndescription: Test\n---\n')
            (runtime / 'README.md').write_text('# Test\n')
            for name, value in {'coverage': {'rows': []}, 'ownership': {'concerns': []},
                                'resource-map': {'resources': []}, 'evolution-methods': []}.items():
                (audit / (name + '.json')).write_text(json.dumps(value))
            result = subprocess.run([sys.executable, '-B', str(root / 'scripts/validate_andino_unified.py'),
                '--audit-dir', str(audit.relative_to(root)), '--runtime', str(runtime)],
                cwd=root, capture_output=True, text=True)
            self.assertIn('"result": "FAIL"', result.stdout)
            self.assertNotIn('Traceback', result.stderr)

    def test_missing_source_snapshot_is_a_validation_error(self):
        with tempfile.TemporaryDirectory() as folder:
            audit = Path(folder)
            (audit / 'coverage.json').write_text(json.dumps({'rows': [
                {'upstream': 'missing', 'source_path': 'skills/one/SKILL.md',
                 'source_status': 'stable', 'andino_method_ids_and_paths': []}]}))
            (audit / 'ownership.json').write_text(json.dumps({'concerns': []}))
            result = subprocess.run([sys.executable, '-B', str(
                Path(__file__).resolve().parents[1] / 'scripts/validate_andino_unified.py'),
                '--audit-dir', folder, '--check-sources'], capture_output=True, text=True)
            self.assertEqual(1, result.returncode)
            self.assertIn('source snapshot missing', result.stdout)
            self.assertNotIn('Traceback', result.stderr)

    def test_candidate_manifest_identity_and_byte_drift(self):
        method = {'id': 'sample', 'resources': [],
                  'positive_requests': ['Explore possible directions'],
                  'negative_requests': ['Implement the accepted spec']}
        manifest = 'docs/validation/andino-unified/evolution-methods.json'
        checker = 'scripts/check_andino_evolution_methods.py'
        inputs = {manifest: 'b' * 64, checker: 'c' * 64}
        hashes = {'skills/sample/GUIDE.md': 'a' * 64}
        record = {'id': 'sample', 'status': 'PASS', 'observed': {'result': 1},
                  'guide_sha256': 'a' * 64,
                  'metadata_sha256': hashlib.sha256(json.dumps(
                      method, sort_keys=True, separators=(',', ':')).encode()).hexdigest()}
        report = {'source_family': 'evolution', 'inputs': inputs.copy(), 'records': [record]}
        check = lambda: validate_method_evidence([method], [report], hashes, inputs)
        self.assertEqual([], check())
        hashes['skills/sample/GUIDE.md'] = 'd' * 64
        self.assertTrue(check())
        hashes['skills/sample/GUIDE.md'] = 'a' * 64
        report['inputs'] = {checker: 'c' * 64,
                            'docs/validation/andino-evolution/evolution-methods.json': 'b' * 64}
        self.assertTrue(check())
        candidate_inputs = report['inputs'].copy()
        self.assertEqual([], validate_method_evidence(
            [method], [report], hashes, candidate_inputs,
            manifest_prefix='docs/validation/andino-evolution'))
        report['source_family'] = 'unreviewed'
        self.assertTrue(validate_method_evidence(
            [method], [report], hashes, candidate_inputs,
            manifest_prefix='docs/validation/andino-evolution'))


class PublicationEvidence(unittest.TestCase):
    def test_publication_check_uses_selected_prior_release_without_overwriting_history(self):
        class StopBeforeNetwork(Exception):
            pass
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            release = root / 'src/ai_rules/release/data'
            release.mkdir(parents=True)
            (release / 'release_manifest.json').write_text(json.dumps(
                {'first_party': {'andino-workflow': {'commit': 'new-runtime'}}}))
            legacy = root / 'docs/validation/andino-unified'
            (legacy / 'pre-publication').mkdir(parents=True)
            (legacy / 'publication-lineage.json').write_text(json.dumps({'to_runtime_hash': 'hash'}))
            (legacy / 'pre-publication/release_manifest.json').write_text(json.dumps(
                {'first_party': {'andino-workflow': {'commit': 'legacy-prior'}}}))
            selected = root / 'candidate'
            selected.mkdir()
            (selected / 'publication-lineage.json').write_text(json.dumps({'to_runtime_hash': 'hash'}))
            prior = selected / 'previous-release-manifest.json'
            prior.write_text(json.dumps({'first_party': {'andino-workflow': {'commit': 'selected-prior'}}}))
            with patch.object(check_andino_publication, 'ROOT', root), \
                 patch.object(sys, 'argv', ['check', '--evidence-dir', str(selected), '--previous-manifest', str(prior)]), \
                 patch.object(check_andino_publication, 'export_git_ref', side_effect=StopBeforeNetwork) as export:
                with self.assertRaises(StopBeforeNetwork):
                    check_andino_publication.main()
            self.assertEqual('selected-prior', export.call_args.args[0])


if __name__ == '__main__':
    unittest.main()
