# Classify Git operation authority: procedure detail and bounded example

Original hook misses git -C directory push and many option spellings; it is excluded as enforcement. The worked example classifies tokenized direct Git argv only. It deliberately does not parse shell strings, aliases, pipes, subcommands with unknown effects or every Git option; those return review-required, never safe. This limited fixture is not a replacement security parser.

## Run the example

This example uses only Python's standard library and writes inside the current working directory. Read the code, then run it only in a fresh disposable directory. The main repository's `scripts/check_andino_matt_methods.py --runtime-root <package>` executes this exact block in a TemporaryDirectory and independently checks the semantic results. No project files, index, external services or credentials are needed.

```python
from pathlib import Path
import json
def classify(argv):
 if not argv or argv[0]!="git": return "review-required"
 i=1
 while i<len(argv) and argv[i]=="-C": i+=2
 if i>=len(argv): return "review-required"
 command=argv[i]; args=argv[i+1:]
 if command in {"push","clean","commit","add","merge","rebase"}: return "requires-authority"
 if command=="reset" and "--hard" in args: return "requires-authority"
 if command in {"status","diff","log"}: return "read-only"
 return "review-required"
cases=[["git","status"],["git","-C","repo","push"],["git","reset","--hard"],["git","-C"]]
verdicts=[classify(c) for c in cases]
Path("git-review.json").write_text(json.dumps(verdicts),encoding="utf-8")
result={"verdicts":verdicts,"executed_mutations":[]}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspect both generated artifact(s) and `result.json`. The result is a bounded operational example for the procedure above; it does not simulate or assert model auto-activation. External CLI, browser rendering, TypeScript resolution, human decision quality and unavailable host behavior remain separate checks.
