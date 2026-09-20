"""Sequential, opt-in behavioral runs; no automatic grading or remote actions."""
import argparse
import json
import subprocess
import sys
import hashlib
from pathlib import Path
from run_skripsi_smoke import make_prompt

ROOT = Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--runtime',required=True,type=Path)
    p.add_argument('--start',type=int,default=1)
    p.add_argument('--stop',type=int,default=110)
    p.add_argument('--timeout',type=int,default=120)
    a=p.parse_args()
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.runtime,text=True).strip()
    cases={c['id']:c for c in json.loads((ROOT/'evals/skripsi-skill.json').read_text(encoding='utf-8'))}
    fixtures=json.loads((ROOT/'evals/skripsi-fixtures.json').read_text(encoding='utf-8'))
    for number in range(a.start,a.stop+1):
        ident=f'EVAL-{number:03}'
        out=ROOT/'docs/validation/skripsi-skill/live'/f'{ident}.json'
        if out.exists():
            old=json.loads(out.read_text(encoding='utf-8'))
            spec=fixtures['cases'].get(ident,{})
            fixture='\n'.join(filter(None,[fixtures['notice'],fixtures.get(spec.get('base',''),''),spec.get('extra','')])) if spec else ''
            fingerprint=hashlib.sha256(make_prompt(cases[ident],fixture).encode('utf-8')).hexdigest()
            if old.get('runtime_revision')==revision and old.get('execution_status')=='EXECUTED' and old.get('input_sha256')==fingerprint:
                print(f'{ident} existing execution retained',flush=True)
                continue
        result=subprocess.run([sys.executable,str(ROOT/'scripts/run_skripsi_smoke.py'),'--runtime',str(a.runtime),
                               '--case',ident,'--output',str(out),'--timeout',str(a.timeout)],cwd=ROOT)
        if result.returncode:
            raise SystemExit(result.returncode)

if __name__=='__main__':
    main()
