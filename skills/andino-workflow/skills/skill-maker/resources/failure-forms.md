# Failure forms

Read at gate 2, when you assign each row a destination and, for skill rows, a form. The form
that fixes one kind of failure makes another kind worse, so classify before you write.

## Destination first

A row goes into the skill only when an agent needs judgement during a task. Everything else
has a better home, and the skill is shorter and stronger without it.

| The row is | Destination | What to write in the routing table |
| --- | --- | --- |
| A rule a linter, formatter, type checker, schema or CI job can catch (import order, indentation, a forbidden call, a generated file out of date) | Tooling | The tool and rule that catch it now (`import/order` in `npm run lint`), or the exact proposed check |
| A fact, preference or convention (an endpoint, a contact, a naming rule) | Project instructions | The file and section that will hold it (`AGENTS.md`, "Working here") |
| Something a file or tool already holds | Already covered | The file and line, or the tool setting, you checked |
| A one-time event that will not recur | Nothing | Why it will not recur |
| A decision the agent makes during work | Skill | The form below |

"Already covered" needs a check of the repository, not a guess. When a request asks for a
skill and every row lands outside it, make no skill: make the routed changes and say where
each item went.

## Form for each skill row

| Baseline failure | Form that works | Form that backfires |
| --- | --- | --- |
| Discipline: the agent knows the rule and skips it under pressure | A hard rule tied to the action, an excuse table built from the excuses as said, stop signals, and "letter equals spirit" | Soft wording ("prefer", "consider", "it is recommended") |
| Shape: the output complies but has the wrong form (long, buried verdict, narrated, restated input) | An ordered recipe: the parts of the output, in order, with a size for each | A list of prohibitions ("don't restate", "never narrate") |
| Omission: a required part is missing from something the agent already produces | A required slot in the template the agent fills, with an explicit "none" value | A prose reminder near the template |
| Condition: the right action depends on the situation | A branch on something the agent can observe ("if the check exits 2 ...") | An unconditional rule with exemptions |

Why prohibitions backfire on shape: with a competing goal ("be thorough"), an agent
negotiates with "don't X" and produces more of X. In obra's head-to-head wording tests on
prompt guidance, the prohibition arm produced clearly more unwanted content than the recipe arm,
and trended worse than no guidance. That was one setting; micro-test your own case, but do not
reach for a prohibition first. A recipe leaves nothing to negotiate: the output has the parts or
it does not.

## Rules for any form

- **No escape clauses.** "Don't X unless it matters" reopens the negotiation. In the same tests,
  one such clause turned a consistent recipe noisy. Write a real exception as its own condition
  on something observable.
- **Exemptions do not scope.** "This limit does not apply to code blocks" still suppresses code
  blocks. If part of the output must be exempt, restructure so the rule cannot reach it.
- **Answer the evidence, not your imagination.** Each rule and each excuse-table row traces to a
  row of the routing table. A rule for a failure nobody observed is a guess that costs context
  on every load.

## Closing loopholes for discipline rows

State the rule, then close the workarounds the evidence showed:

```markdown
Regenerate from the .proto file; never edit files under `gen/` by hand.

No exceptions:
- Not for a one-line fix.
- Not when the generator is missing locally: stop and report it.
- Not "for now, regenerate later".
```

Put this early, before the steps:

```markdown
Breaking the letter of this rule is breaking its spirit.
```

Build the excuse table from the words agents used. Quote them; a paraphrase lets the next agent
find a neighbouring wording:

```markdown
| Excuse | Why it does not apply |
| --- | --- |
| "It's a one-line change, regenerating is overkill" | The next regeneration silently drops it. Size is not the issue; ownership of the file is. |
| "protoc isn't installed here" | Then the change cannot be made here. Stop and say who can run it. |
| "The reviewer said ship it" | A go-ahead does not regenerate the file. Say it was not regenerated. |
```

Add stop signals an agent can notice in its own reasoning:

```markdown
Stop signals: you are writing "just this once", "regenerate later" or "small enough". Each one
means: go back to the rule.
```

When an evaluation shows a new excuse, add it to the table and the stop signals, and rerun the
scenarios that exposed it. Update the description only if the excuse reveals a trigger the
description missed (a situation just before the violation).
