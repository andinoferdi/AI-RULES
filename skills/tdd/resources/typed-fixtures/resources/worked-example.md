# Migrate TypeScript test fixtures: procedure detail and bounded example

Patterns: object with body.id as Request -> fromPartial({body:{id:'123'}}); intentionally numeric id as unknown as Request -> fromAny({body:{id:123}}); complete object -> fromExact. TypeScript assertions and helpers do not themselves supply runtime validation. A narrow syntax-aware edit or manually reviewed changes are safer than global text substitution.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
fixtures=[{"path":"tests/request.test.ts","intent":"partial","value":{"body":{"id":"123"}}},{"path":"tests/request.test.ts","intent":"invalid","value":{"body":{"id":123}}}]
mapped=[{"helper":"fromPartial" if f["intent"]=="partial" else "fromAny","value":f["value"]} for f in fixtures]
Path("fixture-migration.json").write_text(json.dumps(mapped),encoding="utf-8")
result={"helpers":[m["helper"] for m in mapped],"invalid_id":mapped[1]["value"]["body"]["id"],"production_imports":[],"typescript_run":False}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
