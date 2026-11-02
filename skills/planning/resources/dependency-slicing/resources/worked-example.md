# Slice work into dependent tasks: procedure detail and bounded example

Wide rename example: expand accepts old+new field, migrate UI and worker independently against dual compatibility, contract removes old field only after both. Task records carry behavior, blockers, status, acceptance and proving command. Specific project paths may be retained where the existing durable plan requires them; avoid brittle line numbers.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
graph={"expand":[],"migrate-ui":["expand"],"migrate-worker":["expand"],"contract":["migrate-ui","migrate-worker"]}
done={"expand","migrate-ui"}
ready=sorted(k for k,v in graph.items() if k not in done and set(v)<=done)
Path("tasks.json").write_text(json.dumps(graph),encoding="utf-8")
result={"ready":ready,"contract_blocked":not set(graph["contract"])<=done,"parent_closed":False}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
