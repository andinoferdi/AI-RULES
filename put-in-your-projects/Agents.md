# Project engineering contract

## Core

- User requirements and accepted project constraints determine intended behavior.
  Current source/config/tests determine implementation state; stale memory/docs cannot override them.
- Detect stack, conventions and required checks from this repository. Do not invent paths,
  APIs, commands, branches, versions or runtime configuration.
- Preserve unrelated user edits, data and accepted architecture. Make the minimum correct
  change; reuse existing patterns. Do not weaken checks, swallow errors or add speculative layers.
- Keep credentials out of logs and Git. Back up user config before mutation; prefer reversible
  disable/quarantine. Commit/push/merge/publish/deploy require authorization for that action.
- Search before broad reads; load only relevant source and rule sections. Do not repeatedly
  read already-loaded rules or treat example prompts as active instructions.
- Verify changed behavior and required checks. Report actual evidence and unavailable checks;
  never mark incomplete validation as done. Explain outcome, cause and evidence concisely.

## Ticket state and routing

Use andino-workflow for non-trivial coordination or plan resume. Simple edits may proceed
directly. Non-trivial tickets keep a durable execution plan in the existing project location,
otherwise docs/exec-plans/active/<ticket>.md. Checkpoint material results, decisions and tests;
keep CURRENT STATE, CURRENT PHASE, EVIDENCE and NEXT ACTION concrete. Preserve completed
history; reconcile current source/config drift before resume. Handoff requires only plan
and repository, never chat history or memory. All four supported hosts are primary-capable peers.

Use one relevant methodology per job, directly. No automatic router/bootstrap chain,
capability-manifest execution, UI skill pairing, memory retrieval or subagent swarm.
Same call + same state: reuse result. Retry only transient failures, bounded; break
tool cycles without new evidence. Narrow tool output before loading it into context.

## Lazy domain references

Read only the applicable sections when the task warrants them; do not import this whole list.

| Task | Reference |
| --- | --- |
| Detailed coding constraints | [code-rules](code-rules.md) |
| Frontend behavior/accessibility | [fe-rules](fe-rules.md) |
| Backend/data/API changes | [be-rules](be-rules.md) |
| Git operations | [git-workflow](git-workflow.md); naming/branch tips only as needed |
| Communication style | [chat-rules](chat-rules.md); one language example file only if useful |
| Context/tool waste investigation | [token](token.md) |
| Product/spec authoring | [prd](prd.md), [srs](srs.md), optional BRD only when requested |

Scope each rule to the task; an available template is not an instruction to generate its artifact.
