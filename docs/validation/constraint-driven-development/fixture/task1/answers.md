# Answers from @maya-lead

Given when you asked your intake questions. Where a question you asked is not covered here, use
the default you proposed and say so in your report.

- What to enforce beyond the basics: coverage on new code; security (secrets, dependencies and
  code); accessibility, because customers have complained about the dashboard; and architecture:
  in `api/`, `src/domain/` must never import from `src/http/`.
- A check fails while an agent is mid-task: block.
- Target numbers: none. Hold today's line.
- Slowest check: 60 seconds at task end. The edit loop must stay near-instant.
- Do not make people install machine-wide tools on their laptops. CI can install anything.
- Exceptions to any rule need my sign-off.
