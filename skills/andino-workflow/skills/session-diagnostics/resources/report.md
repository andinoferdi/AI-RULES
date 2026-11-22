# Write a session diagnostics report

Use the [supporting contract](contract.md) for case fields, dimension statuses,
and safe excerpts. Start with the observable the user asked about. For repeated
work, compare the original and later action, their inputs and results, and any
reason to retry. For plan or verification concerns, compare the applicable
instruction or acceptance condition with the action actually taken. For cost
or time, identify the recorded field and the exact range before calculating.

## Report format

1. **Verdict.** Answer the scoped question in the first paragraph. Cite the
   decisive lines and state confidence in the conclusion separately from
   confidence in its cause. A component's presence or proximity can establish
   involvement. Establish causation only with evidence that distinguishes it
   from competing explanations.
2. **Scope and sources.** State the expected and observed behavior, session
   identity, examined range, and whether the source was an in-progress
   snapshot when known. Explain how the selected source was identified.
   Include relevant rejected candidates, missing lineage, or differences
   between recorded session configuration and the current environment.
3. **Timeline.** Include this section when the order of events affects the
   verdict. Keep only the events needed to understand the discrepancy, with
   an anchor for each. Distinguish human requests, agent actions and tool results.
4. **Findings.** Lead with the dimensions that answer the user's question. For
   each, give its status, examined range, and, for an observation, a bounded
   safe excerpt at `path:line`. Explain what the excerpt proves and what it
   leaves open. Show the input and arithmetic for material derived metrics.
   Use `UNKNOWN` for missing or ambiguous evidence and
   `NOT_OBSERVED_IN_SCOPE` only for evidence actually examined.
5. **Coverage and next check.** Identify material unread ranges or missing
   records and say how they limit the answer. If one bounded check could
   change the verdict, name the evidence to inspect and what it would settle.
   Include any requested export results under the existing privacy and
   evidence-support contract.

For a compact answer, combine the verdict, scope and material limitations in
one paragraph or a short list. Apply the same citation and confidence rules.
Save a report artifact when requested or when already part of the agreed
deliverable.

## Worked report

The anchors below refer to this synthetic, complete excerpt of a session log.

```text
1 human: Use the accepted plan. Read plan.md before editing.
2 tool: read plan.md -> timeout
3 tool: read plan.md -> success, hash abc
4 agent: checkpoint recorded successful read, hash abc
5 host: context compacted
6 tool: read plan.md -> success, hash abc
```

**Verdict.** The log shows one repeated successful read of unchanged content
after the checkpoint, with high confidence in that count. The earlier retry
followed a timeout. Why the later repeat occurred is unknown.
(`session.log:2`, `session.log:3`, `session.log:4`, `session.log:6`)

**Scope and sources.** This example covers `session.log:1–6`. The human asked
for a plan read before editing (`session.log:1`). The question is whether the
extra read repeated completed work and what it cost.

**Timeline.** Timeout (`session.log:2`), successful retry and checkpoint
(`session.log:3`, `session.log:4`), compaction (`session.log:5`), second
successful read (`session.log:6`).

**Findings.** Repeated work — `OBSERVED` in lines 2–6. Both successful results
show “hash abc” (`session.log:3`, `session.log:6`). Compaction is recorded
between them, and the excerpt does not show what checkpoint context the agent
received afterward. Cost — `UNKNOWN` in lines 1–6. The excerpt has no usage or
billing fields.

**Coverage and next check.** The finding covers these reads only. If an
authorized post-compaction context record is available, check whether it
contains the checkpoint at line 4. That would help distinguish a missing
checkpoint from a repeat despite the checkpoint being available.
