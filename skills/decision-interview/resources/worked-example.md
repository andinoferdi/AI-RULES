# Clarify the decision: procedure detail and bounded example

The design tree is a dependency graph of decisions, not an implementation task graph. Builder checks rank questions by impact, skip builder discretion and wording nitpicks, and do not create recursive reviewers. A visual comparison can be a local static HTML/SVG file with 2–4 options; no upstream companion server, event telemetry, process launcher or runtime network is needed. Record explicit spoken/written feedback; clicks alone do not manufacture an architectural decision.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
facts={"outcome":"track active experiments","user":"researcher","why_now":"experiments scattered","success":"every active experiment listed","constraint":"local only","out_of_scope":"metrics charts"}
questions={"audience":[],"storage":["audience"],"charts":["audience"]}
settled={"audience"}
frontier=sorted(k for k,v in questions.items() if k not in settled and set(v)<=settled)
Path("intent.md").write_text("\n".join(f"{k}: {v}" for k,v in facts.items()),encoding="utf-8")
result={"frontier":frontier,"out_of_scope":facts["out_of_scope"],"material_missing":[]}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
