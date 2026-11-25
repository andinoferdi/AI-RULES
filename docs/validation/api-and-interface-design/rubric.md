# Comparison rubric: API and interface design

Frozen on 2026-11-25 before any change to the candidate skill. Three arms run the same
prompt on the same fixture: Addy Osmani's `api-and-interface-design`
(addyosmani/agent-skills commit 63128d0), the current `andino-api-and-interface-design`
(AI-RULES main at 83e0c3e) and the candidate rewrite. A grader who sees only this rubric,
the fixture and the three outputs (labelled A, B, C) scores every criterion.

## Run setup

Each arm gets its own run folder with a copy of `fixture/repo/` at `<RUN_DIR>/repo/` and
its own copy of the skill folder at `<SKILL_DIR>`. Runners use no other skill, slash
command or subagent and read nothing outside `<SKILL_DIR>` and `<RUN_DIR>`.

Run prompt, identical for every arm (`<SKILL_DIR>` and `<RUN_DIR>` substituted):

> Read `<SKILL_DIR>/SKILL.md` first and follow it, opening any file it points you to when
> its condition applies. The repository in `<RUN_DIR>/repo/` is described in
> `repo/SYSTEM.md`; read the code before designing.
> Task 1: product wants refunds and wants charging to be safe to retry. Design the payments
> API change.
> Task 2: the notifications module is painful to use from its three callers. Redesign its
> interface.
> Task 3: the props of `web/PaymentStatusBadge.tsx` keep producing impossible combinations.
> Redesign them.
> For each task write `<RUN_DIR>/out/taskN/DESIGN.md` (decisions, consumer impact,
> migration, how you would verify) and `<RUN_DIR>/out/taskN/contract.ts` (the new or
> changed types, schemas or signatures). Task 1 also writes `out/task1/idempotency.ts`, the
> request-handling code that claims, replays or rejects an idempotency key, and
> `out/task1/schema.sql` for any table or constraint it needs. Do not mention which
> guidance you used. Touch nothing outside `<RUN_DIR>`.

## Scoring

Score each criterion 0, 1 or 2 and give one line of evidence (file and quote). Score what
the output says or does; a criterion the output never addresses scores 0 unless the row
says otherwise.

### Task 1: payments API

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| H1 | Atomic claim | The key is claimed in one atomic operation backed by a unique constraint (insert first, or `INSERT ... ON CONFLICT`), in both DESIGN.md and idempotency.ts | Atomic in one place, check-then-act in the other | `SELECT` then `INSERT`, or no claim |
| H2 | Key source | The SDK creates one key per intent and reuses it across retries (per-attempt UUID and `Date.now()` requestId removed), and mobile v3's stable `requestId` is honoured as the key on the legacy route | One of the two | Per-attempt keys remain, or neither addressed |
| H3 | Payload mismatch | Same key with a different body is rejected in the uniform error envelope (409 or 422) and never replayed | Rejected, but in another shape | Replayed, or not handled |
| H4 | In-flight duplicate | A deliberate response for a duplicate that arrives while the first is running (409, bounded wait or 202 with status URL), stated | Handled in code but not stated as a choice | Not handled, or the second request proceeds |
| H5 | Unknown outcome | Intent recorded before calling PayCo; PayCo gets a stable `Idempotency-Key` derived from ours; a timeout leads to a reconcilable state (webhook or polling), not a retry with a new key | Two of the three | One or none |
| H6 | Retention | Key retention covers the longest re-delivery path (7-day DLQ replay, client retries) with that reasoning, and notes that PayCo's 24-hour window is not enough on its own | A retention period without reasoning tied to retry paths | None, or shorter than 7 days |
| H7 | Mobile compatibility | `POST /api/payments/create`, the array body of `GET /api/payments`, and the existing fields and status strings stay working for mobile v3; new routes or fields are added beside them, with a deprecation path for the legacy route | All kept, but no deprecation path; or one existing contract changed with the break acknowledged | An existing field renamed (for example to camelCase), the array wrapped, or the route removed without acknowledgement |
| H8 | Bounded list | The list endpoint becomes bounded (limit or cursor) in a way that keeps mobile v3's array body (Link header, opt-in parameter or new route), and the design states what a default limit does to mobile | Bounded, but the shape change for mobile is only acknowledged; or mobile stays unbounded with a plan | Still unbounded with no plan, or the shape breaks silently |
| H9 | Error shape | One error envelope with a machine-readable code across the new and touched endpoints, a status-code mapping, and no stack trace or internal detail in responses | Envelope defined but applied partly, or a leak remains | Mixed shapes, or the stack leak kept |
| H10 | Boundary validation | Request bodies are parsed at the edge, and the webhook verifies `PayCo-Signature` over the raw body and parses the event shape before use; the service's re-validation and `formatPayment`'s checks of our own rows are removed or justified | Edge parsing present, but the signature check or the internal clean-up is missing | Validation stays scattered, or the webhook stays trusted |
| H11 | Webhook delivery | Events are deduplicated by `event.id` (or an equivalent guard) so PayCo retries and DLQ replays do not notify twice, and out-of-order events cannot move a payment backwards (for example `failed` after `paid`) | One of the two | Neither |
| H12 | Refund design | A noun sub-resource (for example `POST /api/payments/:id/refunds`), separate input and output types, idempotent with a key, and the remaining refundable amount enforced so concurrent refunds cannot exceed the charge | Missing the concurrency-safe limit or the idempotency | A verb route, or no limit at all |
| H13 | Proportion on PUT | `PUT /api/payment-methods/:id` keeps working without a new required `Idempotency-Key` or other new required input (untouched also scores 2) | A key or field added as optional with a stated reason | A key or new field made mandatory, or the route's semantics changed |

