# Skills in this repository

Agents load a skill when its description matches the task, then read the whole file.

## Layout

- One folder per skill: `skills/<name>/SKILL.md`. The frontmatter `name` equals the folder name.
- Longer material goes in `skills/<name>/references/`, linked from the step that needs it.

## SKILL.md

Frontmatter has `name` and `description`. The description starts with "Use when", says only
when to load the skill, and stays under 300 characters.

The body uses these sections, in this order. Add others only between Procedure and Output.

1. `## When to use`: when the skill applies and when it does not.
2. `## Procedure`: the steps.
3. `## Output`: what the agent produces.
4. `## Verification`: how to check the skill's result.

## Before merging a skill change

Say in the PR how you checked that the skill changes what agents do.
