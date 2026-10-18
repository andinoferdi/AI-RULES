# Re-explain a confusing message: procedure detail and bounded example

Example original: 'The frontier is empty because unresolved predecessor edges remain.' Repitch: 'No task can start yet. The API task is waiting for the schema change. Finish that change first, then the API task becomes ready.' Keep domain terms such as Order/Invoice where they prevent ambiguity, and define them if the user does not know them.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
context={"task":"API","blocked_by":"schema"}
text=f"No task can start yet. The {context['task']} task is waiting for the {context['blocked_by']} change. Finish that change first."
Path("repitch.txt").write_text(text,encoding="utf-8")
result={"task":"API","prerequisite":"schema","meaning_preserved":True,"tool_actions":[]}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
