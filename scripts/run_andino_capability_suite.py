"""Sequential opt-in live evaluations; no automatic grading, installs or MCP enabling."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from validate_andino_capabilities import ROOT, EVAL_CASES


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime',type=Path,required=True)
    parser.add_argument('--catalog',type=Path)
    parser.add_argument('--output',type=Path,default=ROOT/'docs/validation/andino-workflow/live')
    parser.add_argument('--case',action='append',help='Repeat to select cases; default is all capability scenarios')
    parser.add_argument('--timeout',type=int,default=120)
    parser.add_argument('--skip-recorded',action='store_true',help='Resume without overwriting existing records; hashes still need audit')
    args=parser.parse_args()
    all_cases=json.loads((ROOT/'evals/andino-workflow.json').read_text(encoding='utf-8'))
    selected=args.case or [c['id'] for c in all_cases if c['id'] in EVAL_CASES]
    if set(selected)-EVAL_CASES:
        parser.error('Unknown capability case')
    errors=[]
    for identity in selected:
        output=args.output/(identity+'.json')
        if args.skip_recorded and output.exists():
            print(f'PRESERVED: {identity}',flush=True)
            continue
        command=[sys.executable,str(ROOT/'scripts/run_andino_capability_eval.py'),'--runtime',str(args.runtime),'--case',identity,'--output',str(output),'--timeout',str(args.timeout)]
        if args.catalog:
            command.extend(['--catalog',str(args.catalog)])
        result=subprocess.run(command,cwd=ROOT,check=False)
        if result.returncode:
            errors.append(identity)
            print(f'NOT_VERIFIED: {identity}; environment/actor execution failed; continuing independent cases',flush=True)
            if result.returncode != 2:
                print('STOP: deterministic runner/setup error; fix before attempting another case.',flush=True)
                return 1
    print(f'Attempted {len(selected)} requested cases; {len(errors)} execution failures. Review records; execution is not PASS.',flush=True)
    return 2 if errors else 0


if __name__=='__main__':
    raise SystemExit(main())
