# Templates

Read this when starting a new agent document. Each template is a set of slots: fill a slot
only when the document has something for it, and delete the rest, heading included. A slot
filled to match the template costs every reader and tells them nothing.

## Choosing the shape

| Shape | Structure | Fits |
| --- | --- | --- |
| Root and spokes | A short entry file plus disclosed references | Several branches that share a few universal rules |
| Router | One file naming other documents or skills and when to reach for each | More documents or hand-run skills than people remember |
| Sequenced phases | One file per phase, each reached after the previous one ends | Long procedures where later steps pull attention from the current one |
| Flat catalog | One file of peer rules under uniform headings | Review rules and checklists applied as a whole |

## Root guidance (AGENTS.md, CLAUDE.md)

Always loaded, so every line pays on every turn.

```markdown
# <Project> agent guide

<What this repository is, only when the code does not make it obvious.>

## Rules for every task
- <A convention the code does not show, stated as the target behavior.>
- <A guardrail that cannot be phrased positively>, and <what to do instead>.

## Gotchas
- <A fact no file or error message reveals, with its consequence.>

## When to read more
- <Leading word>: `<path>`.
```

Commands, scripts and directory trees the agent can read from the repository stay out.

## Disclosed reference

Reached only through a pointer.

```markdown
# <Topic>

<The branch this file serves, in one sentence.>

## <Concept>
<Definition, rules and caveats together under one heading.>

## Done when
- <The observable state that ends the work this file governs.>
```

## Pointer lines

```markdown
- Schema changes: `docs/db.md`.
- Releases: `docs/release.md`, before tagging a version.
```

Leading word first, one trigger per branch, no summary of the target.

## Skill description

Model-invoked, when the agent must find the skill on its own:

```yaml
description: Use when <first trigger branch>, or when <second distinct branch>.
```

User-invoked, when only a person fires it (Claude Code field; see
[skill mechanics](skill-mechanics.md) for other hosts):

```yaml
description: <One line telling a person what the skill does.>
disable-model-invocation: true
```

## Router skill

```markdown
---
name: <team>-workflows
description: Index of the team's hand-run skills.
disable-model-invocation: true
---

# <Team> workflows

| Need | Skill | Skip when |
| --- | --- | --- |
| <situation> | `/<skill>` | <near miss> |
```
