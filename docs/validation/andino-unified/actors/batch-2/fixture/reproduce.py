import json
from subject import page
items = ['A', 'B', 'C', 'D']
print(json.dumps({'first': page(items, 0, 2), 'second': page(items, 1, 2)}))
