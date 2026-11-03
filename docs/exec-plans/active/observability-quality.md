# Observability skill quality

Status: DONE
Phase: Complete

The accepted design keeps the Andino member layout and authorization boundaries.
Implementation is the primary case. Auditing existing telemetry is the comparison case.

| Task | Dependencies | Acceptance |
| --- | --- | --- |
| Improve procedure | None | Keep the entrypoint and guide aligned. Require question-to-signal mapping, logical outcome versus attempts, and evidence by applicable signal. |
| Build worked example | Procedure | Extend the existing checklist with a scheduler/replay case spanning queue, provider, metrics, trace and alert response, plus an audit of plausible faulty evidence. |
| Verify and publish | Example | Compare old Andino, Addy and revised Andino against the same two cases. Run both embedded probe variants, verify links and entrypoint parity, push and compare isolated latest setup output with the source files. |

The case comparison checks attribution, signal semantics, incident usability and
verification claims. Direct walkthroughs and independent model runs are recorded
separately. Preserve the existing offline checker and avoid changing installer code
if latest setup already tracks the published skill branch.

## Evidence

The workflow checkout matches its remote after fetch. The local main checkout has
unrelated changes. Previous publication records distinguish latest setup from
frozen bundles.

Direct walkthrough using the same cases for all three sources:

| Case | Previous Andino | Addy reference | Revised Andino |
| --- | --- | --- | --- |
| Scheduler timeout then success; replay exhausts retries | Origin and RED guidance, no explicit outcome counting boundary | Concrete origin and propagation snippets, questions about first versus retried success, no complete counting example | Worker evidence and expected metric deltas distinguish provider attempts from terminal outcomes and cover redelivery |
| Audit misleading origin, inflated failure counts and a disconnected worker span | Requires checking evidence, supplies an offline shape probe | Names attribution and trace red flags and checks actual signal output | Maps each bad observation to the failing boundary and records per-signal evidence and retest |

This was a direct walkthrough of the instructions, not an independent model
benchmark. Both embedded probe variants produced their expected JSON. Local
resource links resolved and the Git whitespace check passed.

Skill content was published in `6a875e7`. A clean Codex project-scoped
`ai-rules setup` using the default latest source installed three targets with
zero failures. All four observability package files matched the source after
newline normalization in both nested and standalone installs. This verifies
distribution. Native session discovery and live telemetry were not exercised.

## NEXT ACTION

None. The published skill is available through latest setup.
