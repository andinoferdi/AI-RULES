# Audit rubric

Read this when auditing an existing agent document. It gives the five checks, the evidence
each finding cites, the report table, the preservation ledger and a JSON form for tools.

## The five checks

Run every check on every section and record a finding the moment you see it. A check passes
when it has no finding.

### 1. Pointers

- Look for: a pointer buried mid-sentence; the leading word late in the line; synonyms that
  rename one branch; a pointer restating what its target's first paragraph says; a target
  that does not exist; must-have material behind a pointer no step or branch names (dead
  disclosure).
- Evidence: the pointer line, its target path, and whether the target exists.
- Usual fix: one line per pointer, leading word first, one trigger per branch. Pull
  must-have material up a rung, or sharpen the pointer until a branch names it.

### 2. Hierarchy

- Look for: reference only some branches need, inlined between steps; one meaning scattered
  across sections; steps hidden under reference; a document so long that steps compete with
  reference (sprawl).
- Evidence: the branch that needs the material and the branches that do not.
- Usual fix: disclose branch-only reference behind a pointer; co-locate a concept's
  definition, rules and caveats under one heading; split by sequence only when the rush is
  observed.

### 3. Completion criteria

- Look for: a step with no end condition; a subjective end ("looks good", "works
  properly"); a criterion that is clear but forces no legwork.
- Evidence: the step and its current end condition.
- Usual fix: sharpen the bound, then raise the demand ([completion criteria](completion-criteria.md)).

### 4. Wording

- Look for: a prohibition where a target action could be stated; a guardrail with no
  positive path; restatements a leading word would retire; coined labels; weak leading
  words ("be careful").
- Evidence: the sentence.
- Usual fix: state the target behavior; pair each real guardrail with what to do instead;
  collapse restatements into one existing word (table below).

### 5. Pruning

- Look for: one meaning in two places; restated environment facts (scripts, config values,
  directory trees, `--help` output) that one lookup reveals; lines that no longer bear on
  the task or describe behavior that changed (sediment); sentences the model follows by
  default (no-ops); contradictions between the document and its sources.
- Evidence: both copies, or the line and the source it restates with the source's current
  value.
- Usual fix: keep one authoritative copy; delete cheap caches and point at the source; keep
  what the agent cannot find by looking (unwritten conventions, reasons, gotchas no config
  confesses); delete stale and no-op sentences whole; resolve a contradiction from its
  source of truth.

A no-op verdict, and any claim that an edit changes behavior, is a hypothesis until the same
task runs with and without the line. Record it as one.

## Leading words that retire restatements

| Restatement | Leading word |
| --- | --- |
| "fast, deterministic, low-overhead loop" | tight |
| "a failing check you trust before writing code" | red |
| "the one authoritative place this is defined" | SSOT (single source of truth) |
| "a thin end-to-end slice through every layer" | tracer bullet |
| "old guidance nobody removed" | sediment |
| "script-safe, stable command output" | porcelain |
| "keep going until every item is checked" | relentless |

Use a word the consuming agent already knows. A coined term has to be defined and still
recruits no priors.

## Report

| # | Location | Check | Finding (evidence) | Fix | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | AGENTS.md "Codegen", line 3 | Pruning | "Run `npm run codegen` after editing `schema.graphql`" also appears in "Workflow", line 7 | Keep the Codegen copy, delete the other | fixed |

Status is `fixed` (applied), `proposed` (waits for the owner's go-ahead) or `needs decision`
(the owner must choose, or a target or source could not be read).

## Preservation ledger

List every rule of the original once:

| Original rule | Verdict | Where now, or why removed |
| --- | --- | --- |
| Run `npm run codegen` after editing `schema.graphql` | merged | Codegen, step 1 |
| Deploy with `fab deploy` | removed | Stale: no fabfile exists; `.github/workflows/deploy.yml` deploys on merge |

Verdicts are kept, moved, merged and removed. A removed rule always carries its reason.

## JSON form

For tools that consume audits:

```json
{
  "document_path": "AGENTS.md",
  "document_kind": "root-guidance",
  "findings": [
    {"location": "Codegen, line 3", "check": "pruning", "evidence": "duplicate of Workflow, line 7",
     "fix": "keep the Codegen copy", "status": "fixed", "behavior_claim_verified": false}
  ],
  "ledger": [{"rule": "Run codegen after editing schema.graphql", "verdict": "merged",
              "where_or_reason": "Codegen, step 1"}],
  "status": "REVISION_REQUIRED"
}
```

- `document_kind`: root-guidance, skill-body, skill-description, disclosed-reference, router.
- `check`: pointers, hierarchy, completion, wording, pruning.
- `status`: PASS with no findings, REVISION_REQUIRED when findings exist, BLOCKED when a
  finding needs a decision the auditor cannot make.
