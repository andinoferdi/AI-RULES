# Plan execution contract

## Single durable checkpoint and state

The existing plan is authoritative. Preserve its proportional shape and equivalent
project fields. Keep TODO, IN_PROGRESS, BLOCKED, DONE and SKIPPED synchronized when
both board and detail exist. BLOCKED names its dependency and can resume when resolved.
SKIPPED records an accepted replacement. Drift can reopen DONE and affected consumers;
preserve unrelated valid evidence. Recovery attributes current bytes and preserves
user changes before rerunning missing checks; never revert unknown work.

## Acceptance and evidence

DONE requires current acceptance observations: command/action, directory, exit/result,
exercised scope, relevant environment, tested identity and limits. Separate expected
from actual results. Commit ranges identify committed bytes only; hashes or scoped
snapshots also cover WIP and owned new files. Empty or wholly skipped checks are gaps.

Load canonical TDD for behavior changes: meaningful RED, minimal implementation,
focused GREEN. Import/tool/fixture errors are setup failures. If already GREEN,
inspect coverage and real behavior; preserve satisfied behavior rather than inventing
changes. Static artifacts use observable artifact checks; runtime-affecting config
needs behavioral checks. Select regression/integration by risk and project quality floor.

Reuse requires nonempty source, check and relevant environment identities, prior PASS
and unchanged dependencies. Two missing fields do not constitute matching evidence.
Worker reports and checklist marks never replace actual observation.

## Rulings and authority

Accepted requirements outrank defective steps. Record the smallest grounded correction:
`Ruling: <decision> — <evidence/spec basis> — <cost and scope if wrong>`.
Propagate interface changes and invalidate affected consumers. A ruling cannot waive
acceptance or silently change a material user-owned requirement.

Reuse existing scoped session authority for commit, push, setup and delegation. This
guide grants none. Check actual effect and host constraints; ask only for missing
authority or decisions. Network reading is not automatically publication. Block the
affected action and continue independent authorized work.

## Review and delivery

Use canonical code-review and verification. Pin accepted BASE plus committed, staged,
unstaged and owned untracked bytes. Include requirements, rulings, actual checks and
untested risks; preserve separate Spec and Standards verdicts. Diff statistics alone
are not a review. Fresh delegation requires utility, availability and authorization;
otherwise make a distinct self-review and disclose the limitation.

Grade real user effect, resolve material findings using suitable behavioral/static
checks and scoped re-review. Defer optional polish with reasons. Bound loops by new
evidence; a pass limit never converts unresolved acceptance to DONE. Preserve the
exact blocker, failed criterion and concrete NEXT ACTION.

Distinguish source verification, publication and installed activation. When setup is
in scope, compare nested and native member resources with the reviewed source revision.
Finish only when required outcomes are observed; retain the durable checkpoint.
