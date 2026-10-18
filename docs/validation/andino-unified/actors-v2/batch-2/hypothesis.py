import json
from pathlib import Path

faulty = Path(__file__).with_name('subject.py').read_text()
probe = faulty.replace('index * (size - 1)', 'index * size')
assert faulty != probe
scope = {}
exec(compile(probe, '<single-variable-hypothesis>', 'exec'), scope)
assert scope['page'](['A', 'B', 'C', 'D'], 1, 2) == ['C', 'D']
print(json.dumps({'variable': 'start stride', 'old_start': 1, 'predicted_start': 2,
                  'predicted_page1': ['C', 'D'],
                  'observed_page1': scope['page'](['A', 'B', 'C', 'D'], 1, 2),
                  'hypothesis_supported': True}, sort_keys=True))
