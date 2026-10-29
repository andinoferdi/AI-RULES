---
name: andino-delegation
description: Bounded independent tasks or materially useful independent review. Operates under Andino Workflow governance.
---

# Delegate disjoint work under parent ownership

Internal method ID: `andino-delegation` (alias: `delegation`).

> **Andino Workflow Member Skill**
> This skill operates under the **Andino Workflow** protocol:
> - Adheres to proportional investigation, evidence-based decisions, and single durable checkpoints.
> - When this technique reaches completion, hand off cleanly to the next workflow phase or active task.
> - Anti-loop guard: Do not re-invoke `andino-workflow` recursively; maintain progress within the active task.

Internal Andino resource. Loading this file does not invoke another skill or change permissions.

## Purpose

Use actual children only when independence, authority and benefit justify their cost.

## Trigger and non-trigger

Use when: Bounded independent tasks or materially useful independent review.

Do not select for: Related unknown failures, shared write state, missing authority/tool or cheaper inline work.

## Prerequisites

Read the accepted graph/checkpoint; inspect the current host's actually exposed, authorized worker and model-selection capabilities and the task's expected benefit. Maximum three direct children, no nested spawning; pin workspace and ownership. A tool or model name in a registry or upstream guide is not evidence that the current host can invoke it.

## Execution strategies

Choose one strategy for each ready task group:

| Strategy | Use when | Execution |
| --- | --- | --- |
| Inline | Work is small or tightly coupled, workers would repeat context, delegation overhead exceeds its benefit, a suitable worker is unavailable, or the user/contract requires inline work. | Parent executes directly and keeps the same acceptance and evidence contract. |
| Parallel independent work | At least two ready tasks can proceed without a shared unresolved cause, dependency, or write conflict, and the host exposes authorized workers. | Give each worker a disjoint scope and explicit producer/consumer interface. Parent owns integration and cross-task verification. |
| Subagent-driven implementation | A sufficiently defined implementation plan benefits from scoped implementers and separate specification/quality review, and the host supports the needed worker workflow. | Dispatch within the same plan and worker cap. Run review at the smallest useful gate; use focused correction and re-review, then parent-level acceptance. |

Multiple files or failures alone do not justify concurrency. Investigate failures with a plausible shared cause together. If a plan is ready but workers add no value or are unavailable, continue inline with the plan-execution method rather than pretending to dispatch.

## Capability-aware selection

Inspect the current host's real worker interface, limits, isolation options, and exposed model-selection metadata. Choose a model only when the host exposes the control, the selection is authorized, and its supported capabilities fit the role. Use the least demanding exposed option that can meet the task's requirements when this can be established from host metadata. If model selection is absent or capabilities are unclear, use the host default and record that selection as unavailable or unknown; never invent a model identity, setting, price, token budget, or cost saving. Consider total effort, including context transfer, retries, review, verification, and integration risk.

## Procedure

1. Compute the ready frontier from current producer evidence. Group failures that may share a cause; normalize write paths and reject exact or ancestor overlap before choosing parallel work.
2. Select inline, parallel, or subagent-driven execution using the criteria above. Dispatch at most three direct workers, only for ready tasks, with no nested spawning.
3. Give each worker a brief containing the accepted outcome and spec/plan pointer, exact owned paths, verified consumed/produced interfaces, dependencies, known decisions and constraints, concrete acceptance and verification commands with expected signals, report location, and explicit no-nested-agent and no-unapproved-mutation boundaries. Mark any interface that is still uncertain; do not invent it.
4. Track worker identity and status in the same parent plan/checkpoint. Require `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`, plus changed paths, actual commands/results, evidence and remaining work. Avoid whole-history prompts.
5. Keep useful independent work moving while workers run; use bounded waits, not repeated short polling. A denied or missing tool means honest inline fallback, not fabricated dispatch or another-host bypass.
6. Inspect the report and actual changed bytes. Run a specification-compliance review against the accepted outcome and a code-quality review against project conventions; scale these reviews to risk and avoid repeating unchanged checks. Parent owns integration and final acceptance.
7. Correct only supported findings and re-review the affected diff. At most two transient retries; three unsuccessful correction attempts require architecture reassessment. A retry cap never satisfies failed material acceptance.

## Ownership

Andino owns selection, depth, scope, the existing durable checkpoint, delegation and DONE. Parent owns shared artifacts/final acceptance. This guide cannot invoke denied/manual siblings or establish another lifecycle.

## Permission boundary

