# Authoring craft

Read at gate 5 when you write the skill text. Wording levers (pointers, hierarchy, completion
criteria, pruning, leading words) belong to `agent-document-authoring`; this file covers the
choices specific to skills.

## Degrees of freedom

Match how specific an instruction is to the cost of a wrong guess:

| Freedom | Use for | Write |
| --- | --- | --- |
| High | Judgement with many valid paths: review, trade-offs, analysis | The goal, the criteria and the traps |
| Medium | A clear pattern with local variation: an endpoint, a report | A skeleton or pseudocode with the decisions filled in |
| Low | Steps where any deviation breaks something: migrations, releases, git surgery | Exact commands, expected output and the stop condition |

## Context cost

Assume the agent is capable. Spend lines on what it cannot know (this repository's rules, the
failure that happened, the order that matters, the stop conditions), not on what JSON is or why
tests matter. Each step ends on a condition the agent can check ("Done when: the output shows
..."), because agents stop at the first point that looks finished.

## One excellent example

One complete example from a real scenario, commented where the reason is not obvious, beats
the same idea in five languages or a fill-in-the-blank template. Pick the language the domain
uses (shell or Python for system work, the project's language for code patterns). Agents port a
good example well; they copy a contrived one badly.

## Flowcharts

Use a small flowchart only for a branch an agent would get wrong without it. Labels name states
and decisions, never code; a command inside a node cannot be copied and hides its output. Lists
and tables cover linear steps and lookups better.

## File layout

- Keep principles, the procedure and short code patterns in the skill file.
- Move heavy reference (long API notes, catalogues) and reusable scripts to linked files, each
  linked from the step that needs it, with a "skip when" so the agent loads it only then.
- Link one level deep from the skill file; a chain of files is a maze.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
| --- | --- | --- |
| A story of one session ("on 3 October we found ...") | Not reusable; the next case differs | The rule and the evidence that it was needed |
| The same example in several languages | Thin and costly to maintain | One complete example |
| Code in flowchart nodes | Cannot be copied or run | Code blocks next to the step |
| Generic labels (`helper1`, `step3`, `pattern4`) | Carry no meaning | Names that say what the thing does |
| Prose for a rule a tool enforces | Costs context, drifts from the tool | Route it to the tool (gate 2) |
| Coined labels and pseudo-measurements | Readers cannot act on them | Plain words and real observations |
