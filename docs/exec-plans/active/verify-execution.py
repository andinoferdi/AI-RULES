import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

parser = argparse.ArgumentParser(description='Validate a supplied workflow runtime from the main quality plane')
parser.add_argument('--runtime', type=Path, required=True)
root = parser.parse_args().runtime.resolve()
member = root / 'skills/plan-execution'
guide = (member / 'GUIDE.md').read_text(encoding='utf-8')
skill = (member / 'SKILL.md').read_text(encoding='utf-8')
assert skill.split('---', 2)[2].strip() == guide.strip()
code = re.search(r'```python evolution-example\n(.*?)\n```', guide, re.S)[1]
namespace = {}
exec(code, namespace)
reuse = namespace['reusable_tasks']
task = [{'id': 'x', 'deps': []}]
assert reuse(task, {'x': {'result': 'PASS'}}, {'x': {'anything': 'present'}})['rerun'] == ['x']
assert reuse(task, {'x': {'result': 'PASS', 'source': '', 'check': '', 'environment': ''}},
             {'x': {'source': '', 'check': '', 'environment': ''}})['rerun'] == ['x']
old = code.replace('and all(isinstance(record.get(key), str) and record[key].strip()\n'
                   '                            for record in (old, now)\n'
                   '                            for key in ("source", "check", "environment"))\n                    ', '')
mutant = {}
exec(old, mutant)
assert mutant['reusable_tasks'](task, {'x': {'result': 'PASS'}}, {'x': {'anything': 'present'}})['reusable'] == ['x']
print('PASS: synchronized entrypoints; drift fixture; missing/empty identity; old mutation rejected')
main = Path(__file__).resolve().parents[3]
with tempfile.TemporaryDirectory(prefix='plan-execution-candidate-') as tmp:
    candidate = Path(tmp) / 'workflow'
    candidate.mkdir()
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
    for name in filter(None, paths):
        if not (root / name).is_file():
            continue
        target = candidate / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((root / name).read_bytes())
    for command in (
        ['python', 'scripts/validate_skills.py', '--andino-dir', str(candidate)],
    ):
        result = subprocess.run(command, cwd=main, capture_output=True, text=True, encoding='utf-8')
        print('COMMAND', command, 'EXIT', result.returncode)
        print(result.stdout[-6000:])
        print(result.stderr[-1000:])
        assert result.returncode == 0
print(json.dumps({p.relative_to(member).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in member.rglob('*') if p.is_file()}, indent=2))
