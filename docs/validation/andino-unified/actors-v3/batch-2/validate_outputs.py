import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
results = json.loads((root / 'results.json').read_text(encoding='utf-8'))
work = json.loads((root / 'work.json').read_text(encoding='utf-8'))
assert len(results['selection_results']) == 38
assert len({x['id'] for x in results['selection_results']}) == 38
assert all(not x['scenario_actions'] for x in results['selection_results'])
for resource in results['resource_activation']:
    assert hashlib.sha256(Path(resource['path']).read_bytes()).hexdigest() == resource['sha256'], resource['path']
for case in results['selection_results']:
    for resource in case['selected']:
        assert hashlib.sha256(Path(resource['path']).read_bytes()).hexdigest() == resource['sha256'], resource['path']
assert work['status'] == 'DONE'
assert hashlib.sha256((root / 'subject.before.py').read_bytes()).hexdigest() == work['before']['sha256']
assert hashlib.sha256((root / 'subject.py').read_bytes()).hexdigest() == work['after']['sha256']
observed = {x['name']: x['exit_code'] for x in work['commands']}
assert observed == {'reproduction': 0, 'red': 1, 'hypothesis': 0, 'green': 0, 'suite': 0,
                    'faulty_copy_sensitivity': 1, 'original_scenario_after_fix': 0}, observed
summary = {'selection_cases': 38, 'resource_hashes': 'match current files',
           'fixture_record': work['status'], 'observed_exits': observed,
           'results_sha256': hashlib.sha256((root / 'results.json').read_bytes()).hexdigest(),
           'work_sha256': hashlib.sha256((root / 'work.json').read_bytes()).hexdigest()}
(root / 'validation.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
print(json.dumps(summary, indent=2))
