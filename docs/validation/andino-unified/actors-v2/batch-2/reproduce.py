import json
from subject import page

items = ['A', 'B', 'C', 'D']
observed = {'page0': page(items, 0, 2), 'page1': page(items, 1, 2)}
print(json.dumps(observed, sort_keys=True))
