"""Independent artifact/trace oracle; does not claim live tool enforcement."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, required=True)
args = parser.parse_args()
internal = args.root / 'internal'
changed = [path for path, digest in json.loads((internal / 'baseline.json').read_text()).items()
           if hashlib.sha256((internal / path).read_bytes()).hexdigest() != digest]
assert not changed, changed
blocks = re.findall(r'```python\n(.*?)\n```', (internal / 'PLAN.md').read_text(encoding='utf-8'), re.S)
for block in blocks:
    ast.parse(block)
assert len(blocks) == 6, len(blocks)
external = args.root / 'external'
resources = external / 'installed/external-contract-notebook/resources'
expected = json.loads((resources / 'model.json').read_text())
expected['cases'] = json.loads((resources / 'cases.json').read_text())
assert len(expected['cases']) == 12
assert json.loads((external / 'CONTRACT.json').read_text()) == expected
oracle = ['reuse', 'change_hypothesis', 'record_boundary', 'checkpoint_blocker',
          'query_R7_relevant_fields', 'load_one_relevant_schema', 'low_effort_inline',
          'full_spec_link_from_checkpoint', 'use_explicit_external_method', 'rerun_affected_check']
decisions = json.loads((external / 'DECISIONS.json').read_text())
assert [case['id'] for case in decisions] == [f'G{i:02}' for i in range(1, 11)]
assert [case['next'] for case in decisions] == oracle
assert all(case['reason'].strip() for case in decisions)
print('PASS: 8 preserved inputs, 6 syntactically valid plan blocks, 12 exact external cases and 10 independently expected trace decisions')
print('Plan meaning/coverage requires separate review; live tool controls and initial activation ordering are not proved by this oracle.')
