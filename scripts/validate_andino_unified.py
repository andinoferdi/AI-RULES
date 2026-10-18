"""Check source-derived integration coverage and one-owner decisions.

Structural checks are deliberately separate from procedural and live host evidence.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'docs/validation/andino-unified'
REQUIRED = ('source_id upstream source_path original_skill_name source_status source_sha256 '
            'snapshot_commit_or_tree snapshot_tree snapshot_dirty_fingerprint purpose_and_trigger '
            'unique_techniques dependencies_and_host_assumptions potential_conflicts disposition '
            'rationale license_notice_references verification_state').split()
OWNER_FIELDS = ('concern authoritative_owner supporting_techniques precedence activation non_trigger '
                'permitted_side_effects permission_gate fallback evidence negative_test_ids').split()
STATUSES = {'stable', 'misc', 'in-progress', 'deprecated', 'meta', 'setup'}
DISPOSITIONS = {'ADAPT', 'MERGE', 'INTERNALIZE', 'CONDITIONAL', 'EXCLUDE', 'DEFER'}


def validate_coverage(document, runtime_files=None, source_paths=None):
    rows = document.get('rows') if isinstance(document, dict) else None
    if not isinstance(rows, list) or not rows:
        return ['coverage: nonempty source-derived rows required']
    errors, seen, seen_paths, accounted = [], set(), set(), {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f'row {index}: object required')
            continue
        identity = row.get('source_id', f'row {index}')
        if identity in seen:
            errors.append(f'{identity}: duplicate source identity')
        seen.add(identity)
        source_key = (row.get('upstream'), row.get('source_path'))
        if source_key in seen_paths:
            errors.append(f'{identity}: duplicate upstream/source path')
        seen_paths.add(source_key)
        for field in REQUIRED:
            if not row.get(field):
                errors.append(f'{identity}: missing {field}')
        if row.get('source_status') not in STATUSES:
            errors.append(f'{identity}: invalid source status')
        if row.get('disposition') not in DISPOSITIONS:
            errors.append(f'{identity}: invalid disposition')
        if not re.fullmatch(r'[0-9a-f]{64}', row.get('source_sha256', '')):
            errors.append(f'{identity}: invalid source hash')
        eligible = row.get('source_status') in ('stable', 'misc')
        methods = row.get('andino_method_ids_and_paths', [])
        if eligible and (not methods or row.get('disposition') in ('EXCLUDE', 'DEFER')):
            errors.append(f'{identity}: eligible source has no implemented destination')
        if not isinstance(methods, list):
            errors.append(f'{identity}: method array required')
            methods = []
        for method in methods:
            if not isinstance(method, dict):
                errors.append(f'{identity}: invalid method object')
                continue
            method_id = method.get('id', '')
            path = method.get('path', '')
            expected = 'SKILL.md' if method_id == 'root-contract' else f'skills/{method_id}/GUIDE.md'
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', method_id) or path != expected:
                errors.append(f'{identity}: unsafe or inconsistent method path: {path}')
            if runtime_files is not None and path not in runtime_files:
                errors.append(f'{identity}: missing method {path}')
        if eligible and not row.get('test_ids'):
            errors.append(f'{identity}: eligible source lacks verification mapping')
        if row.get('source_path', '').endswith('/SKILL.md'):
            accounted.setdefault(row.get('upstream'), set()).add(row['source_path'])
    if source_paths is not None:
        for upstream in set(source_paths) | set(accounted):
            expected, actual = set(source_paths.get(upstream, set())), accounted.get(upstream, set())
            errors.extend(f'{upstream}: unaccounted source {p}' for p in sorted(expected - actual))
            errors.extend(f'{upstream}: stale source {p}' for p in sorted(actual - expected))
    return errors


def validate_ownership(document):
    concerns = document.get('concerns') if isinstance(document, dict) else None
    if not isinstance(concerns, list) or not concerns:
        return ['ownership: nonempty concern matrix required']
    errors, seen = [], set()
    for row in concerns:
        if not isinstance(row, dict):
            errors.append('ownership: concern object required')
            continue
        concern = row.get('concern')
        if concern in seen:
            errors.append(f'{concern}: duplicate authoritative concern/owner')
        seen.add(concern)
        for field in OWNER_FIELDS:
            if not row.get(field):
                errors.append(f'{concern}: missing {field}')
        if row.get('unresolved_issue'):
            errors.append(f'{concern}: unresolved ownership collision')
    return errors


def source_roots(audit_dir):
    roots = {}
    for path in sorted(audit_dir.glob('*-audit.json')):
        audit = json.loads(path.read_text(encoding='utf-8'))
        snapshot = audit['snapshot']
        roots[audit.get('upstream', audit.get('source'))] = Path(
            snapshot.get('local_path', snapshot.get('root', snapshot.get('path'))))
    return roots


def validate_method_evidence(methods, reports, hashes, input_hashes=None):
    errors, metadata, records = [], {}, {}
    for method in methods:
        identity = method['id']
        if identity in metadata:
            errors.append(f'{identity}: duplicate method metadata')
        metadata[identity] = method
        positive = method.get('activation', {}).get('positive', {}).get('request') or method.get('positive_requests')
        negative = method.get('activation', {}).get('negative', {}).get('request') or method.get('negative_requests')
        if not positive or not negative or positive == negative:
            errors.append(f'{identity}: distinct positive/non-trigger fixtures required')
    actual = {p.split('/')[1] for p in hashes if re.fullmatch(r'skills/[^/]+/GUIDE.md', p)}
    if actual != set(metadata):
        errors.append('method metadata and actual GUIDE.md set differ')
    for report in reports:
        if input_hashes is not None:
            inputs = report.get('inputs', {})
            family = report.get('source_family')
            required = {f'scripts/check_andino_{family}_methods.py',
                        f'docs/validation/andino-unified/{family}-methods.json'}
            if (family not in {'addy', 'matt', 'superpowers'} or not required <= inputs.keys()
                    or any(input_hashes.get(path) != digest for path, digest in inputs.items())):
                errors.append('procedural report: stale or missing checker/manifest input identity')
        for record in report.get('methods', report.get('records', [])):
            identity = record.get('id', record.get('method'))
            if identity in records:
                errors.append(f'{identity}: duplicate procedural evidence')
            records[identity] = record
    for identity, method in metadata.items():
        record = records.get(identity, {})
        digest = hashlib.sha256(json.dumps(method, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        if record.get('metadata_sha256') != digest:
            errors.append(f'{identity}: stale or missing operational metadata identity')
        if record.get('status') != 'PASS' or not (record.get('observed') or record.get('default')):
            errors.append(f'{identity}: missing passing observed procedure')
        evidence_hashes = dict(record.get('source_hashes', record.get('resource_sha256', {})))
        guide = f'skills/{identity}/GUIDE.md'
        if record.get('guide_sha256'):
            evidence_hashes[guide] = record['guide_sha256']
        for path in [guide, *method.get('resources', [])]:
            if path not in hashes or evidence_hashes.get(path) != hashes[path]:
                errors.append(f'{identity}: stale or missing procedural byte evidence for {path}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit-dir', type=Path, default=AUDIT)
    parser.add_argument('--runtime', type=Path)
    parser.add_argument('--check-sources', action='store_true')
    args = parser.parse_args()
    document = json.loads((args.audit_dir / 'coverage.json').read_text(encoding='utf-8'))
    ownership = json.loads((args.audit_dir / 'ownership.json').read_text(encoding='utf-8'))
    files = None
    if args.runtime:
        from validate_skills import directory_files, package_files
        files, modes = directory_files(args.runtime)
        errors = package_files(files, 'andino-workflow', modes)
        methods = [m for p in sorted(args.audit_dir.glob('*-methods.json'))
                   for m in json.loads(p.read_text(encoding='utf-8'))]
        reports = [json.loads(p.read_text(encoding='utf-8')) for p in sorted(args.audit_dir.glob('*-operational.json'))]
        hashes = {name: hashlib.sha256((args.runtime/name).read_bytes()).hexdigest()
                  for name in files if (args.runtime/name).is_file()}
        input_paths = [*args.audit_dir.glob('*-methods.json'),
                       *ROOT.glob('scripts/check_andino_*_methods.py')]
        input_hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in input_paths}
        errors += validate_method_evidence(methods, reports, hashes, input_hashes)
        resources = json.loads((args.audit_dir/'resource-map.json').read_text(encoding='utf-8'))['resources']
        for row in document['rows']:
            for asset in row['essential_assets']:
                destinations = [r for r in resources if r['upstream'] == row['upstream'] and r['source_path'] == asset]
                if not destinations or any(not r.get('rationale') or
                                           r.get('disposition') != 'EXCLUDE' and r.get('runtime_path') not in files
                                           for r in destinations):
                    errors.append(f"{row['source_id']}: unresolved resource disposition {asset}")
    else:
        errors = []
    source_paths = None
    if args.check_sources:
        roots = source_roots(args.audit_dir)
        source_paths = {name: {p.relative_to(root).as_posix() for p in root.rglob('SKILL.md')
                               if '.git' not in p.relative_to(root).parts}
                        for name, root in roots.items()}
        for row in document['rows']:
            path = roots[row['upstream']] / row['source_path']
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row['source_sha256']:
                errors.append(f"{row['source_id']}: source bytes drift or missing")
    errors += validate_coverage(document, files, source_paths) + validate_ownership(ownership)
    summary = dict(result='FAIL' if errors else 'PASS', evidence_class='STRUCTURAL VERIFIED',
                   rows=len(document['rows']), categories=dict(Counter(r['source_status'] for r in document['rows'])),
                   method_destinations=len({m['id'] for r in document['rows'] for m in r['andino_method_ids_and_paths']}),
                   unresolved_collisions=sum(bool(r.get('unresolved_issue')) for r in ownership['concerns']),
                   errors=errors, limitation='Does not prove method operation or live host routing.')
    print(json.dumps(summary, indent=2))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
