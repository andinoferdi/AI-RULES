# Execution-plan lifecycle

Use the user's path or the repository's existing convention. Otherwise use
`docs/exec-plans/active/<ticket>.md`. Create a plan for a non-trivial ticket, not
for every message. Reuse the existing plan rather than starting a parallel one.

Start from [the template](execution-plan-template.md). Replace template fields with
facts or explicit unknowns. Phases are dynamic: add/split/reorder when evidence
changes dependencies; preserve finished phases and briefly explain material revisions.

Checkpoint outcomes and verification, not a transcript. Store symbol/file pointers,
concise command results, decision reasons and remaining work. Exclude raw reasoning,
large logs, full diffs, source files, credentials and repeated project instructions.

At interruption, name the first file/symbol to inspect, the change or question to
resolve and the next check. At completion, record acceptance evidence, mark DONE
and move to the repository's completed-plan location, updating direct links.
If an external ticket relies on the old path, leave a short forwarding pointer.

Plans are human-readable Markdown; neither a proprietary memory tool nor a
particular model, UI or subscription is required to resume.
