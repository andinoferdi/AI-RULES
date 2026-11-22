---
name: andino-skill-maker
description: Use when authoring, evaluating, or maintaining executable skills, operational runbooks, or pre-commit protocols. Operates under Andino Workflow governance.
---

# Skill Maker: Author and Refine Executable Skills

Internal method ID: `andino-skill-maker` (aliases: `skill-maker`, `writing-skills`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow protocol: single durable checkpoint, proportional investigation, anti-loop guards.
> Loading this file does not invoke another skill or mutate repository state. Upstream references yield to current policy.

## 1. Dominant Negative Gates (When NOT to Use)

Reject skill creation immediately if ANY condition holds:
- **Passive Repository Guidance**: Instructions for `CLAUDE.md` or `AGENTS.md` belong to `agent-document-authoring`.
- **Mechanically Enforceable**: Rules enforceable via linter, compiler, type checker, or schema belong in automated tooling.
- **One-Off / Hypothetical**: Solutions to one-time issues or imagined problems without a demonstrated need.
- **Narrative Retrospective**: Documenting past session history rather than an active, reusable decision procedure.

## 2. Dual-Mode Operational Triage Router

| Mode | Selection Trigger | Operational Protocol |
| :--- | :--- | :--- |
| **Mode A: Remedial** (Failure-Driven) | Observed agent error, prompt deviation, or rule violation under pressure. | **Documentation TDD**: Run baseline without skill, record verbatim excuses, author minimal counter, verify compliance under pressure. |
| **Mode B: Greenfield** (Invariant-Driven) | New capability, operational runbook, or multi-step coordination protocol. | **Invariance Enforcement**: Declare floor invariants, assess unguided baseline, write minimal contract, verify boundary adherence. |

## 3. The 5 Floor Invariants

1. **Iron Law of Verification (TDD for Docs)**: Run an unguided baseline before introducing a behavioral rule. If it passes, retain existing guidance. A source walkthrough can justify correcting a demonstrable contract defect, with behavior still NOT_VERIFIED.
2. **SDO Isolation**: Frontmatter description defines triggering conditions ONLY. Never summarize the internal workflow, or agents will skip reading the skill.
3. **Match Form to Failure**: Prohibitions for discipline failures under stress; positive recipes for output shaping; structural slots for omissions.
4. **Zero Nuance Clauses**: Escape clauses (*"unless needed"*) reopen negotiation. Express exceptions as falsifiable branches on observable predicates.
5. **Single Great Example**: One complete, runnable, production-grounded example beats shallow multi-language dilution.

## 4. Anti-Rationalization Refutations

| Rationalization Shortcut | Mechanical Reality & Required Response |
| :--- | :--- |
| *"The skill is obviously clear; no need to test it."* | Clear to author != clear to other models under pressure. Run the baseline test first. |
| *"I will write the skill first, then write the test."* | Writing guidance before observing failure guarantees speculative rules and token bloat. |
| *"I summarized the workflow in description so agents know it works."* | Summaries leak workflow; models take the shortcut and bypass the full skill body. |
| *"A negative rule ('never do X') is enough to shape the output."* | Prohibitions backfire on shaping problems and increase unwanted tokens. Use a positive recipe. |
| *"I'll add 'unless necessary' to keep the rule flexible."* | Nuance clauses destroy compliance. State legitimate exceptions as explicit conditional branches. |

## 5. Diagnostic Red Flags (Stop Immediately)

1. Treating a walkthrough or metadata check as an observed consumer baseline.
2. Summarizing internal steps or workflow in the frontmatter `description`.
3. Using negative prohibitions to fix output structure instead of a positive recipe.
4. Adding an *"unless..."* or *"except when..."* clause to an operational rule.
5. Providing three shallow code examples in different languages instead of one deep, runnable example.
6. Embedding executable shell or code logic inside diagram nodes.

## Procedure

1. Write the brief before changing the skill. Name the consumer, task, trigger,
   near miss, required output and authority boundary. State reversible assumptions
   and resolve any ambiguity that changes the artifact or permitted action.
2. Define acceptance before running the task. Specify observable actions,
   deliverable contents and forbidden side effects. Use the same task, tools and
   authority for the unguided control, current skill (for revisions) and candidate.
3. Use the evidence to select the smallest change. For a repeated failure,
   reproduce it and preserve behaviors that already pass. For a new skill,
   identify the invariant the unguided control misses. If the controls meet the
   requirements, retain the existing guidance.
4. Write the procedure around the consumer's decisions and output. Give exact
   preconditions, actions, output fields and stop conditions where the cost of
   guessing is high. Put longer examples and infrequent branches in local
   resources linked from the step that needs them.
5. Check discovery, task performance and packaging separately. Probe a trigger
   and a near miss, inspect completed artifacts against the oracle, and resolve
   referenced resources from the installed entrypoint when distribution is in
   scope. If independent trials are unavailable or unauthorized, use a bounded
   walkthrough to identify contract defects and report behavior as NOT_VERIFIED.

## Resources

- Complete authoring methodology and evaluation craft: [GUIDE.md](GUIDE.md)
- Skill Discovery Optimization (SDO) and keyword engineering: [resources/sdo-and-discovery-protocols.md](resources/sdo-and-discovery-protocols.md)
- Failure-form matching matrix and loophole closing: [resources/failure-form-matching-and-bulletproofing.md](resources/failure-form-matching-and-bulletproofing.md)
- Pressure scenario design, micro-tests, and TDD documentation: [resources/subagent-testing-and-pressure-scenarios.md](resources/subagent-testing-and-pressure-scenarios.md)
- Degrees of freedom, token budgeting, and anti-patterns: [resources/anthropic-craft-and-degrees-of-freedom.md](resources/anthropic-craft-and-degrees-of-freedom.md)
- Canonical authoring templates for skills and runbooks: [resources/worked-examples-and-templates.md](resources/worked-examples-and-templates.md)
- Evaluation record schemas and oracle contracts: [resources/contract.md](resources/contract.md)

## 7. Runnable Operational Contract & Verification Harness

```python andino-operational-example
import json, os, re, sys

def evaluate_skill_contract(data):
    if not isinstance(data, dict): return {"valid": False, "error": "Contract must be a dict"}
    mode = data.get("mode")
    if mode not in ("remedial", "greenfield"): return {"valid": False, "error": "Invalid mode"}
    name = data.get("name", "")
    if not isinstance(name, str) or not re.fullmatch(r"andino-[a-z0-9]+(?:-[a-z0-9]+)*", name): return {"valid": False, "error": "Invalid name"}
    lines = data.get("contract_lines")
    if type(lines) is not int or lines < 1: return {"valid": False, "error": "contract_lines must be positive int"}
    kind = data.get("contract_kind", "strict")
    if kind not in ("strict", "root", "member"):
        return {"valid": False, "error": "Invalid contract kind"}
    exception = data.get("craft_exception", "")
    has_exception = isinstance(exception, str) and bool(exception.strip())
    if lines >= 150 and (kind != "member" or not has_exception):
        return {"valid": False, "error": "Strict contracts require <150 lines"}
    if data.get("has_negative_gates") is not True: return {"valid": False, "error": "Missing negative gates"}
    if data.get("has_sdo_isolation") is not True: return {"valid": False, "error": "Missing SDO isolation"}
    return {"valid": True, "mode": mode, "status": "CONTRACT_VERIFIED"}

if __name__ == "__main__":
    is_neg = os.environ.get("ANDINO_NEGATIVE") == "1"
    payload = {
        "name": "andino-sample-skill",
        "mode": "greenfield",
        "contract_lines": 150 if is_neg else 98,
        "has_negative_gates": True,
        "has_sdo_isolation": True,
    }
    result = evaluate_skill_contract(payload)
    if not result["valid"]:
        sys.stderr.write(f"Verification failed: {result['error']}\n")
        sys.exit(1)
    print(json.dumps(result, sort_keys=True))
    sys.exit(0)
```

## 8. Provenance

Synthesized from `obra/superpowers:skills/writing-skills`, Anthropic official Skill Best Practices, and Andino dual-mode authoring. Preserved under MIT license terms in [references/license.md](references/license.md).
