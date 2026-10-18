# Enforce TypeScript package entrypoints: procedure detail and bounded example

Package example: packages/orders/index.ts and client.ts public; lib/policy.ts private; tests/order.test.ts calls ../index and may import ./fixtures.ts. App cannot import orders/lib or orders/tests. Rule matching must use importer package identity, not one hardcoded rule per package. Preserve group/back-reference semantics when adapting dependency-cruiser; verify current API before actual installation.

## Run the example

Use only a fresh disposable directory. The Python standard-library block writes local artifacts. The main checker executes this exact block and independently verifies outputs. Optional browser interaction and dependency-cruiser execution are separate, honestly unverified claims.

```python
from pathlib import Path
import json
def check_graph(edges):
 rules=set(); adjacency={}
 def part(path):
  p=path.split("/")
  return (p[1],len(p)>3,len(p)>3 and p[2]=="tests") if len(p)>2 and p[0]=="packages" else (None,False,False)
 for source,target in edges:
  adjacency.setdefault(source,[]).append(target)
  sp,si,st=part(source); tp,ti,tt=part(target)
  if tt and not st: rules.add("tests-folder-is-private")
  elif tp and ti:
   if sp is None: rules.add("entrypoint-boundary-from-app")
   elif sp!=tp and not st: rules.add("entrypoint-boundary-across-packages")
   elif st and not(sp==tp and tt): rules.add("tests-through-entrypoints")
 visiting=set(); visited=set()
 def visit(node):
  if node in visiting: return True
  if node in visited: return False
  visiting.add(node)
  cycle=any(visit(n) for n in adjacency.get(node,[]))
  visiting.remove(node); visited.add(node)
  return cycle
 if any(visit(n) for n in list(adjacency)): rules.add("no-circular")
 return sorted(rules)
clean=[("app/main.ts","packages/orders/index.ts"),("packages/orders/lib/a.ts","packages/orders/lib/b.ts"),("packages/orders/tests/a.ts","packages/orders/tests/fixture.ts")]
dirty=clean+[("packages/orders/tests/a.ts","packages/orders/lib/b.ts")]
result={"clean":check_graph(clean),"dirty":check_graph(dirty),"restored":check_graph(clean),"app":check_graph([("app/main.ts","packages/orders/lib/a.ts")]),"cross":check_graph([("packages/billing/lib/a.ts","packages/orders/lib/a.ts")]),"fixture":check_graph([("packages/orders/index.ts","packages/orders/tests/fixture.ts")]),"cycle":check_graph([("app/a.ts","app/b.ts"),("app/b.ts","app/a.ts")]),"external_tool_run":False}
Path("boundary-results.json").write_text(json.dumps(result),encoding="utf-8")
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

The TypeScript example implements the five graph rules against literal valid and invalid import fixtures, including a dependency cycle; it does not execute the actual dependency-cruiser resolver. The prototype produces an offline runnable HTML with pure reducer, state display, free-play and guided scenarios. Its Python model is exercised; browser click behavior must be checked separately before claiming live interaction success.
