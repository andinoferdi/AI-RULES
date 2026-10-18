from pathlib import Path
source = Path('subject.before.py').read_text()
assert 'index * (size - 1)' in source
candidate = source.replace('index * (size - 1)', 'index * size', 1)
namespace = {}
exec(candidate, namespace)
pages = [namespace['page'](['A', 'B', 'C', 'D'], i, 2) for i in (0, 1, 2)]
assert pages == [['A', 'B'], ['C', 'D'], []], pages
print({'changed_variable': 'stride only', 'observed_pages': pages, 'prediction': 'confirmed'})
