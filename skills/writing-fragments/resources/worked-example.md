# Collect raw writing fragments: procedure detail and bounded example

A fragment need not be cold-reader complete; it needs to carry something the author may reuse. A leading word can organize later writing, but raw collection does not decide the article's thesis. One shared file is acceptable for this user-authored raw pile; parallel agents must not write it concurrently.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
p=Path("fragments.md"); p.write_text("# Working title\n\nUser-edited opening.",encoding="utf-8")
before=p.read_text(encoding="utf-8")
new="A retry is a second delivery of one intention."
p.write_text(before+"\n\n---\n\n"+new+"\n",encoding="utf-8")
result={"opening_preserved":p.read_text(encoding="utf-8").startswith(before),"fragments":2,"outline_added":False}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
