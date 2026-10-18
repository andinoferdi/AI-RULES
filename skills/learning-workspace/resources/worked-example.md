# Build a learning workspace: procedure detail and bounded example

Workspace: MISSION.md (Why/Success/Constraints/Out of scope), RESOURCES.md (Knowledge/Wisdom/Gaps with annotations), lessons/NN.html, reference/, assets/, learning-records/NN.md and NOTES.md. Learning records are sparse non-obvious changes with evidence; supersede corrected knowledge instead of deleting history. Runtime package examples contain no mandatory course assets or network requirement.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
records=[{"concept":"retry identity","kind":"covered"},{"concept":"idempotency","kind":"demonstrated","evidence":"correctly explained duplicate fixture"},{"concept":"timeouts","kind":"prior knowledge","evidence":"user stated experience"}]
learned=[r["concept"] for r in records if r["kind"]!="covered"]
Path("MISSION.md").write_text("Why: diagnose safe retries\nSuccess: explain duplicate handling\nOut of scope: distributed consensus",encoding="utf-8")
Path("lesson.html").write_text("<!doctype html><h1>Retry identity</h1><p>Compare duplicate requests against the provided fixture.</p><p>Reference: local source fixture</p>",encoding="utf-8")
result={"recorded":learned,"covered_not_mastered":["retry identity"],"scheduled":False}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
