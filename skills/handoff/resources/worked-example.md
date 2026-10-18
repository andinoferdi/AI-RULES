# Prepare a portable handoff: procedure detail and bounded example

Preserve primary-source pointers when the next phase depends on reasoning that compression could flatten. The ordered context choices are Continue, discard irrelevant context, portable Handoff, bounded delegation, then compaction if needed; this is judgment under host constraints, not mandatory commands. No handoff replaces current Andino task state.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
record={"state":"slice implemented, verification pending","phase":"verify","evidence":["spec.md","changes.diff"],"permissions":{"commit":False},"next_action":"run the accepted public-interface test"}
Path("handoff.md").write_text("\n".join(f"{k}: {json.dumps(v)}" for k,v in record.items()),encoding="utf-8")
result={"next_action":record["next_action"],"references":record["evidence"],"commit_allowed":False,"spawned":False}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
