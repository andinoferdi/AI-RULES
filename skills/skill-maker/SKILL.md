---
name: andino-skill-maker
description: Author, evaluate, and maintain executable skills, operational procedures, and runbooks. Use for new capability contracts or observed procedural failures, not passive repository guidance or one-off notes.
---

# Skill Maker: Author and Refine Executable Skills

Internal method ID: `andino-skill-maker` (aliases: `skill-maker`, `method-authoring`, `andino-method-authoring`, `writing-skills`).

## Purpose and prerequisites

Create useful executable guidance under Andino ownership, retaining operational
procedures, human runbooks, pre-commit protocols, and repository governance craft.
Before authoring, read [GUIDE.md](GUIDE.md) and [the supporting contract](resources/contract.md).
Name the consumer task, current contract, authority, acceptance oracle, and mode.
Loading this resource grants no tools, permissions, bootstrap, or second lifecycle.

## 1. Dominant Negative Gates

- Passive project instructions (`CLAUDE.md`, `AGENTS.md`) belong to agent-document-authoring; an executable procedure that audits them can belong here.
- A one-off note or imagined problem without an actual requirement does not justify a skill.
- Prefer a linter, compiler, hook, or schema for mechanically enforceable rules; retain only the judgment or human procedure tooling cannot supply.
- Separate independent concerns when justified. Do not reject required domain craft merely for its shape or length.

## Dual-Mode Authoring Lifecycle

### Mode A: Remedial (failure-driven)

1. Capture the actual wrong action/output, task/context, and observable failure signal.
2. Reproduce it with a realistic no-candidate-guidance control. If the control succeeds or fails differently, investigate before adding speculative rules.
3. Match the repair to the failure: precise boundary/counter, positive recipe, required artifact slot, or observable conditional predicate.
4. Test the candidate on the same task and capabilities in fresh contexts, including variations and negative cases.

### Mode B: Greenfield (capability/invariant-driven)

1. Specify inputs, deliverables, observable success, prerequisites, and negative gates.
2. Identify the required domain craft and write a positive operational recipe.
3. Record an unguided baseline for comparison; a prior failure is not required and must not be invented. A successful baseline can justify a smaller or no new skill.
4. Evaluate candidate capability, variations, and non-triggers against that contract.

### Shared consumer evaluation and refinement

1. Draft a proportional contract covering purpose, triggers/non-triggers, prerequisites, procedure, ownership, permission, output, verification, example, fallback, and provenance. Equivalent headings are valid; no universal FSM/template is required.
2. Keep root coordinator `SKILL.md` strictly <150 lines. Prefer compact member contracts; document any necessary domain-FSM/negative-gate craft exception. This skill's own contract stays <150. Move deep reference into reachable local resources without losing craft.
3. Test consumer use by guidance type: technique application/variation/gaps; pattern recognition/counterexamples; reference retrieval/application; discipline under combined realistic pressure.
4. With an available, authorized evaluator, compare matched control/candidate across several fresh contexts. Inspect actual outputs and false positives, not token scores or rule recital. Use an independent acceptance oracle; self-application is not independent validation.
5. Without an evaluator or independent validation, run explicit walkthroughs and runnable cases; mark model behavior and any unavailable independence NOT_VERIFIED. No forced agents or evaluator swarm.
6. Record variance, evidence identities, limits, and keep/tune/discard decisions in the active task. Rerun affected cases; preserve unaffected evidence and capabilities.

## Ownership, authority, and output

Andino owns selection, shared progress, resource guards, and final status. This
method owns its complete craft and checks; coordinator brevity never removes them.
Use actual tools within existing authority. No user-file deletion, nested agents,
branch/commit/push, publication, installation, external messages, or runtime prompt
fetching is authorized by this skill. No psychological framing overrides the user.
Deliver mode/baseline, minimal guide/resources, independent oracle, consumer-use
evidence, variance, decision, and precise verification limits in the existing task.

## Operational Contract & Verification Harness

This offline metadata example proves only its stated predicates, not model compliance.
Strict/default and root contracts accept 149 and reject 150; members need a documented
`craft_exception` at 150+. `ANDINO_NEGATIVE=1` exercises the actual invalid strict 150
boundary (exit 1). Normal sample is 88 lines (exit 0). Schema details live in the resource.

```python andino-operational-example
import json
import os
import re
import sys

def evaluate_skill_contract(data):
    def invalid(message):
        return {"valid": False, "error": message}

    if not isinstance(data, dict):
        return invalid("Contract data must be an object")
    mode = data.get("mode")
    if mode not in ("remedial", "greenfield"):
        return invalid("Mode must be remedial or greenfield")
    name = data.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"andino-[a-z0-9]+(?:-[a-z0-9]+)*", name):
        return invalid("Name must be a canonical andino- kebab-case ID")
    lines = data.get("contract_lines")
    if type(lines) is not int or lines < 1:
        return invalid("contract_lines must be a positive integer, not a boolean")
    kind = data.get("contract_kind", "strict")
    if kind not in ("strict", "root", "member"):
        return invalid("contract_kind must be strict, root, or member")
    exception = data.get("craft_exception", "")
    if not isinstance(exception, str) or ("craft_exception" in data and not exception.strip()):
        return invalid("craft_exception, when supplied, must be nonempty text")
    if lines >= 150 and (kind != "member" or not exception.strip()):
        return invalid("Strict contracts require <150 lines; members need a craft exception")
    if data.get("has_negative_gates") is not True:
        return invalid("has_negative_gates must be true")
    return {"valid": True, "mode": mode, "status": "CONTRACT_VERIFIED"}

sample_payload = {
    "name": "andino-sample-skill",
    "mode": "greenfield",
    "contract_lines": 88,
    "has_negative_gates": True,
}
if __name__ == "__main__":
    if os.environ.get("ANDINO_NEGATIVE") == "1":
        sample_payload["contract_lines"] = 150
    result = evaluate_skill_contract(sample_payload)
    if not result["valid"]:
        sys.stderr.write(f"Verification failed: {result['error']}\n")
        sys.exit(1)
    print(json.dumps(result, sort_keys=True))
```

## Progressive Disclosure & Provenance

[GUIDE.md](GUIDE.md) owns the full consumer-evaluation procedure; [resources/contract.md](resources/contract.md)
owns record fields, pressure cases, and example-input semantics. All resources are local.
Synthesized from `obra/superpowers:skills/writing-skills/SKILL.md` and Andino dual-mode
authoring. Existing package MIT attribution/notices apply. No upstream bootstrap,
hooks, servers, community policy, or Anthropic best-practices expression is included.
