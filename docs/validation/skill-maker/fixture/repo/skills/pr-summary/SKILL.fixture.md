---
name: pr-summary
description: Use when opening a pull request - reads the diff, groups the changes by area, writes the summary, adds a risk section from the checklist and links the issue.
---

# PR summary

## When to use

Opening a pull request or updating its description after new commits.

## Procedure

1. Read the full diff against `main` and the linked issue.
2. Write the summary for the reviewers.
3. Go through the [risk checklist](references/risk-checklist.md) and add what applies.
4. Link the issue on the last line as `Fixes #<number>`.

Keep the summary under 8 lines unless the change is complex.

Don't restate the diff. Never narrate what you did. Don't list every file you touched. Avoid
long background sections. Don't pad the testing notes.

## Output

The PR description in Markdown.

## Verification

Read the description once before posting it.
