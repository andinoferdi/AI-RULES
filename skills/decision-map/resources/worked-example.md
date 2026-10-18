# Map unresolved decisions: procedure detail and bounded example

Map template: Destination; Notes; Decisions so far (gist + pointer only); Not yet specified; Out of scope. Question record: ID/title, type, question, blockers, claim, answer/evidence. Render names as links instead of walls of IDs. Research produces cited facts, prototypes produce a user-evaluated answer, interviews record actual decisions and prerequisite tasks record the facts they made available.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
tickets={"sources":{"type":"research","blocked":[],"status":"resolved"},"choice":{"type":"interview","blocked":["sources"],"status":"open"},"prototype":{"type":"prototype","blocked":["choice"],"status":"open"}}
frontier=sorted(k for k,v in tickets.items() if v["status"]=="open" and all(tickets[b]["status"]=="resolved" for b in v["blocked"]))
Path("map.md").write_text("Destination: choose local storage\nDecisions so far: sources -> source-note.md\nNot yet specified: backup policy\nOut of scope: cloud sync",encoding="utf-8")
result={"frontier":frontier,"user_choice_resolved":False,"implementation_started":False}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
