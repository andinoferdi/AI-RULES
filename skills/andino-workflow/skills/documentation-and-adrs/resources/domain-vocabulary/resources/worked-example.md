# Sharpen domain terms: procedure detail and bounded example

Glossary format: context summary, Language, bold canonical term, tight definition, Avoid aliases. Multiple contexts earn a root map listing paths and their relationships; do not split a bloated glossary before pruning implementation detail. Optional ADR fields are status, rejected alternatives and non-obvious consequences. A rejection is recorded only when its reason prevents a future mistaken recommendation.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
terms={"Order":{"definition":"A customer's accepted request for goods.","avoid":["Purchase"]},"Invoice":{"definition":"A request for payment after delivery.","avoid":["Bill"]}}
aliases={a:k for k,v in terms.items() for a in v["avoid"]}
names=["Purchase","Invoice","Order"]
canonical=[aliases.get(n,n) for n in names]
Path("GLOSSARY.md").write_text("\n\n".join(f"**{k}**: {v['definition']}\n_Avoid_: {', '.join(v['avoid'])}" for k,v in terms.items()),encoding="utf-8")
result={"canonical":canonical,"distinct_terms":len(terms),"implementation_details":[]}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
