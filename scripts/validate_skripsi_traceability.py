"""Check inventory, ownership and evidence references, never grade model behavior."""
import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit(report, runtime_paths, main_paths, case_ids):
    errors=[]
    required={f'FR-{n:03}' for n in range(1,147)} | {f'NFR-{n:03}' for n in range(1,48)} | {f'AC-{n:03}' for n in range(1,143)}
    rows=report.get('requirements',[])
    ids=[row.get('id') for row in rows]
    if len(ids)!=len(set(ids)) or set(ids)!=required:
        errors.append('Requirement inventory must contain exactly 146 FR, 47 NFR and 142 AC without duplicates')
    for group_name, count, prefix in [('capabilities',32,'CAP'),('evals',110,'EVAL'),('core_outputs',61,'OUTPUT')]:
        found=[row.get('id') for row in report.get(group_name,[])]
        width=2 if prefix=='CAP' else 3
        expected={f'{prefix}-{n:0{width}}' for n in range(1,count+1)}
        if len(found)!=len(set(found)) or set(found)!=expected:
            errors.append(f'{group_name}: incomplete or duplicated inventory')
    for row in [*rows,*report.get('capabilities',[]),*report.get('evals',[]),*report.get('core_outputs',[])]:
        target=row.get('implementation',{})
        paths=runtime_paths if target.get('branch')=='skripsi-skill' else main_paths if target.get('branch')=='main' else set()
        if target.get('path') not in paths:
            errors.append(f"{row.get('id')}: missing implementation target {target}")
        if row.get('behavioral_verdict')=='PASS' and not row.get('live_evidence'):
            errors.append(f"{row.get('id')}: behavioral PASS has no live evidence")
        for case in row.get('eval_ids',[]):
            if case not in case_ids:
                errors.append(f"{row.get('id')}: missing eval {case}")
    initial={f'EVAL-{n:03}' for n in range(1,111)}
    if not initial.issubset(case_ids):
        errors.append('SRS initial evals missing from runtime oracle file')
    tasks=report.get('tasks',[])
    tids=[row.get('id') for row in tasks]
    if len(tids)!=75 or len(tids)!=len(set(tids)) or not all(re.fullmatch(r'P\d+-T\d{2}',str(t)) for t in tids):
        errors.append('Expected 75 unique GRAND-PLAN task IDs')
    return errors


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--runtime-ref',default='origin/skripsi-skill')
    a=p.parse_args()
    report=json.loads((ROOT/'docs/validation/skripsi-skill/traceability.json').read_text(encoding='utf-8'))
    paths=set(subprocess.check_output(['git','ls-tree','-r','--name-only',a.runtime_ref],cwd=ROOT,text=True).splitlines())
    main_paths={f.relative_to(ROOT).as_posix() for f in ROOT.rglob('*') if f.is_file() and '.git' not in f.parts}
    cases=json.loads((ROOT/'evals/skripsi-skill.json').read_text(encoding='utf-8'))
    errors=audit(report,paths,main_paths,{c['id'] for c in cases})
    if errors:
        print('\n'.join('FAIL: '+e for e in errors))
        return 1
    print('PASS: 335 requirements/acceptance criteria, 32 capabilities, 110 initial eval owners, 75 task records')
    print('Implementation ownership is not behavioral verification.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
