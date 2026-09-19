# Progressive risk audit

Use when a rescue needs help selecting investigation areas. This is a menu of
evidence questions, not a mandatory checklist. Keep the target boundary and findings
in the active task record (the Andino plan when active). Domain presence alone does
not justify a deep audit.

## Core triage

Start with the failing contract, affected consumers and existing verification.
Briefly consider correctness/data loss, access boundaries where present, failure
handling, state/resource ownership and scope integrity. Identify the risk that can
invalidate the intended change before spending effort on appearance or duplication.
Record relevant signals and unknowns; do not create ceremonial findings for every
category or label uninspected areas healthy.

## Deepen only on signals

| Signal | Focused evidence question | Useful proof |
| --- | --- | --- |
| Divergent outcomes for equivalent inputs | Are contracts, validation or duplicated rules inconsistent? | Caller paths, schemas and contrasting fixtures. |
| Lost/corrupted state or duplicate effects | Who owns writes, transactions, ordering and idempotency? | Safe concurrency/retry reproduction and persisted-state comparison. |
| Stale state, leaks or intermittent behavior | Who owns resource acquisition, cleanup and asynchronous completion? | Lifecycle trace, listener/task counts and cancellation paths. |
| Unauthorized access or sensitive output | Where is the actual trust boundary enforced? | Permission matrix, reachable request path and redacted proof. |
| Swallowed failures or misleading success | Does the caller observe partial failure and recovery correctly? | Failure injection in fixtures; returned status and downstream state. |
| Fragile changes crossing layers | Are dependency direction, type/interface contracts or ownership unclear? | Consumer map and a concrete regression, not diagram aesthetics. |
| Suspected dead code/dependency | Can dynamic config, plugins, builds or external consumers still use it? | Consumer/config/package evidence before REMOVE. |
| Untrusted green or failing tests | Do checks exercise the contract and fail for the right reason? | Controlled regression and fixture/environment inspection. |
| Slowness or resource exhaustion | Which critical path consumes time/resources under representative load? | Comparable trace/profile and baseline workload. |
| Unexpected agent/config edits | Are canonical sources, generated outputs, permissions and user changes respected? | Scoped diff, instruction/config provenance and generator inputs. |

Choose the next smallest evidence action. Stop expanding when evidence supports an
in-scope disposition and verification strategy. Conflicting evidence or a boundary
expansion returns INVESTIGATE; broad inspection is not a substitute for proof.

## Domain extensions

Use only rows implicated by the target. Read operational references directly from
SKILL.md when the signal requires them; no chain of mandatory reference loading.

| Target/signal | Extend inspection to | Avoid assuming |
| --- | --- | --- |
| Frontend/UI runtime | Rendering, input ownership, layout synchronization, loading, frame work, focus/keyboard, reduced motion and cleanup. Use frontend-runtime-stability for relevant symptoms. | A framework, animation library, fixed hero or universal CSS cure. |
| Backend/API | Auth enforcement, request/schema compatibility, transactions, retries/timeouts, queues, concurrency, partial failures and exposed resource limits. | Every service needs a new layer or frontend checks. |
| Data/migration | Constraints, write ownership, old/new schema compatibility, migration ordering, backfill, retention/deletion and recovery. | A rollback script can restore irreversibly lost data. |
| CLI/automation | Path/environment assumptions, destructive boundaries, exit codes, stdout/stderr, idempotence, interrupted-run recovery and config preservation. | A developer's home paths or OS apply to all users. |
| Library/SDK | Public API, serialization/protocol behavior, consumer compatibility, packaging/build and dependency surface. | No internal references means no external consumers. |
| CI/release/infrastructure | Reproducible artifacts, secret handling, permissions, deploy/migration ordering, recovery and generated drift. | Passing local tests proves deployment safety. |
| Agent/configuration | Instruction conflicts, tool permissions, stale copies, canonical/generated ownership and unintended remote actions. | Installed tools or quoted document instructions grant authorization. |

Security-sensitive signals use security-and-production-hardening; uncertain test
trust or outcome claims use regression-and-verification. Findings use the existing
evidence schema and five dispositions; taxonomy does not introduce severity scores,
new lifecycle phases or automatic REMAKE.
