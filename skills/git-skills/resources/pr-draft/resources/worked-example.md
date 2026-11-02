# Describe a pull request: procedure detail and bounded example

Default sections when no project template exists: Summary, Evidence with Before/After, Merge Danger with Door/Blast Radius. Nonvisual changes use exact test or console evidence. Retain source attribution in [credits.md](credits.md): the visual menu is adapted from Dex Horthy / Humanlayer show-me, via the audited Matt source.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
before="duplicate request creates 2 invoices"
after="duplicate request returns original invoice"
body="# Summary\ncreate_invoice(request_id) -> existing or new Invoice\n\n# Evidence\nBefore: "+before+"\nAfter: "+after+"\n\n# Merge Danger\nDoor: two-way before external invoice delivery\nBlast radius: billing retries\n"
Path("pr-body.md").write_text(body,encoding="utf-8")
result={"before":before,"after":after,"risk":"billing retries","published":False}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
