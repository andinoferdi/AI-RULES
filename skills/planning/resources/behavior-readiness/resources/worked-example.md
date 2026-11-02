# Write a buildable specification: procedure detail and bounded example

Suggested content: Objective/problem/solution; capability map if warranted; behavior and scope; interface decisions; actual project context/commands/style; testing/seam choices; authority boundaries; open questions. A provider owns its contract. Capability maps describe independent deliverables, task graphs describe implementation order, decision maps describe unanswered questions: keep these roles distinct.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
modules={"identity":[],"billing":["identity"],"reports":["billing"]}
remaining=dict(modules); order=[]
while remaining:
 ready=sorted(k for k,v in remaining.items() if set(v)<=set(order))
 if not ready: raise ValueError("capability cycle")
 order.extend(ready)
 for k in ready: del remaining[k]
criteria={"identity":["session can be retrieved"],"billing":["one invoice per retry key"],"reports":["total agrees with invoice fixture"]}
Path("spec.md").write_text("Objective: reliable billing\nBuild order: "+" -> ".join(order)+"\nOut of scope: email delivery\n"+json.dumps(criteria),encoding="utf-8")
result={"build_order":order,"criteria_owned":sorted(criteria),"open_questions":[]}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