### Task 2: notifications module

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| M1 | Caller leverage | Each of the three callers makes one call (for example `notify(userId, 'receipt', vars)`); template, channel choice, retry and recording are hidden inside, so dunning's different retry count and missing record are fixed by construction | Callers simplified but still orchestrate some steps | Interface still exposes the four steps |
| M2 | Seams | Dependencies are injected at the seam that has two real adapters (the SMS, email and push providers, with an in-memory fake for tests); the single-implementation `INotificationRepo` is removed or justified; no new single-implementation interface is added | Seam placed but `INotificationRepo` kept without reason, or one extra speculative interface | More speculative interfaces or layers, or vendor clients still constructed inside `send` |
| M3 | Error contract | What the module returns or throws on transient versus permanent failure is explicit, and a notification failure cannot fail or roll back a payment or webhook response | One of the two | Neither |
| M4 | Fit for an in-process module | No HTTP machinery imported into the module: no `Idempotency-Key` header, status codes, pagination envelopes or schema re-parsing of typed internal arguments. Deduplication keyed by a business event is fine | One HTTP-only element applied | Several |
| M5 | Tests through the interface | Tests call the public entry point with the in-memory fake; the `jest.mock` of internals goes; nothing is exported only for tests | Interface tests planned, but internal mocks or exports remain | No test plan, or tests of internals only |
| M6 | Caller migration | The three in-repo callers move in the same change (or in stated steps), and the old functions are removed or made private at the end | Migration stated but the old entry points stay public with no end | No migration |

### Task 3: PaymentStatusBadge props

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| P1 | Impossible states | Props become a discriminated union (or equivalent) so paid-and-refunded or partial-refund-without-amount cannot be expressed, and each variant carries only its own data | Union introduced, but one impossible state still compiles | Boolean props kept |
| P2 | Migration fits the consumer | The design uses the fact that the 12 call sites are internal and co-deployed: update them in the same change (or a codemod), or a deprecation with a removal step | Migration given without regard to who the consumers are | No migration, or both prop styles kept forever |
| P3 | Proportion | No API-only machinery in the component (error envelopes, idempotency, pagination, runtime schema parsing of typed props) | One such element | Several |

### All tasks: output quality

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| Q1 | Contract files | Each `contract.ts` holds the real types, schemas or signatures; for task 1 input and output types are separate and payment, customer and refund IDs cannot be swapped by accident (branded or distinct types) | Contracts present but input/output merged or IDs interchangeable | Missing or prose only |
| Q2 | Consumer impact | Each DESIGN.md lists every consumer-visible change with its compatibility (additive or breaking) per consumer | Present for some tasks | Absent |
| Q3 | Verification | Each DESIGN.md names concrete checks (for example N concurrent requests with one key produce one charge; a mismatched body gets 409/422; a replayed webhook sends one notification; impossible props fail to compile) | Checks named for some tasks or vaguely | "Test thoroughly" or none |
| Q4 | Idempotency code | `idempotency.ts` has no defect: no check-then-act, unique violation handled, a failed or in-progress record does not crash a replay, the stored status and body are replayed, and the request hash is computed over a stable form or the choice is stated | One defect | Two or more, or a race |
| Q5 | Honesty and register | Plain words; assumptions and unknowns marked; no invented metrics, scores or pseudo-math | Some jargon or one unmarked assumption | Inflated claims or invented metrics |

Maximum: 27 criteria, 54 points.

## Gate

The candidate passes when its score is at least Addy's on every criterion and at least the
current skill's on every criterion. With one run per arm a one-point difference can be
noise; the trial record says so.
