"""Grade frozen raw selections separately from actor work and native-host proof."""
import argparse
import hashlib
import json
from pathlib import Path


def grade(runtime, oracle, actors, siblings=None):
    rows, seen, errors = [], set(), []
    for actor in sorted(actors.glob('batch-*/results.json')):
        for result in json.loads(actor.read_text(encoding='utf-8'))['selection_results']:
            identity = result['id']
            if identity in seen or identity not in oracle:
                errors.append(f'{identity}: duplicate or unknown case')
                continue
            seen.add(identity)
            expected = oracle[identity]
            selected = result['selected']
            failures = []
            for method in selected:
                guide = ((siblings or {}).get(method['id']) or
                         runtime / 'skills' / method['id'] / 'GUIDE.md')
                if not guide.is_file() or Path(method['path']).resolve() != guide.resolve():
                    failures.append(f"{method['id']}: absent or wrong canonical guide")
                elif hashlib.sha256(guide.read_bytes()).hexdigest() != method.get('sha256'):
                    failures.append(f"{method['id']}: stale guide identity")
                if not method.get('reason') or not method.get('insight'):
                    failures.append(f"{method['id']}: missing selection reason/applied insight")
            present = expected['method'] in {m['id'] for m in selected}
            if present != (expected['kind'] == 'positive'):
                failures.append('required method absent' if expected['kind'] == 'positive' else 'excluded method selected')
            rows.append(dict(id=identity, expected=expected, selected=[m['id'] for m in selected],
                             result='FAIL' if failures else 'PASS', errors=failures,
                             actor=actor.as_posix()))
    errors.extend(f'{identity}: missing case' for identity in sorted(set(oracle) - seen))
    return dict(result='FAIL' if errors or any(r['errors'] for r in rows) else 'PASS',
                scope='Oracle-hidden Codex delegated resource selection; actual work and native host invocation graded separately.',
                runtime=runtime.resolve().as_posix(), cases=len(rows),
                passed=sum(r['result'] == 'PASS' for r in rows), rows=rows, errors=errors,
                limitation='Checks expected membership and actual resource byte identity. Parent reviews substantive insights and work; this is not native picker discovery or cross-host parity.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', type=Path, required=True)
    parser.add_argument('--oracle', type=Path, required=True)
    parser.add_argument('--actors', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--catalog', type=Path)
    args = parser.parse_args()
    siblings = {r['id']: Path(r['path']) / 'SKILL.md'
                for r in json.loads(args.catalog.read_text(encoding='utf-8'))} if args.catalog else {}
    report = grade(args.runtime, json.loads(args.oracle.read_text(encoding='utf-8')), args.actors, siblings)
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f"{report['result']}: {report['passed']}/{report['cases']} selections; {len(report['errors'])} accounting errors")
    return int(report['result'] != 'PASS')


if __name__ == '__main__':
    raise SystemExit(main())
