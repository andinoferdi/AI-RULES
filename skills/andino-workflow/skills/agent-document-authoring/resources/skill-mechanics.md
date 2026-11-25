# Skill mechanics

Read this when the document is a skill. It covers what changes for a skill: the
description, the invocation choice, splitting by invocation and router skills. Everything
else about writing the skill is the levers in `SKILL.md`.

## The description is a pointer

A skill's `description` is its top-level context pointer. Hosts that list skills keep it
loaded every turn, so it pays context load whether or not the skill fires, and its wording
decides when the agent reaches the body. The pointer rules in `SKILL.md` apply in full:

- Name the trigger branches, the situations in which the skill should fire, with the
  leading word first.
- Leave the workflow out. A description that summarizes the steps lets the agent act on the
  summary and skip the body.
- One trigger per branch; collapse synonyms into the branch they rename.

| Weak | Sharp |
| --- | --- |
| "Reviews database migrations by reading the migration files, checking for locks, estimating table size and writing a report. Use for migrations, schema changes, DDL, ALTER TABLE or database changes." | "Use when a change adds or edits a database migration." |

## Invocation: who can fire the skill

Two choices, each spending one of the two loads:

- **Model-invoked.** The skill keeps a model-facing description, so the agent can fire it on
  its own and other skills can reach it. A person can still type its name: model invocation
  adds agent reach and never removes the human's. The cost is the description's permanent
  context load. A model-invoked skill whose content is all reference is also a home for
  reference several skills share.
- **User-invoked.** Only a person typing its name can fire it, and no other skill can. It
  costs no context load and spends cognitive load instead: the person must remember it
  exists. In Claude Code set `disable-model-invocation: true`. On another host use that
  host's own control, checked in its documentation rather than assumed. The description
  becomes a one-line summary for people, with the trigger list removed.

Choose model invocation only when the agent must reach the skill on its own, or another
skill must. A skill that only ever fires by hand is user-invoked and pays no context load.

Reference that two user-invoked skills both need can live in neither: without a
model-facing description, neither can reach the other. Put it in a plain file outside the
skill system that both point at.

## Splitting by invocation

Split off a new model-invoked skill when a distinct leading word should trigger it on its
own (a word you actually use in prompts), or when another skill must reach it. Its
description is new permanent context load, so that independent reach has to be worth it.
The sequence split, which keeps later steps out of view, is in `SKILL.md` under When to
split.

## Router skills

When user-invoked skills multiply past what people remember, the piled-up cognitive load is
cured by a router skill: one user-invoked skill that names the others and when to reach for
each, so people remember one name instead of many. A router can only point. User-invoked
skills have no model-facing description, so nothing but a person can fire them. A template
is in [templates](templates.md).

## Testing a skill

Writing a skill with these levers does not show that it triggers or behaves as intended.
Trigger probes, baseline runs and behavior trials belong to `skill-maker`; hand the skill
there when the request needs that proof.
