# Prepare a human-only procedure: procedure detail and bounded example

Stage schema: name, prerequisites, URL/command, exact action, output variable name, is_secret, local destination, optional external destination, irreversible flag, completion observation. Prefer a human checklist over bespoke credential-handling code. A native-shell implementation may use protected secret input and atomic replace only after preserving permissions; no script is automatically installed or run.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
stages=[{"name":"create test key","produces":"SERVICE_KEY","secret":True,"destination":".env","external":False},{"name":"confirm test mode","produces":"MODE","secret":False,"destination":".env","external":False}]
names=[s["produces"] for s in stages]
Path("manual-steps.md").write_text("1. Open verified test dashboard. Enter SERVICE_KEY privately in your own terminal; never paste into chat.\n2. Confirm MODE=test.\nNo external writes.",encoding="utf-8")
result={"variables":names,"secret_names":["SERVICE_KEY"],"secret_values":[],"external_writes":[]}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
