# Scaffold a course exercise: procedure detail and bounded example

Upstream recipe is conditional for AI Hero course conventions: section 05-memory, exercise 05.02-short-term, explainer/problem/solution readme.md; code-bearing variant main.ts has more than one line. Adapt to the actual course's entry names and validator rather than imposing TypeScript on every lesson.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
base=Path("exercises/05-memory/05.02-short-term")
for variant,text in {"explainer":"# Short-term memory\nExplore retention using a concrete recall task.","problem":"# Recall task\nCompare two provided study sequences.","solution":"# Reference explanation\nExplain the observed sequence difference."}.items():
 p=base/variant; p.mkdir(parents=True); (p/"readme.md").write_text(text,encoding="utf-8")
variants=sorted(p.name for p in base.iterdir())
result={"variants":variants,"nonempty_readmes":all((base/v/"readme.md").stat().st_size>0 for v in variants),"course_linter_run":False}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
