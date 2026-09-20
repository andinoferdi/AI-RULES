"""Validate recorded human/agent adjudication; never infer behavioral success."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit(cases, reviews, records):
    errors = []
    ids = {case['id'] for case in cases}
    for case in cases:
        key = case['id']
        review, record = reviews.get(key, {}), records.get(key, {})
        verdict = review.get('verdict')
        if verdict not in ('PASS', 'FAIL', 'NOT_VERIFIED') or not review.get('reason'):
            errors.append(f'{key}: missing explicit verdict/reason')
        if not record:
            errors.append(f'{key}: missing execution record')
            continue
        if record.get('case') != key or not record.get('runtime_revision'):
            errors.append(f'{key}: record identity/revision missing')
        if not record.get('oracle_hidden'):
            errors.append(f'{key}: oracle isolation not recorded')
        if verdict == 'PASS':
            if record.get('execution_status') != 'EXECUTED' or not record.get('observed_output'):
                errors.append(f'{key}: PASS without successful observed execution')
            if case.get('kind') != 'negative-trigger':
                reads = [a for a in record.get('tool_actions', [])
                         if a.get('exit_code') == 0 and 'SKILL.md' in a.get('command', '')]
                if not reads:
                    errors.append(f'{key}: PASS without successful skill read')
        if verdict == 'FAIL':
            errors.append(f'{key}: unresolved behavioral failure')
    for key in set(reviews) - ids:
        errors.append(f'{key}: review has no oracle')
    return errors


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory', type=Path, default=ROOT/'docs/validation/skripsi-skill')
    a = p.parse_args()
    cases = json.loads((ROOT/'evals/skripsi-skill.json').read_text(encoding='utf-8'))
    reviews = json.loads((a.directory/'live-review.json').read_text(encoding='utf-8'))['reviews']
    records = {f.stem: json.loads(f.read_text(encoding='utf-8')) for f in (a.directory/'live').glob('*.json')}
    errors = audit(cases, reviews, records)
    if errors:
        print('\n'.join(errors))
        return 1
    counts = {v: sum(r['verdict'] == v for r in reviews.values()) for v in ('PASS','FAIL','NOT_VERIFIED')}
    print(json.dumps(counts))
    print('Record consistency checked; NOT_VERIFIED remains a verification limit.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
