# Shape raw material into an article: procedure detail and bounded example

Beat means one move: scene, claim, question, aside or pivot; one sentence to several paragraphs as needed, but split multiple jobs. A block can ground a concept and unlock several later moves. If a tempting next claim requires an unknown concept, introduce it first or explicitly revise audience prerequisites. Gap-naming prevents fabricated anecdotes.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
grounded={"request"}
beats={"identity":{"requires":{"request"},"grounds":{"idempotency"}},"retry":{"requires":{"idempotency"},"grounds":{"retry safety"}},"billing":{"requires":{"invoice"},"grounds":{"payment"}}}
reachable=sorted(k for k,v in beats.items() if v["requires"]<=grounded)
chosen="identity"; grounded|=beats[chosen]["grounds"]
next_ready=sorted(k for k,v in beats.items() if k!=chosen and v["requires"]<=grounded)
Path("raw.md").write_text("Requests can be repeated. Identity connects repeated attempts.",encoding="utf-8")
original=Path("raw.md").read_bytes()
Path("article.md").write_text("A request may arrive twice. Idempotency uses one identity for the same intended action.",encoding="utf-8")
result={"initial_choices":reachable,"next_choices":next_ready,"grounded":sorted(grounded),"raw_preserved":Path("raw.md").read_bytes()==original}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
