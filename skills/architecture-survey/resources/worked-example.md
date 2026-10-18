# Survey architecture friction: procedure detail and bounded example

Offline report pattern: semantic article per candidate, file list, recommendation/dependency badges, two columns with inline SVG or plain boxes and arrows, concise problem/solution/wins, optional ADR callout. Escape all source names/text. Use no external scripts, fonts, trackers or securityLevel loose. A diagram that requires a paragraph to decode should be simplified.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
from html import escape
candidate={"name":"Order intake","files":["handler.py","policy.py"],"before":["handler -> policy","caller repeats validation"],"after":["submit_order -> Receipt"],"strength":"Strong"}
body=f"<h1>{escape(candidate['name'])}</h1><h2>Before</h2><pre>{escape(chr(10).join(candidate['before']))}</pre><h2>After</h2><pre>{escape(chr(10).join(candidate['after']))}</pre><p>Tests: one public submit seam</p>"
Path("architecture.html").write_text("<!doctype html><meta charset='utf-8'><style>body{font:18px sans-serif;max-width:55rem;margin:2rem auto}pre{white-space:pre-wrap}</style>"+body,encoding="utf-8")
result={"candidate":"Order intake","strength":"Strong","external_assets":[],"product_edits":[]}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