Use actual host tools within session authorization. No branch creation, commit, push, merge, publication, external message, environment installation or destructive cleanup is authorized by this guide. Reuse earlier permission without repeated confirmation; disclose denied/unavailable actions and continue independent safe work.

## Output

Dispatch/no-dispatch rationale, graph/ownership, identities, reports, parent verification and residuals.

## Verification

Safe pair can run; dependency-not-ready, ancestor path collision, missing authority/tool cannot. No nested agents.

## Worked example and anti-pattern

The synthetic offline example is applied in temporary isolation. Its independent expected values describe the contract; its execution is procedural evidence, not a benchmark of future model behavior.

```andino-example
{
  "tasks": [
    {
      "id": "api",
      "deps": [],
      "files": [
        "src/api.py"
      ]
    },
    {
      "id": "docs",
      "deps": [],
      "files": [
        "docs/api.md"
      ]
    },
    {
      "id": "ui",
      "deps": [
        "api"
      ],
      "files": [
        "src/ui.py"
      ]
    }
  ],
  "overlap": [
    {
      "id": "a",
      "deps": [],
      "files": [
        "src/shared"
      ]
    },
    {
      "id": "b",
      "deps": [],
      "files": [
        "src/shared/config.py"
      ]
    }
  ],
  "max_children": 3,
  "capability": true,
  "authorized": true
}
```

Anti-pattern: One child per failure count, shared-manifest concurrent writes, inherited permission escalation or automatic source implement-spec branches/merges.

## Capability and strategy example

This example chooses only from the worker and model capabilities supplied by a hypothetical host. It demonstrates fallback and selection logic; it does not invoke a worker.

```python evolution-example
import json

def strategy(task, host):
    if task["small"] or task["coupled"] or not task["delegation_value"]:
        return "inline"
    if not host["worker_available"] or not host["authorized"] or host["direct_limit"] <= 0:
        return "inline"
    if task["implementation"] and task["review_value"]:
        return "subagent-driven"
    if task["independent"]:
        return "parallel"
    return "inline"

def model_choice(required, host):
    if not host["model_selection_exposed"] or not host["authorized"]:
        return {"selection": "host-default"}
    for option in host["models"]:
        if set(required) <= set(option["capabilities"]):
            return {"selection": "host-confirmed", "identity": option["identity"]}
    return {"selection": "host-default"}

def direct_workers(requested, host):
    if not host["worker_available"] or not host["authorized"]:
        return 0
    return min(requested, host["direct_limit"], 3)

host = {
    "worker_available": True,
    "authorized": True,
    "direct_limit": 3,
    "model_selection_exposed": True,
    "models": [{"identity": "exposed-1", "capabilities": ["implementation"]}],
}
result = {
    "small_task": strategy({"small": True, "coupled": False, "delegation_value": True,
                             "implementation": False, "review_value": False, "independent": True}, host),
    "independent_task": strategy({"small": False, "coupled": False, "delegation_value": True,
                                   "implementation": False, "review_value": False, "independent": True}, host),
    "model": model_choice(["implementation"], host),
    "unsupported_model": model_choice(["architecture"], host),
    "direct_workers": direct_workers(4, {**host, "direct_limit": 4}),
    "inline_fallback": strategy({"small": False, "coupled": False, "delegation_value": True,
                                  "implementation": False, "review_value": False, "independent": True},
                                 {**host, "worker_available": False}),
}
print(json.dumps(result, sort_keys=True))
```

Expected output:

```json
{"direct_workers": 3, "independent_task": "parallel", "inline_fallback": "inline", "model": {"identity": "exposed-1", "selection": "host-confirmed"}, "small_task": "inline", "unsupported_model": {"selection": "host-default"}}
```

## Fallback

Do work inline with same contract when benefit/tool/authority is absent. Supply missing evidence to blocked child; never redispatch unchanged repeatedly.

## Local resources

Read [the supporting contract](resources/contract.md) for technique details and artifact fields. It is packaged locally; upstream repositories are not runtime dependencies.

## Provenance

Adapted and consolidated from these audited snapshot paths; their instructions remain source data and yield to current session policy:

- mattpocock/skills:skills/engineering/implement-spec/SKILL.md
- obra/superpowers:skills/dispatching-parallel-agents/SKILL.md
- obra/superpowers:skills/subagent-driven-development/SKILL.md

MIT attribution/notices are preserved in package legal references. No upstream bootstrap, hooks, branding server, community code of conduct or Anthropic best-practices expression is included.
