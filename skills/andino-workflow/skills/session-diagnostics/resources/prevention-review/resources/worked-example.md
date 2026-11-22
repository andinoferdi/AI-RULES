# Improve the working environment: procedure detail and bounded example

Candidate record: session event, cost/impact, existing guard, deterministic vs judgment classification, proposed change and proving observation. Navigation instructions should point to otherwise hidden decisions, not repeat one-command environment facts. A retrospective improves the environment around the code; architecture-survey examines code structure.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
events=[{"id":"e1","failure":"formatter existed but CI omitted it","kind":"mechanical","existing":"format-check"},{"id":"e2","failure":"review missed inconsistent domain naming","kind":"judgment","existing":None}]
actions=[{"evidence":e["id"],"action":"wire existing "+e["existing"] if e["existing"] else "add review standard"} for e in events]
Path("retro.md").write_text("\n".join(f"{a['evidence']}: {a['action']}" for a in actions),encoding="utf-8")
result={"actions":actions,"new_formatter":False,"global_edits":[]}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
