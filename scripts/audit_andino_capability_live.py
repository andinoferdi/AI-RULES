"""Audit recorded verdict consistency and coverage; does not execute or grade an actor."""

import argparse
import json
from collections import Counter
from pathlib import Path

from validate_andino_capabilities import ROOT, REQUIRED_CASES, EVAL_CASES, content_hash, runtime_files, validate_record, historical_hashes


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime',type=Path,required=True)
    parser.add_argument('--records',type=Path,default=ROOT/'docs/validation/andino-workflow/live')
    parser.add_argument('--allow-historical',action='store_true',help='Audit only documented older hashes without claiming latest-runtime PASS')
    args=parser.parse_args()
    current=content_hash(runtime_files(args.runtime))
    prior=historical_hashes(current,args.allow_historical)
    errors=[]
    results=Counter()
    revisions=Counter()
    seen=set()
    for path in sorted(args.records.glob('*.json')):
        try:
            record=json.loads(path.read_text(encoding='utf-8'))
        except (OSError,ValueError) as exc:
            errors.append(f'{path.name}: {exc}')
            continue
        errors.extend(f'{path.name}: {error}' for error in validate_record(record))
        if not isinstance(record,dict):
            continue
        if record.get('runtime_hash') != current and record.get('runtime_hash') not in prior:
            errors.append(f'{path.name}: stale/different runtime hash')
        revisions[record.get('runtime_hash','INVALID')]+=1
        identity=record.get('case')
        if not isinstance(identity,str) or identity not in EVAL_CASES:
            errors.append(f'{path.name}: unknown behavioral case')
            continue
        if identity in seen:
            errors.append(f'{path.name}: duplicate behavioral record')
        seen.add(identity)
        if record.get('scope') != 'behavioral':
            errors.append(f'{path.name}: smoke must stay separate')
        if record.get('verdict') == 'PASS' and record.get('selected'):
            completed=[i for i in record.get('invocations',[]) if isinstance(i,dict) and i.get('status')=='completed' and i.get('exit_code',0)==0]
            if not completed:
                errors.append(f'{path.name}: selected capability PASS has no successful observed invocation')
        results[record.get('verdict','INVALID')]+=1
    missing=sorted(REQUIRED_CASES-seen)
    print(json.dumps({'recorded':len(seen),'verdicts':dict(results),'missing':missing,'current_runtime_hash':current,'recorded_revisions':dict(revisions)}))
    if errors:
        print('\n'.join('FAIL: '+error for error in errors))
        return 1
    print('PASS: recorded evidence is structurally consistent; no model grading or cross-host claim.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
