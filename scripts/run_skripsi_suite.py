"""Sequential, opt-in behavioral runs; no automatic grading or remote actions."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--runtime',required=True,type=Path)
    p.add_argument('--start',type=int,default=1)
    p.add_argument('--stop',type=int,default=110)
    p.add_argument('--timeout',type=int,default=120)
    a=p.parse_args()
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.runtime,text=True).strip()
    for number in range(a.start,a.stop+1):
        ident=f'EVAL-{number:03}'
        out=ROOT/'docs/validation/skripsi-skill/live'/f'{ident}.json'
        if out.exists():
            old=json.loads(out.read_text(encoding='utf-8'))
            if old.get('runtime_revision')==revision and old.get('execution_status')=='EXECUTED':
                print(f'{ident} existing execution retained',flush=True)
                continue
        result=subprocess.run([sys.executable,str(ROOT/'scripts/run_skripsi_smoke.py'),'--runtime',str(a.runtime),
                               '--case',ident,'--output',str(out),'--timeout',str(a.timeout)],cwd=ROOT)
        if result.returncode:
            raise SystemExit(result.returncode)

if __name__=='__main__':
    main()
