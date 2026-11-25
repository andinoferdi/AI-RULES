---
name: andino-agent-document-authoring
description: Use when writing, auditing, trimming or restructuring a document another agent reads, such as AGENTS.md, CLAUDE.md, a SKILL.md body or description, a context pointer or a disclosed reference, or when choosing how a skill is invoked or split. Operates under Andino Workflow governance.
---

# Write documents agents follow the same way every run

Internal method ID: `andino-agent-document-authoring` (aliases: `agent-document-authoring`, `writing-for-agents`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: proportional investigation, evidence-based
> decisions, one durable checkpoint and clean handoff. Do not invoke the workflow
> recursively. Loading this resource changes neither tools nor permissions.

## Purpose

Make a document an agent consumes predictable: the agent takes the same process every
run, even when its output differs. A skill, an `AGENTS.md` or `CLAUDE.md`, and a file
reached through a pointer differ in packaging, not in writing, so the same levers apply to
each. A shorter document is often the result and never the goal: a cut that removes
behavior the document must produce is a regression.

## Trigger and non-trigger

Use when writing, auditing, trimming or restructuring a document another agent reads
(`AGENTS.md`, `CLAUDE.md`, a skill's body or description, a pointer line, a disclosed
reference), or when choosing how a skill is invoked, split or routed.

Do not select for:

- Building and testing an executable skill end to end. `skill-maker` owns baseline runs,
  trigger probes and skill TDD, and applies these levers to the skill's wording.
- ADRs, specs or glossaries written for people: `documentation-and-adrs`.
- Rules a linter, formatter or type checker can enforce: move them into that tool.
- Prose polish of text people read: `natural-writing`.
- Notes for the current conversation only, or cuts made only to save length.

## Select a resource, not a second lifecycle

Load only the resource the current need names. It runs inside this procedure and current
authority; it starts no second plan.

| Current need | Resource | Skip when |
| :--- | :--- | :--- |
| The document is a skill: description, invocation, splitting, routers | [skill mechanics](resources/skill-mechanics.md) | The document is not a skill |
| Auditing an existing document: checks, report, ledger, JSON | [audit rubric](resources/audit-rubric.md) | Writing a new document |
| A step's end condition is vague, or agents finish steps early | [completion criteria](resources/completion-criteria.md) | Every step already ends on a clear, demanding criterion |
| Starting a new document | [templates](resources/templates.md) | Revising an existing one |
| Seeing one audit end to end | [worked example](resources/worked-example.md) | The procedure is already clear |

## Prerequisites

Name the document's kind and its consumer (which agent, on which host). Read the document,
every file its pointers name and every environment source it restates (`package.json`,
`Makefile`, config, the directory layout). An unread target or source stays unknown; never
fill it from assumption.

## Procedure

Author mode writes a new document. Audit mode revises an existing one and records findings.

1. **Classify the load.** Always loaded: root guidance, a skill description, and every
   pointer line in either. Loaded on demand: a skill body, a disclosed reference.
   Always-loaded lines earn the hardest pruning. For a skill, read
   [skill mechanics](resources/skill-mechanics.md).
2. **Map branches and rungs.** List the distinct cases the document serves (its branches).
   Place each piece of content on a rung of the information hierarchy below. Mark
   duplication, scattering, branch-only material inlined, dead disclosure and broken
   pointers. Done when every section has a rung and every pointer target is resolved or
   recorded as broken.
3. **Apply the levers in order**, each pass shrinking the next: prune, then hierarchy,
   then pointers, then steps and completion criteria, then wording. In audit mode, record
   each finding as you find it: location, check, evidence and fix
   ([audit rubric](resources/audit-rubric.md)).
4. **Re-read as the consumer.** Walk each branch from its trigger: start at the
   always-loaded pointer, follow it, and reach every step and must-have rule that branch
   needs. Done when every branch walk reaches its material and every rule of the original
   has a ledger verdict: kept, moved, merged, or removed with a reason.
5. **Report** as described in Output. A claim that a sentence is a no-op, or that an edit
   changes behavior, is a hypothesis until the same task runs with and without it; label
   it as one.

## Levers

### Context pointers

A context pointer is a reference held in the agent's context that names out-of-context
material and encodes the condition for reaching it. A skill's description is one; a line
in `AGENTS.md` naming a document is the same object. The pointer's wording, not its target,
decides when and how reliably the agent reaches the material. A must-have target behind a
weakly worded pointer is a variance bug: sharpen the wording first, and inline the material
only if sharpening fails.

A pointer does two jobs: it says what the material is, and it names the branches that
should trigger reaching it. A branch is a distinct case the document handles, so different
runs take different paths through it. Every word of an always-loaded pointer costs on every
turn, so prune it harder than the body:

- Front-load the leading word; the pointer is where it does its triggering work.
- One trigger per branch. Synonyms that rename one branch are that branch written twice;
  collapse them and keep only distinct branches.
- Cut identity the target already carries.

### The two loads

Every document and pointer you add spends one of two budgets:

- **Context load** is always-loaded material on the agent's window, such as an `AGENTS.md`
  line or a skill description. It spends tokens and attention every turn, whether or not
  it fires.
- **Cognitive load** is the cost on the person, who must know which documents exist and
  when to reach for each. It is the price of human agency, not a cost to minimise: spend it
  where human judgment matters and remove it where it does not.

Material reached only through a pointer escapes context load at the price of the pointer's
line. Material with no pointer at all rides entirely on cognitive load.

### Information hierarchy

A document holds steps (ordered actions) and reference (definitions, rules and facts
consulted on demand), in any mix. The core decision is where each piece sits on a ladder
ranked by how immediately the agent needs it:

1. **In-file step**: what the agent does, in order.
2. **In-file reference**: consulted on demand. A flat set of peer rules on one rung is a
   fine arrangement.
3. **Disclosed reference**: a separate file reached by a pointer and loaded only when the
   pointer fires, from a sibling file to fully external material.

Push too little down and the top bloats; push too much and you hide material the agent
needs. **Progressive disclosure** moves material down the ladder to keep the top legible.
Branching is the cleanest test: inline what every branch needs and disclose what only some
branches reach. Reference that should be disclosed buries the steps around it and turns
attending to them into a coin-flip. The opposite failure is **dead disclosure**: must-have
material behind a pointer that no step or branch names, so the agent never opens it.

**Co-location** decides what sits beside a piece once it is placed. Keep a concept's
definition, rules and caveats under one heading, so reading one part brings its neighbours
with it. Scattering fragments one meaning across sections; duplication repeats it.
**Sprawl** is a document simply too long, even when every line is live: attention thins
across the excess. The cure is the ladder: disclose, and split by branch or sequence.

### Steps and completion criteria

Every step ends on a completion criterion. **Clarity** asks whether the agent can tell done
from not done. A vague end invites **premature completion**: attention slips to being done,
pulled by the visible steps still ahead. **Demand** is how much the criterion requires.
"Every modified model accounted for" forces legwork that "produce a change list" does not,
and "every rule applied" binds flat reference the same way. The strongest criteria are
both checkable and exhaustive; a judgment with an exhaustiveness bar is as valid as a
command's exit code. Forms and examples: [completion criteria](resources/completion-criteria.md).

When an agent rushes a step, sharpen the bound first. Only when the step is irreducibly
fuzzy and the rush has been observed, hide the later steps by splitting across a real
context boundary, such as a hand-off or a subagent dispatch. Splitting text inside one
loaded file clears nothing.

### When to split

Splitting a document spends one of the two loads, so split only when the cut earns it:

- **By sequence**, where later steps tempt the agent to rush the current one. Merging
  sequences does the reverse and invites premature completion.
- **By invocation**, for skills: see [skill mechanics](resources/skill-mechanics.md).

### Leading words and negation

A **leading word** is a compact concept already in the model's pretraining that the agent
thinks with, such as *tracer bullet*, a *tight* loop or a *red* test. Repeated as a token,
never as a sentence, it anchors a whole region of behavior in few tokens. It anchors twice:
in the body it steers execution, and in a pointer, when the same word lives in your
prompts, docs and code, it helps the agent reach the material. Hunt for restatements a
leading word retires, such as a triad spelled out at three sites or a sentence gesturing at
one idea. A coined label recruits no priors, so you pay to define it, and it sets a
register the agent may copy; reach for an existing word first.

**Negation** steers by naming the forbidden behavior and so makes it more available, not
less. State the target behavior instead ("write one-line comments"). A prohibition earns
its place only as a hard guardrail you cannot phrase positively, and even then it comes
paired with what to do instead.

### Pruning

- **Single source of truth.** Keep each meaning in one place, so changing it is a one-place
  edit. Duplication costs maintenance and tokens and inflates a meaning past its rank. A
  leading word repeats a token on purpose, never the meaning.
- **Environment as source.** Scripts, config files, the directory layout and `--help`
  output are sources of truth too. A document that restates them is a cache, earning its
  load only when the lookup is expensive. Cache what the agent cannot find by looking: an
  unwritten convention, the reason behind a choice, a gotcha no config confesses.
- **Relevance.** A line loses relevance when it never bears on the task, or when it goes
  stale as the behavior it describes changes. Without pruning, stale layers settle as
  **sediment**.
- **No-ops.** Hunt sentence by sentence for instructions the model already follows by
  default. The test is model-relative and is settled by running the document, not by
  debate. Delete the whole sentence rather than trimming words. A leading word too weak to
  beat the default (*be thorough*) is a no-op; the fix is a stronger word (*relentless*) or
  a more demanding criterion.

## Ownership and permission boundary

Andino coordinates selection, shared progress, resource guards and final status from
evidence. This skill owns its procedure, resources and checks, and coordinator brevity
never truncates them. Edit only the documents the request names, and report any renamed or
moved file that other documents link to. Loading this skill grants no commit, push,
publication or installation authority.

## Output

- **Author mode:** the document or documents, plus the pointer line that reaches each
  disclosed file.
- **Audit mode:** the findings table, the revised document or a diff, the preservation
  ledger ([audit rubric](resources/audit-rubric.md)) and one "Not verified" line naming the
  behavior claims that were not run.

## Verification

Every pointer target exists, every step ends on a completion criterion and every original
rule has a ledger verdict. These are properties of the document. Whether agents behave
better needs a with-and-without trial on a real task, which `skill-maker` runs for skills.

## Worked example and anti-pattern

[The worked example](resources/worked-example.md) audits a testing section end to end and
ends with a structural check you can adapt.

Anti-patterns: deleting guardrails or branch detail to look short; copying template slots
that have no content; replacing a judgment criterion with a shell command that does not
test it; reporting a hunch as a proven no-op.

## Fallback

A pointer target or environment source that cannot be read becomes a `needs decision`
finding, never a guess. When the host's loading behavior is unknown, state the assumption
the classification rests on.

## Local resources

The resources above are packaged with this skill; upstream repositories are not runtime
dependencies. The MIT notice is in [references/license.md](references/license.md).

## Provenance

Adapted closely from Matt Pocock's `writing-for-agents` (`SKILL.md` and
`SKILL-MECHANICS.md`, mattpocock/skills commit 3216582, 2026-08-19) under the MIT license.
The procedure, audit rubric, templates, completion-criteria catalog and worked example are
Andino additions.
