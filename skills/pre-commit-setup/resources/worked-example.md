# Prepare project pre-commit checks: procedure detail and bounded example

Optional Node recipe: lint-staged with prettier --ignore-unknown --write for staged matching files, then actual typecheck/test scripts. Husky syntax varies by installed version; inspect current docs/version before implementation. Full tests may be inappropriate per commit in large repos; respect existing quality policy instead of hardcoding every check.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
scripts={"prepare":"build-tools","typecheck":"tsc --noEmit","test":"test-runner"}
prepare=scripts["prepare"]+" && husky"
hook=["lint-staged"]+[f"npm run {n}" for n in ("typecheck","test") if n in scripts]
Path("proposed-hook.txt").write_text("\n".join(hook),encoding="utf-8")
result={"prepare":prepare,"hook":hook,"index_touched":False,"package_execution":False}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
