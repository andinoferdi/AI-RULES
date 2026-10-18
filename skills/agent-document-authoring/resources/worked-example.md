# Write documents agents can use: procedure detail and bounded example

Information hierarchy: primary ordered action, nearby in-file reference, then disclosed branch reference. Context load is always-loaded agent cost; human cognitive load is locating/choosing artifacts. Authoring should reduce irrelevant load while preserving meaningful user agency. Shared runtime routing belongs to Andino root/index, never this guide.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
entries=[{"meaning":"use actual repo commands","kind":"action"},{"meaning":"use actual repo commands","kind":"duplicate"},{"meaning":"TS-specific fixture examples","kind":"branch-reference"}]
unique=[]
for e in entries:
 if e["meaning"] not in [x["meaning"] for x in unique]: unique.append(e)
Path("consumer-guide.md").write_text("1. Discover the repository test command; done when its actual definition is located.\nTS fixture migration: read the local fixture reference only for TypeScript tests.",encoding="utf-8")
result={"meanings":len(unique),"duplicate_removed":1,"branch_reference":"TS-specific fixture examples","live_model_verified":False}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
