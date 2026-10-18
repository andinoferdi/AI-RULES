# Configure project workflow documents: procedure detail and bounded example

Local issue convention can use one feature directory, spec, issues/NN-title.md, Status and Blocked by, append-only comments. GitHub shared issue/PR numbering differs from GitLab separate spaces; resolve type explicitly. Native dependencies require real IDs and feature availability. Main Andino checkpoint remains authoritative; these are domain adapter documents, not another execution board.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
existing="# Project\nKeep this instruction.\n"
mapping={"needs-triage":"triage","needs-info":"waiting","ready-for-agent":"agent-ready","ready-for-human":"human-ready","wontfix":"declined"}
Path("issue-tracker.md").write_text("Tracker: local Markdown\nOne file per issue; Blocked by: real IDs; comments append.",encoding="utf-8")
Path("triage-labels.json").write_text(json.dumps(mapping),encoding="utf-8")
Path("AGENTS.md").write_text(existing+"\nWorkflow documents: issue-tracker.md and triage-labels.json\n",encoding="utf-8")
result={"roles":len(mapping),"preserved":"Keep this instruction." in Path("AGENTS.md").read_text(),"external_writes":[]}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
