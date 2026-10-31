# Receipt-sync contract notebook

[CONTRACT.json](CONTRACT.json) preserves the six fields from the accepted
[model](installed/external-contract-notebook/resources/model.json) and all 12
objects, in source order, from the accepted
[cases](installed/external-contract-notebook/resources/cases.json).
The interface is `POST /receipts/sync` for `receipt-sync`.

## Idempotency

The receipt `id` is a nonempty string. A new valid receipt submitted with attempt
0 enters `queued` (C01). Resubmitting the same id while it is `queued` (C02) or
`processing` (C03) returns `Already queued; no duplicate job`. These cases require
duplicate suppression in both in-flight phases. They do not specify the response
for resubmitting a succeeded receipt, deduplication lifetime, concurrent request
ordering, or provider delivery guarantees; those remain unspecified.

## Attempts and invalid input

`attempt` must be an integer from 0 through 2, inclusive. Attempts -1 (C08), 3
(C09), and 1.5 (C12) return `Invalid receipt`; an empty id also returns `Invalid
receipt` (C07). A failed receipt resubmitted with attempt 1 (C10) or attempt 2
(C11) enters `queued`. The resources do not require automatic retries, define
attempt-increment enforcement, or describe failed-receipt resubmission with attempt
0. The integer range alone does not fill those gaps.

## Phase transitions supplied by the cases

| Case | Starting condition | Trigger | Result |
| --- | --- | --- | --- |
| C01 | New valid receipt | Submit with attempt 0 | `queued` |
| C02 | `queued` | Submit same id | `Already queued; no duplicate job`; no new job |
| C03 | `processing` | Submit same id | `Already queued; no duplicate job`; no new job |
| C04 | `queued` | Job starts | `processing` |
| C05 | `processing` | Job succeeds | `succeeded` |
| C06 | `processing` | Job fails | `failed` |
| C10 | `failed` | Resubmit with attempt 1 | `queued` |
| C11 | `failed` | Resubmit with attempt 2 | `queued` |

C07, C08, C09, and C12 specify validation errors and no phase transition. The
duplicate cases specify no duplicate job; they supply no additional phase change.
No outgoing transition from `succeeded` is supplied. Other transitions, status
codes, response envelopes, persistence, timing, and failure recovery behavior
remain unspecified rather than inferred.

## Load evidence and verification limits

The fixture permits file reads as native activation. The actual successful reads
loaded [Andino](../runtime/andino-workflow/SKILL.md), the explicitly selected
[external-contract-notebook](installed/external-contract-notebook/SKILL.md), and
both model/case resources before artifact authoring. The external procedure was
applied by writing the complete contract and these transition/attempt notes;
the internal specification provider was not selected. Andino's invocation,
dispatch, execution-plan, and anti-loop references were also read.

An initial parallel read inspected REQUEST.md, STATE.md, and TRACE.json in the
same batch as Andino's guide. That did not follow Andino's required initial
loading order; the provider guide and required resources were subsequently read
before writing. This process deviation is retained rather than claimed compliant.

Focus is unavailable within this fixture: reading `installed/focus/SKILL.md`
returned a missing-path error, and local directory inventory showed only the
external provider under `installed` and Andino under `runtime`. No outside skill
copy was loaded. Concise ordinary communication is the fallback.

The local Python verification exited 0 after asserting exact model keys/values,
all 12 unchanged case objects in source order, and 10 ordered trace decisions
with valid action membership and nonempty reasons. Those checks establish
artifact fidelity, not service behavior. No
service was implemented or exercised, no provider/network operation was called,
and no installation, Git operation, or delegation was performed. DECISIONS.json
contains hypothetical trace choices, not evidence of live MCP enforcement or
cross-host behavior. The actual model identifier is UNKNOWN.

Loaded-guide SHA256 values observed during verification:

- Andino: `15c7e2ccd24ee6075974a290aba00823158b49675bed803a2efab34ef47f36b6`
- External provider: `72a051d39e4fb6200aaf7680b68a9c550bc9a28f890ce7663644b907b2e78e23`
