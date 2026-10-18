import json
from subject import page
items = ['A', 'B', 'C', 'D']
cases = [(1, ['B']), (2, ['C', 'D']), (3, ['D'])]
observations = []
for size, expected in cases:
    actual = page(items, 1, size)
    candidate_start = 1 * size
    candidate = items[candidate_start:candidate_start + size]
    observations.append({'size': size, 'actual': actual, 'expected': expected, 'candidate': candidate})
    assert actual != expected, 'Prediction requires the original incorrect stride'
    assert candidate == expected
print(json.dumps(observations))
