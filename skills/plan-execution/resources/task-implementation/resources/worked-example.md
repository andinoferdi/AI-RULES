# Execute an accepted slice: procedure detail and bounded example

The task graph is an execution aid within Andino, not an integration-branch mandate. If a task depends on ignored fixtures or credentials missing in a worktree, verify safely in the approved checkout or report that validation unavailable. Avoid repeated broad review loops; fix evidenced findings and run focused checks. Long-term tactics such as better diagnostics belong only when they serve observed needs.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
deps={"schema":[],"api":["schema"],"screen":["api"],"docs":["schema"]}
accepted={"schema"}
frontier=sorted(k for k,v in deps.items() if k not in accepted and set(v)<=accepted)
Path("checkpoint.md").write_text("Accepted: schema\nReady: api, docs\nBlocked: screen\nNEXT ACTION: implement api",encoding="utf-8")
result={"ready":frontier,"blocked":["screen"],"git_mutations":[]}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
