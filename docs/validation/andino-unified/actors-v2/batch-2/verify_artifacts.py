import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
results = json.loads((root / 'results.json').read_text())
work = json.loads((root / 'work.json').read_text())
for filename, expected in work['hashes'].items():
    assert hashlib.sha256((root / filename).read_bytes()).hexdigest() == expected, filename
for row in results['selection_results']:
    for resource in row['selected']:
        assert resource['state'] == 'ACTIVE' and resource['used'] is False
        assert hashlib.sha256(Path(resource['path']).read_bytes()).hexdigest() == resource['sha256']
assert len(results['selection_results']) == 38
assert work['green']['tests'] == 3 and work['green']['exit_code'] == 0
assert work['faulty_copy_sensitivity']['failures'] == 3
assert work['commands'][7]['exit_code'] == 0
assert '=before.py' in work['commands'][7]['output']
assert work['commands'][8]['exit_code'] == 1
print(json.dumps({'records_parse': True, 'selection_count': 38, 'all_recorded_hashes_current': True,
                  'snapshot_states_honest': True, 'wrapper_failure_not_counted_as_sensitivity': True}, sort_keys=True))
