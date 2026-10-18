# Design a deep module: procedure detail and bounded example

Example: calculateShipping(order, rates) hides rate lookup and zone matching behind one domain result. Locality improves only if callers stop repeating policy. Compare a minimal quote(order), an extensible quote(order, policies), and a common-case standardQuote(order); record costs rather than declaring fewer methods universally better. Internal parts may remain small and swappable without entering the public interface.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
designs=[{"name":"minimal","entrypoints":1,"behaviors":6,"adapters":["production","test"]},{"name":"flexible","entrypoints":5,"behaviors":6,"adapters":["production"]}]
viable=[x for x in designs if len(x["adapters"])>=2]
Path("interface.md").write_text("quote(order) -> Quote\nErrors: unsupported destination\nInvariant: cents >= 0\nHidden: zone policy and rate matching",encoding="utf-8")
result={"selected":viable[0]["name"],"public_behaviors":viable[0]["behaviors"],"hypothetical_seams":[x["name"] for x in designs if len(x["adapters"])<2]}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
