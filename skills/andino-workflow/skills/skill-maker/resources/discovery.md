# Discovery

Read at gates 1, 5 and 7: how a skill gets found, what its description says, and how to probe
that it loads when it should and stays quiet when it should not. For rewording the description
or splitting a skill, `agent-document-authoring` has the levers; this file covers what to test.

## How agents find a skill

At startup an agent sees only each skill's name and description. It loads a skill when the
description matches the task, then reads the body. Two failures follow:

- the description misses the situation, so the skill never loads;
- the description summarises the procedure, so the agent follows the summary and skips the
  body. obra reports a case where a description saying "code review between tasks" led an agent
  to run one review although the body required two; with a trigger-only description it ran both.

## The description

- Starts with "Use when" (or the repository's own convention) and names situations and symptoms
  an agent can recognise: what the user asks, what the agent sees, what it is about to do.
- Says only when to load. No steps, no outcome summary, no list of what the skill contains.
- Names the moment just before a violation for a discipline skill ("before editing a file
  under `gen/`"), since that is when the agent must load it.
- Uses the words an agent would search for: error messages, symptoms, tool and file names.
  Prefer the problem ("flaky", "pass/fail inconsistently") over one technology's symptom unless
  the skill is technology-specific, and then say so.
- Third person, inside the host's length limit.

```yaml
# Summarises the procedure: agents may follow this line instead of the body
description: Use for generated code - checks the generator, regenerates, diffs and reports.

# Trigger only
description: Use when a change touches files under gen/ or a .proto file, or when a generated file looks wrong.
```

## Probes

Write two requests in gate 1 and record them in gate 7:

| Probe | Example | Passing means |
| --- | --- | --- |
| Must load | "Add a `nickname` field to the User message" | The agent loads the skill before editing |
| Must not load | "Rename the User class in the admin UI" (no generated code involved) | The agent does not load it |

With a fresh agent, give it the skill set and each prompt alone and see whether it loads the
skill. Without one, check by reading: does the description name a situation present in the
first prompt and absent from the second? Record that as self-review.

## Naming

- Letters, numbers and hyphens; the name matches the folder.
- Name by what the agent does or the core idea (`regenerating-protobuf-code`,
  `condition-based-waiting`), not a vague category (`proto-helpers`).
- Follow the repository's prefix or naming rule when it has one.

## Size and cross-references

Every loaded line competes with the task for context. Keep the body to what changes behaviour,
move long reference material to linked files, point to `--help` instead of copying flags, and
refer to another skill by name instead of repeating its steps. A frequently loaded skill earns
the strictest budget.
