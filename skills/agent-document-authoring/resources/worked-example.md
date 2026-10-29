# Write documents agents can use: worked procedure, case study, and verification

This resource provides an end-to-end transformation case study, an empirical diagnostic audit rubric, and a deterministic verification procedure for `agent-document-authoring`.

---

## Worked case study: Before and after transformation

### The problem: A bloated, sediment-heavy deployment guide (Before)
Below is a common failure mode observed in real agent instruction files:

```markdown
<!-- BEFORE: Monolithic, negated, fuzzy bounds, environment-shadowing -->
# Deployment Guide
Please be thorough and make sure you do a great job deploying the app.
DO NOT deploy if tests are failing. DO NOT deploy on Fridays unless authorized.
Never forget to check environment variables.
To run tests, type `npm test`. To check git status, type `git status`.
Steps:
1. Understand the code and make sure everything looks good.
2. Run the tests.
3. If this is a Docker build, create Dockerfile, configure multi-stage builds, setup Alpine Linux base, install dependencies, copy package.json, expose port 3000... (30 lines of Docker instructions inlined here).
4. Deploy the build.
5. Check if the deployment works properly.
```

### Flaws identified:
1. **Fuzzy completion criteria:** "Make sure everything looks good" and "check if deployment works properly" are subjective bounds that trigger premature completion.
2. **Negation trap:** Multiple prohibitions (*DO NOT deploy*, *Never forget*) activate the forbidden state in model attention without specifying positive paths.
3. **Environment shadowing / Cache waste:** Explaining `npm test` and `git status` repeats what the environment already tells the agent for free.
4. **Information hierarchy collapse / Sprawl:** 30 lines of branch-specific Docker details buried the sequential deployment flow for all other users.
5. **No-ops:** "Please be thorough" is a zero-yield no-op that the model already attempts by default.

---

### The solution: Stratified, positively steered, demanding guide (After)

```markdown
<!-- AFTER: Stratified, demanding completion bounds, positive steering, disclosed branch -->
# Production deployment procedure

Ordered execution sequence for production deployment.

## Procedure

1. Verify test suite: run `npm test`. Done when test runner exits 0 with zero failing assertions.
2. Inspect working tree: ensure working directory is clean. Done when `git status --porcelain` produces zero output lines.
3. Build artifact:
   - For standard Node builds: execute `npm run build`. Done when `dist/server.js` exists.
   - For containerized builds: consult [`docker-build.md`](#docker-build). Read only when building container targets.
4. Execute release: trigger deployment pipeline via `npm run deploy:prod`. Done when output confirms production deployment ID and HTTP health probe returns 200 OK.
```

### Improvements achieved:
- **Zero no-ops:** Deleted "be thorough" and environment restatements.
- **Positive steering:** Replaced negative bans with explicit pre-conditions ("Done when test runner exits 0").
- **Progressive disclosure:** Moved containerization detail behind a cleanly worded context pointer loaded only for container runs.
- **Demanding completion bounds:** Every single step has an observable, falsifiable success criterion.

---

## 5-Point diagnostic self-audit rubric

Before releasing any agent-facing guide or skill, evaluate each line against this rubric:

| Dimension | Question to Ask | Pass Condition | Failure Mode to Fix |
| :--- | :--- | :--- | :--- |
| **1. Pointer Integrity** | Does the pointer front-load the leading word and isolate one branch? | Pointers front-load core token; synonyms collapsed; local path valid. | Trigger lists buried in prose; identical branch listed under 3 synonyms. |
| **2. Information Hierarchy** | Are sequential steps separated from flat reference? | Sequential actions sit in primary tier; specialized reference disclosed behind pointer. | Inlined edge cases burying execution steps (Sprawl). |
| **3. Completion Bounds** | Can the agent distinguish done from not-done with certainty? | Bound is checkable, observable, and forces thorough legwork. | Fuzzy criteria ("check carefully", "ensure quality") causing premature completion. |
| **4. Positive Formulation** | Are instructions framed as target actions rather than bans? | Positive actions prompted; negations restricted to absolute safety gates. | Negation cascade ("do not do X, never do Y") triggering the elephant in context. |
| **5. Pruning & No-Ops** | Does every line actively change agent behavior? | Environment data not cached; zero dead sediment; zero default model no-ops. | Restating `package.json` scripts, `--help` menus, or generic pleasantries. |

---

## Deterministic verification example

This bounded example demonstrates deduplication of instruction meanings, progressive disclosure of branch references, and the generation of verifiable consumer guides. It uses only Python's standard library and executes in isolation.

The repository checker (`scripts/check_andino_matt_methods.py --runtime-root <package>`) executes this exact code block inside a clean `TemporaryDirectory` and independently verifies the semantic results.

```python
from pathlib import Path
import json
entries=[{"meaning":"use actual repo commands","kind":"action"},{"meaning":"use actual repo commands","kind":"duplicate"},{"meaning":"TS-specific fixture examples","kind":"branch-reference"}]
unique=[]
for e in entries:
 if e["meaning"] not in [x["meaning"] for x in unique]: unique.append(e)
Path("consumer-guide.md").write_text("1. Discover the repository test command; done when its actual definition is located.\nTS fixture migration: read the local fixture reference only for TypeScript tests.",encoding="utf-8")
result={"meanings":len(unique),"duplicate_removed":1,"branch_reference":"TS-specific fixture examples","live_model_verified":False}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

Inspecting `consumer-guide.md` and `result.json` proves:
1. Duplicate meanings are detected and pruned down to single sources of truth.
2. Branch-specific reference ("TS-specific fixture examples") is disclosed behind a targeted condition.
3. Sequential actions end on explicit observable bounds ("done when its actual definition is located").
4. Deterministic local execution validates structural integrity without relying on unverified external networks or live model routing assumptions.
