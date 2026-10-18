# Draft a questionnaire for someone else: procedure detail and bounded example

Format: title; Purpose; From/To/How used; Context; How to answer; themed questions with answer stubs; Anything else. A question for platform owner about launch throughput differs from a question for finance about budget, even when both inform capacity. Static questionnaires collect unknowns, interviews recompute a live frontier.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
gaps={"capacity":"What peak request rate must launch support?","retention":"How long must audit records be retained?"}
recipient="platform owner"
Path("questionnaire.md").write_text("# Launch discovery\nPurpose: choose capacity and retention\nTo: "+recipient+"\nPartial answers and unknowns are useful.\n\n"+"\n\n".join(f"## {q}\n\n> " for q in gaps.values()),encoding="utf-8")
result={"recipient":recipient,"covered_gaps":sorted(gaps),"sent":False}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
