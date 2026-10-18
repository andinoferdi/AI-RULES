"""Prepare raw actor inputs separately from the private routing oracle."""
import hashlib
import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT/'docs/validation/andino-unified'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suffix', default='')
    args = parser.parse_args()
    if args.suffix and (not args.suffix.startswith('-') or not args.suffix[1:].isalnum()):
        parser.error('suffix must be a hyphen followed by letters/digits')
    methods = [m for path in sorted(AUDIT.glob('*-methods.json'))
               for m in json.loads(path.read_text(encoding='utf-8'))]
    cases, oracle, evals = [], {}, []
    for method in methods:
        for kind in ('positive', 'negative'):
            activation = method.get('activation', {}).get(kind, {})
            request = activation.get('request') or method[kind+'_requests'][0]
            case_id = hashlib.sha256((method['id']+':'+kind).encode()).hexdigest()[:12]
            cases.append(dict(id=case_id, request=request))
            oracle[case_id] = dict(method=method['id'], kind=kind)
            evals.append(dict(id='unified-'+method['id']+'-'+kind,
                              kind='behavior' if kind == 'positive' else 'negative-trigger',
                              prompt=request, fixture='Disposable task; no external action authorized. Other product facts/accepted current phase are settled unless the request explicitly asks to resolve them.',
                              expected=f"Select {method['id']}" if kind == 'positive' else f"Do not select {method['id']}",
                              forbidden='Bulk loading or invented tool/skill use; authority bypass.',
                              capabilities=[method['id']]))
    random.Random(20261018).shuffle(cases)
    inputs = AUDIT/('actor-inputs'+args.suffix)
    inputs.mkdir(exist_ok=True)
    work = [
        dict(request='Use Andino to implement sum_invoice(values) for integer amounts: sum_invoice([10,5]) must return 15 and empty input returns 0. Use an executable regression and preserve the public function. Work in your output directory only.',
             files={'subject.py': 'def sum_invoice(values):\n    return 0\n'}),
        dict(request='Use Andino to investigate and fix this reported bug. Calling page([A,B,C,D],0,2) returns A,B but page(...,1,2) returns B,C; page indices start at zero and pages must be consecutive non-overlapping slices. Reproduce the actual symptom, test a cause, and verify the fix in your output directory only.',
             files={'subject.py': 'def page(items, index, size):\n    start = index * (size - 1)\n    return items[start:start + size]\n'}),
        dict(request='Use Andino to review candidate.py as an uncommitted new file. Spec: admins may open every record; members may open only records from their own organization. Standard: never evaluate user input dynamically. Do not repair it. Write review.json with specific findings, file/line, consequence, and separate spec/standards verdicts.',
             files={'candidate.py': 'def can_open(user, record):\n    role = eval(repr(user["role"]))\n    return role == "admin" or user["org"] != record["org"]\n'})
    ]
    for index in range(3):
        content = dict(selection_cases=cases[index::3], work=work[index])
        (inputs/f'batch-{index+1}.json').write_text(json.dumps(content, indent=2)+'\n', encoding='utf-8')
    (AUDIT/('routing-oracle'+args.suffix+'.json')).write_text(json.dumps(oracle, indent=2)+'\n', encoding='utf-8')
    (ROOT/'evals/andino-unified.json').write_text(json.dumps(evals, indent=2)+'\n', encoding='utf-8')
    print(f'{len(cases)} raw requests in three oracle-hidden actor inputs; {len(methods)} method pairs.')


if __name__ == '__main__':
    main()
