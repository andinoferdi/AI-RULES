# Specify a recurring workflow: procedure detail and bounded example

Terms: trigger fires a run; workflow is the contract; loop is its repeated instantiation; checkpoint is actual human judgment; brief makes review quick. Example event-driven inbox workflow drafts a categorization summary, then asks the user to approve any external reply. Drafting and sending are different permissions.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
workflow={"trigger":{"type":"event","event":"new support request"},"steps":["classify","draft response"],"checkpoint":{"after":"draft response","brief":["summary","reason","draft link"]},"permissions":{"send":False},"done":"reviewable response draft"}
Path("workflow.json").write_text(json.dumps(workflow,indent=2),encoding="utf-8")
result={"trigger":"event","checkpoint_after":"draft response","send_allowed":False,"automation_created":False}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
