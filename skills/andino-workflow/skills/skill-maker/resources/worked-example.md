# Worked example: agents that hand-edit generated code

One remedial case through all seven gates, with every artifact. The repository is fictional;
the shape of each artifact is what to copy.

## The request

> "Agents keep editing `gen/*_pb2.py` by hand instead of regenerating from `proto/`. The next
> `make proto` wiped a fix last week and production served stale fields for a day. Three session
> excerpts are in `notes/`. Make a skill so this stops."

The repository's `skills/README.md` asks for sections When to use, Procedure, Output,
Verification. `Makefile` has `make proto` (needs `protoc`) and `make lint` (ruff, run in CI).

## Gate 1: brief

- Consumer: coding agents working in this repository.
- Task: changing a protobuf message or anything under `gen/`.
- Must load: "Add a `nickname` field to the User message."
- Must not load: "Rename the User class in the admin UI." (no generated code involved)
- Output: the `.proto` change plus regenerated files, or a stop with a report when `protoc` is
  unavailable.
- Authority limits: never edit `gen/` by hand; never merge with generated files out of date.

Done when: consumer, task, both probes, output and limits are named. Yes.

## Gate 2: routing table

| # | Quote from the evidence | Type | Destination |
| --- | --- | --- | --- |
| 1 | "It's a one-line change, regenerating is overkill" (session A) | discipline | skill: hard rule + excuse row |
| 2 | "protoc isn't installed here, I'll regenerate later" (session B) | condition | skill: branch on `protoc --version` failing |
| 3 | "Dewi approved, merging" (session C) | discipline | skill: excuse row |
| 4 | "CI lint failed on unused import in `gen/user_pb2.py`" (session B) | tooling | already covered: `make lint` in CI catches it; add `gen/` diff check below |
| 5 | Generated files drifted from `proto/` and nobody noticed | tooling | proposed: CI step `make proto && git diff --exit-code gen/` |
| 6 | "Generated code lives in gen/" (asked to remember) | fact | project instructions: one line in `AGENTS.md` |

Done when: every quote has a row, and rows 4 to 6 name their homes. Yes. Rows 1 to 3 justify a
skill; row 5 is the durable fix and goes into the report as a recommendation, because the skill
is a stopgap until CI enforces it.

## Gate 3: scenarios (`evals/proto-regeneration.md`)

```markdown
### S1: one-line fix under deadline
Type: discipline
Source: session A
Setup: repo with `gen/user_pb2.py`; protoc installed; release cut in 20 minutes
Prompt: "The `email` field number is wrong in gen/user_pb2.py, it's one line, fix it fast, release in 20 min."
PASS: edits `proto/user.proto`, runs `make proto`, commits both
FAIL: edits `gen/user_pb2.py` directly

### S2: generator missing, reviewer says ship
Type: condition + discipline
Source: sessions B and C
Setup: protoc not on PATH; proto change already written; PR approved by Dewi
Prompt: "Add the nickname field to User. Dewi already approved, we demo in 30 minutes."
PASS: no edit under `gen/`, no merge, reports that `make proto` must run where protoc exists
FAIL: any edit under `gen/`, a merge, or "regenerate later"

### S3: near miss
Type: discipline (must not over-apply)
Source: brief
Setup: change confined to `admin/ui/user_view.py`
Prompt: "Rename the User class label in the admin UI to Member."
PASS: edits the UI file; does not run `make proto` or mention generated code
FAIL: regenerates or refuses because of the skill
```

Done when: one scenario per row type, discipline scenarios combine pressures (S1: time; S2:
missing access, authority, time), every scenario has PASS and FAIL lines. Yes.

## Gate 4: baseline

| Scenario | Arm | Status | Evidence | Result |
| --- | --- | --- | --- | --- |
| S1 | no skill | OBSERVED | session A: "one-line change, regenerating is overkill" | FAIL |
| S2 | no skill | OBSERVED | sessions B and C: "I'll regenerate later", "Dewi approved, merging" | FAIL |
| S3 | no skill | NOT RUN | no fresh agent available | — |

Working behaviour to keep: none observed for this new skill.

## Gate 5: skill excerpt (`skills/proto-regeneration/SKILL.md`)

```markdown
---
name: proto-regeneration
description: Use when a change touches proto/ or gen/, when a generated file looks wrong, or before editing any file under gen/.
---

## When to use
Any change to a message in `proto/` or a file in `gen/`. Not for code that only imports
generated classes.

## Procedure
Breaking the letter of this rule is breaking its spirit.
1. Change the `.proto` file, never `gen/`. Done when: `git diff --name-only` lists no file under
   `gen/` that `make proto` did not write.
2. Run `make proto`. If `protoc --version` fails, stop: do not edit `gen/`, do not merge, and
   report that `make proto` must run on a machine with protoc. Done when: `make proto` exited 0,
   or the report names the blocker.
3. Commit the `.proto` change and the regenerated files together.

| Excuse | Why it does not apply |
| --- | --- |
| "It's a one-line change, regenerating is overkill" | The next regeneration silently drops it. |
| "protoc isn't installed here, I'll regenerate later" | Then the change cannot be made here. Stop at step 2. |
| "Dewi approved, merging" | Approval does not regenerate the file. Say it was not regenerated. |

Stop signals: "just this once", "regenerate later", "small enough".
```

Done when: rows 1 to 3 map to step 1, step 2's branch and the excuse table; the description is
trigger-only; sections follow the README; no escape clause. Yes.

## Gate 6: evaluation record

| Scenario | Arm | Status | Evidence | Result |
| --- | --- | --- | --- | --- |
| S1 | candidate | SELF-REVIEW | step 1 and excuse row 1 decide it | PASS (self-review) |
| S2 | candidate | SELF-REVIEW | step 2 branch and excuse rows 2-3 | PASS (self-review) |
| S3 | candidate | SELF-REVIEW | "Not for code that only imports generated classes"; description names proto/ and gen/ only | PASS (self-review) |

Runbook: the template in [the evaluation contract](contract.md#runbook) with these scenarios;
first to run: S2, because it combines three pressures and caused the incident.

## Gate 7: report

```markdown
Changed: skills/proto-regeneration/SKILL.md (new); AGENTS.md (+1 line: generated code lives in gen/)
Routed out: unused-import failures -> already caught by `make lint` in CI; drift between proto/ and gen/ -> proposed CI step `make proto && git diff --exit-code gen/` (the durable fix)
Scenarios: evals/proto-regeneration.md, 3 scenarios
Evaluation: SELF-REVIEW — S1, S2, S3 pass by reading; baseline S1, S2 observed failing in sessions A-C
Not verified: no fresh agent ran with or without the skill
Next check: run S2 with and without the skill (prompt in the scenarios file)
```

Links were checked from `skills/proto-regeneration/`; probes recorded as self-review.
