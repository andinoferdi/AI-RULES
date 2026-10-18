# Capture primary-source findings: procedure detail and bounded example

Findings format: Question; Source/version table; Observations with line/page/URL citations; Inferences separately; Decision implications; Gaps and verification date. This local example uses provided source facts as a fixture and proves claim-to-source closure, not live internet research.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
sources={"spec-v1":{"revision":"v1","facts":{"retry_key":"required","retention_hours":24}}}
claims=[{"claim":"Retry key is required","source":"spec-v1","field":"retry_key","value":"required"},{"claim":"Retention is 24 hours","source":"spec-v1","field":"retention_hours","value":24}]
unsupported=[c["claim"] for c in claims if sources[c["source"]]["facts"][c["field"]]!=c["value"]]
Path("research.md").write_text("\n".join(f"- {c['claim']} [fixture {c['source']}]" for c in claims),encoding="utf-8")
result={"supported":len(claims)-len(unsupported),"unsupported":unsupported,"live_research":False}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
