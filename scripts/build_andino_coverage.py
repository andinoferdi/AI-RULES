"""Normalize reviewed local-source audit decisions into a many-to-many matrix.

This quality-plane tool does not implement runtime routing or grant permissions.
"""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'docs/validation/andino-unified'
ALIASES = {
    'test-driven-development': 'tdd', 'agent-skills-test-driven-development': 'tdd',
    'systematic-debugging': 'debugging', 'parallel-delegation': 'delegation',
    'requirements-discovery': 'decision-interview', 'routing': 'root-contract',
    'repository-workflow-configuration': 'project-configuration',
}


def build_rows(audits):
    rows = []
    for filename, audit in audits.items():
        upstream = audit.get('upstream', audit.get('source'))
        snapshot = audit['snapshot']
        sources = audit.get('methods', audit.get('skills', audit.get('items', [])))
        for source in sources:
            path = source['source_path']
            name = source.get('original_name', source.get('name', source.get('source_id')))
            status = source.get('source_status', source.get('status'))
            category = source.get('category', '')
            if status in ('active', 'stable'):
                status = 'stable'
            elif status == 'active-meta':
                status = 'meta'
            elif category in ('misc', 'in-progress', 'deprecated'):
                status = category
            elif 'deprecated' in str(status) or not path.endswith('/SKILL.md'):
                status = 'deprecated'
            elif status not in ('meta', 'setup', 'misc', 'in-progress'):
                status = 'setup' if 'setup' in str(status) else 'in-progress'
            methods = source.get('canonical_methods', source.get('method_ids',
                        [source['andino_method_id']] if source.get('andino_method_id') else []))
            methods = list(dict.fromkeys(ALIASES.get(m, m) for m in methods))
            disposition = source['disposition'].upper()
            disposition = {'ADAPT-CONDITIONAL': 'CONDITIONAL', 'INTEGRATE': 'ADAPT',
                           'COMPOSE': 'MERGE', 'ABSORB': 'INTERNALIZE',
                           'EXCLUDE-LIFECYCLE': 'EXCLUDE'}.get(disposition, disposition)
            if status == 'misc' or status == 'in-progress' and disposition != 'EXCLUDE':
                disposition = 'CONDITIONAL'
            if name == 'using-agent-skills':
                methods = ['root-contract']
                status, disposition = 'meta', 'INTERNALIZE'
            if name == 'chief-of-staff':
                methods = ['environment-retrospective', 'implementation']
                disposition = 'CONDITIONAL'
            if status == 'deprecated':
                methods, disposition = [], 'EXCLUDE'
            rows.append({
                'source_id': f'{upstream}:{path}', 'upstream': upstream,
                'snapshot_commit_or_tree': snapshot.get('head', snapshot.get('commit')),
                'snapshot_tree': snapshot['tree'],
                'snapshot_dirty_fingerprint': snapshot.get('content_fingerprint_sha256', snapshot.get('disk_manifest_sha256')),
                'source_path': path, 'original_skill_name': name, 'source_status': status,
                'source_sha256': source.get('source_sha256', source.get('sha256')),
                'purpose_and_trigger': source.get('purpose_and_trigger', source.get('techniques', source.get('unique_techniques'))),
                'unique_techniques': source.get('unique_techniques', source.get('techniques')),
                'essential_assets': source.get('essential_resource_paths', source.get('essential_resources', source.get('resources', []))),
                'dependencies_and_host_assumptions': source.get('dependencies_and_host_assumptions', source.get('dependency_host_assumptions', source.get('adaptation'))),
                'potential_conflicts': source.get('conflicts_and_adaptation', source.get('adaptation')),
                'disposition': disposition,
                'andino_method_ids_and_paths': [{'id': m, 'path': 'SKILL.md' if m == 'root-contract' else f'skills/{m}/GUIDE.md'} for m in methods],
                'rationale': source.get('rationale', source.get('adaptation')),
                'license_notice_references': [f'references/legal/{filename.split("-")[0]}-license.md'],
                'test_ids': [f'{m}:positive|negative|operational' for m in methods if m != 'root-contract'],
                'verification_state': 'PLANNED',
                'audit_evidence': filename,
            })
    ids = [r['source_id'] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate source identity')
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit-dir', type=Path, default=AUDIT)
    args = parser.parse_args()
    audits = {p.name: json.loads(p.read_text(encoding='utf-8'))
              for p in sorted(args.audit_dir.glob('*-audit.json'))}
    if len(audits) != 3:
        raise ValueError('Exactly three complete source audit manifests required')
    rows = build_rows(audits)
    evidence = {'schema_version': 1, 'rows': rows,
                'source_categories': dict(Counter(r['source_status'] for r in rows)),
                'audit_sha256': {name: hashlib.sha256((args.audit_dir/name).read_bytes()).hexdigest() for name in audits}}
    (args.audit_dir / 'coverage.json').write_text(json.dumps(evidence, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps({'rows': len(rows), 'categories': evidence['source_categories'],
                      'method_ids': sorted({m['id'] for r in rows for m in r['andino_method_ids_and_paths']})}))


if __name__ == '__main__':
    main()
