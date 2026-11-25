# Scores

## Task 1
| ID | A | B | C |
|---|---|---|---|
| H1 | 2 - DESIGN #1 and idempotency.ts claim(): `INSERT ... ON CONFLICT (scope, key) DO NOTHING RETURNING`; unique constraint in schema.sql | 2 - handleIdempotent step 1 `INSERT ... ON CONFLICT DO NOTHING`, PK (scope,key); "No SELECT-then-INSERT" | 2 - INSERT_CLAIM ON CONFLICT on PK in main path; legacy SDK path does SELECT-then-INSERT but under `pg_advisory_xact_lock` (see judgement calls) |
| H2 | 2 - SDK 2.x patch makes key once outside loop; `requestId` honoured as key (resolveIdempotencyKey) | 2 - SDK patch key once before loop; legacy `legacy:<requestId>` key | 2 - SDK 3.0 key once per call; mobile `requestId` accepted as key (2.x only guarded, not patched) |
| H3 | 2 - 409 `IDEMPOTENCY_KEY_REUSED` in envelope, hash checked before replay | 2 - 422 `IDEMPOTENCY_KEY_REUSED` in envelope, also operation mismatch | 2 - 422 `IDEMPOTENCY_KEY_REUSED` in envelope, checked before state |
| H4 | 2 - Decision 8 "In-flight strategy: reject", 409 REQUEST_IN_PROGRESS | 2 - Decision 4, 409 + Retry-After, "Never let it through" | 2 - Decision 4, 409 + Retry-After, reasoned against waiting and 202 |
| H5 | 2 - pending payments row before PayCo, downstream key `charge:v1:<scope>:<key>`, unknown then resume/reconciler | 2 - pending row first, stable downstream key, 503 OUTCOME_UNKNOWN, webhook/lookup `resolveKey` | 2 - pending row first, PayCo key `charge:v1:<paymentId>`, unknown, re-drive under 23h, webhook reconcile |
| H6 | 2 - 14 days, DLQ 7 days, PayCo 24h only dedupes (schema comment, Decision 7) | 2 - 30 days, 7-day DLQ, 3-day retries, PayCo 24h | 2 - 30 days, 7-day DLQ, "Do not reduce this to 24h" |
| H7 | 2 - /create unchanged, array kept, status frozen, new /v2 list, Deprecation/Sunset and removal step for legacy mode, mobile requestId kept until v3 gone | 2 - /create kept, new POST /api/payments, Deprecation/Sunset on /create, retire after v3 gone | 1 - all kept, but no new route and no deprecation path for /create; key made mandatory on create (acknowledged, log-only first) |
| H8 | 2 - bare array, limit default 100, X-Next-Cursor, v2 envelope; states v3 sees newest 100 | 2 - bare array, Link header, default 100, states v3 effect and alternative | 2 - bare array, X-Next-Cursor, default/max 200, states v3 sees newest 200 |
| H9 | 2 - `{error:{code,message,details}}`, code to status mapping in contract.ts, stack removed | 2 - one envelope on all payments routes, stack and err.message never returned | 2 - envelope, ErrorCode mapping, INTERNAL never carries stack (new endpoints; create keeps status codes) |
| H10 | 1 - Zod at edge, signature over raw body before parsing, but no event-shape parse and formatPayment checks not addressed | 2 - Zod edge, `express.raw` + HMAC + `PayCoEvent.safeParse`, createPayment/formatPayment stop re-validating | 1 - Zod at edge; signature only "noted not fixed here"; no event parse, no internal clean-up |
| H11 | 2 - webhook_events by event_id; "move state forward only" so no regression | 2 - dedupe in same tx; forward-only, "charge.failed after paid is ignored" | 1 - dedupe by event.id incl. DLQ replay; out-of-order only handled as "row not found -> 5xx", no stop on failed after paid |
| H12 | 2 - POST /payments/:id/refunds, separate input/Refund types, key required, atomic `UPDATE ... refunded_cents + $2 <= amount_cents` + CHECK | 2 - sub-resource, key required, FOR UPDATE + reservation + CHECK | 2 - sub-resource, full/partial union, key required, atomic conditional UPDATE + CHECK |
| H13 | 2 - PUT payment-methods never touched | 2 - untouched | 2 - untouched |

Task 1 totals: A 25, B 26, C 23.

## Task 2 (M1-M6)
| ID | A | B | C |
|---|---|---|---|
| M1 | 2 - `notifier.notify(userId, {type:'receipt',...})` one call; lookup, channel, retry, record private; dunning record fixed inside | 2 - one `notify({userId, template, dedupeKey})`; retry policy inside (dunning 5 kept deliberately) | 2 - one `notify({type, userId, ...})`; dedupe key derived inside, retry per type internal |
| M2 | 2 - `ChannelSender` with 3 vendors + fake injected via createNotifier; INotificationRepo deleted, no new interface | 2 - `ChannelAdapter` injected, "NO store port", repo deleted | 2 - single `deliver` seam injected, repo deleted, no new interface |
| M3 | 2 - NotifyResult sent/duplicate/skipped/failed, "notify never throws"; receipt failure no longer 500s the charge | 2 - sent/skipped/failed, never throws, reasons explicit, claim released on total failure | 2 - sent/duplicate/failed(reason), never throws for delivery, bugs still throw, 5s deadline |
| M4 | 2 - no HTTP constructs; dedupe by business key `${type}:${paymentId}` | 2 - none; business dedupeKey | 2 - none; business-derived dedupe key |
| M5 | 2 - tests at `notify` with fake ChannelSender; old test deleted | 2 - tests through createNotifier with fake adapters; old test deleted (injectable `sleep` is an option, not a test-only export) | 2 - tests through createNotifier with fake `deliver`; old test replaced |
| M6 | 2 - three callers switched in steps; old exports made private; repo files deleted | 2 - one commit, no shim; deep imports blocked with ESLint | 2 - same PR; repo deleted; lint rule makes the rest private |

Task 2 totals: A 12, B 12, C 12.

## Task 3 (P1-P3)
| ID | A | B | C |
|---|---|---|---|
| P1 | 2 - union keyed on `status`; partial needs amount; failureReason only on failed; paidAt only on paid | 2 - same style; `@ts-expect-error` type tests | 2 - same; paidAt dropped; type tests |
| P2 | 2 - all 12 call sites in one PR, no compat layer, tsc lists them | 2 - same, plus guidance for sites holding only booleans | 2 - same, tsc errors guide conversion |
| P3 | 2 - no API machinery; toBadgeProps mapper is UI logic | 2 - none | 2 - none |

Task 3 totals: A 6, B 6, C 6.

## Output quality (Q1-Q5)
| ID | A | B | C |
|---|---|---|---|
| Q1 | 2 - Zod input schemas separate from Payment/Refund; PaymentId and RefundId branded and used in refund signatures; UserId branded in task 2 (customer ID not branded, see judgement) | 1 - input/output separate, but brands are strings while Payment.id is number and `RefundInput.paymentId` is a plain string; IDs interchangeable in practice | 1 - real zod schemas, input/output separate, no branded IDs (plain `number`) |
| Q2 | 2 - per-consumer impact table (mobile, web, SDK 2.x, new SDK) in task 1; behavior-change list in task 2; call-site impact task 3 | 2 - consumers table with ships-with-change plus additive/breaking classification; task 2 caller table | 1 - consumer-facing shape and rollout cover mobile, SDK, dashboard, but no per-consumer compatibility table |
| Q3 | 2 - 20 parallel one-charge test, mismatch 409, timeout stub, fencing, mobile fixture, ts-expect-error | 2 - 20 concurrent, 422, PayCo stub timeout, webhook replay, grep for stack | 2 - 20 simultaneous, 422, 12s stub, crash injection, DLQ-replay webhook, ts-expect-error |
| Q4 | 2 - ON CONFLICT claim; fenced takeover by conditional UPDATE; replays stored status/body; canonical hash of intent; no crash on unknown/in-progress (minor: unknown older than 24h reports REQUEST_IN_PROGRESS) | 2 - ON CONFLICT claim; unknown/in_progress give 409; replays stored status/body; canonical hash (minor: 'backfill' sentinel skips hash check) | 2 - ON CONFLICT claim; fenced CAS; replays stored; canonical hash excluding requestId; legacy path select-then-insert is lock-serialised |
| Q5 | 2 - assumptions listed, "Not verified here", cost of heuristic stated | 2 - explicit UNKNOWN markers and a not-verified list | 2 - "confirm" flags, "Not verified here"; no invented metrics |

Q totals: A 10, B 9, C 8.

## Overall: A 53, B 53, C 49

## Most decisive differences
- H10: only B parses the webhook event shape (`PayCoEvent.safeParse` after raw-body HMAC) and removes service/formatPayment re-validation. A has the signature but no event parse or clean-up. C only notes the signature gap as "not fixed here".
- H11: C does not stop `failed` after `paid` (its out-of-order handling is only "row not found -> 5xx"). A and B state forward-only transitions plus event.id dedupe.
- H7: B gives a new noun route plus a Deprecation/Sunset path for `/create`. C keeps `/create` with no deprecation path and makes the key mandatory there. A keeps the legacy path with a v2 list and a stated removal step.
- Q1: A brands PaymentId, RefundId and UserId and uses them in signatures. B and C leave IDs effectively interchangeable.
- Q2: A and B have per-consumer impact tables. C has only a narrative "consumer-facing shape".

## Judgement calls
- H1 (C): the legacy-SDK path does SELECT then INSERT under an advisory lock, with the unique PK still behind it. I scored 2 since it is serialised and the main path is atomic; strict reading gives 1.
- H2 (C): the per-attempt key is removed only in SDK 3.0, not patched in 2.x (A and B patch 2.x). Could be 1.
- H7 (A): the route `/create` is never deprecated, only the fingerprint mode and the list route. I gave 2 on the strength of the stated removal steps; a strict grader could give 1.
- H9 (A, C): envelope stated as for "new responses"; legacy error bodies change only by dropping the stack. Could be 1.
- M3 (all): none distinguishes "transient" and "permanent" by those words; I accepted the explicit result unions (skipped/failed reasons). A strict reading could drop each to 1.
- Q1 (A, B): the customer ID is not branded in any output. A is 2 because the payment and refund IDs are branded and used throughout; B is 1 because the brand is not carried into Payment.id or the SDK input.
- Q4 (all): small design edges (A aged-unknown reported as in-progress, B backfill sentinel skipping the hash, C lock-serialised select) were not counted as defects; each could move to 1.
- Q2 (C): could be 2 if the narrative per-consumer notes are accepted.
