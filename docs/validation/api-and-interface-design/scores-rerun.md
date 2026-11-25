# Scores

## Task 1
| ID | A | B | C |
|---|---|---|---|
| H1 | 2 - DESIGN "single INSERT ... ON CONFLICT DO NOTHING"; idempotency.ts INSERT_CLAIM on PK (scope,key). SDK 2.x legacy path does SELECT then INSERT but inside a tx under pg_advisory_xact_lock, so not a race | 2 - claim() is INSERT ... ON CONFLICT (scope,key) DO NOTHING RETURNING; UNIQUE constraint in schema.sql | 2 - handleIdempotent INSERT ... ON CONFLICT DO NOTHING RETURNING on PK; same in DESIGN |
| H2 | 2 - SDK 3.0 key generated once outside loop; resolveKey uses body.requestId when no header (mobile v3); 2.x stopgap | 2 - 2.x patch release makes key once outside loop; requestId is the key for mobile | 2 - SDK 2.1.0 key once outside loop, used for header and requestId; keyFrom falls back to requestId |
| H3 | 2 - 422 IDEMPOTENCY_KEY_REUSED in envelope, hash checked before replay | 2 - 409 IDEMPOTENCY_KEY_REUSED in APIError envelope | 2 - 422 IDEMPOTENCY_KEY_REUSED via err() envelope |
| H4 | 2 - "In-flight duplicate: 409 + Retry-After. Chosen over waiting ... and over 202" | 2 - "In-flight strategy: reject. 409 REQUEST_IN_PROGRESS" | 2 - "409 REQUEST_IN_PROGRESS + Retry-After: 2 (rejecting is the default...)" |
| H5 | 2 - payments row pending inserted before PayCo; key charge:v1:<paymentId>; timeout -> unknown, webhook/human reconcile, no re-POST after 23h | 2 - pending row attached before call; downstream key charge:v1:scope:key; unknown + reconciler, no re-POST >24h | 2 - row bound before call; charge:v1:<paymentId>; unknown + sweepClaims (reconcile body is only a comment) and webhook |
| H6 | 2 - 30 days, tied to 7-day DLQ and 3-day retries, "Do not reduce this to 24 h" | 2 - 14 days "DLQ replays up to 7 days"; "PayCo dedupes only 24h" | 2 - 30 days, 7-day DLQ + 3-day retries; "PayCo's own 24h dedupe is NOT enough" |
| H7 | 2 - create route, bare array, status strings kept; additive fields; SDK 2.x kept with announced sunset of the guard. Missing key now 400 (log-only first) acknowledged | 2 - same path/body/fields; Deprecation/Sunset headers for legacy mode; /api/v2/payments added beside | 2 - kept; Deprecation/Sunset headers, npm deprecate 2.0.x; error body change flagged as breaking-if-read |
| H8 | 2 - array kept, optional limit (default 200)/cursor, X-Next-Cursor; states v3 sees newest 200 | 2 - array kept, default 100, X-Next-Cursor, /api/v2 envelope; states v3 sees newest 100 | 2 - array kept, default 200 max 500, Link header; table row states v3 sees newest 200 |
| H9 | 2 - `{error:{code,message,details}}` for new/touched, stack removed on create 500, ErrorCode enum | 2 - APIError envelope, stack removed, mobile assumption marked | 2 - one body on every payments route, mapping per code, stack and err.message removed |
| H10 | 1 - zod validate at the edge; webhook signature "Existing gap, noted not fixed here"; no internal clean-up | 2 - Zod perimeter replaces `input: any` and inner throws; webhook verifies HMAC over raw body before parsing (event shape not zod-parsed) | 2 - zod body parse at edge; HMAC over raw body then PayCoEvent zod schema; "Parse once at the edge" |
| H11 | 1 - dedupe by event.id in webhook_events; no guard against failed-after-paid (only "if row not found return 5xx") | 2 - event_id dedupe; "move state forward only ... cannot regress a row" | 2 - event_id in same tx; forward-only `WHERE status='pending'`, failed never overwrites paid |
| H12 | 2 - POST /payments/:id/refunds, union input, separate Refund type, required key, atomic UPDATE with ceiling + CHECK | 2 - sub-resource, input/output split, required key, atomic UPDATE ceiling + CHECK | 2 - sub-resource, union input, RefundDto, required key, single-statement reservation + CHECK |
| H13 | 2 - PUT payment-methods untouched | 2 - untouched | 2 - untouched |

Task 1 totals: A 24, B 26, C 26.

## Task 2 (M1-M6)
| ID | A | B | C |
|---|---|---|---|
| M1 | 2 - one `notify(event)` per caller; retry, channel, record inside; dunning now records | 2 - `notifier.notify(userId, notification)` one call each (dunning passes `day`) | 2 - one `notify` line per caller |
| M2 | 2 - deliver seam with fake, INotificationRepo deleted, no new interface | 2 - ChannelSender (3 adapters + fake) justified; repo deleted | 2 - ChannelSender with 3 adapters + fake; repo deleted, "not ports" stated |
| M3 | 2 - never throws on delivery, result union; charge/webhook cannot fail; programming errors still throw | 2 - never throws, union; payment test | 2 - never throws; retryable flag distinguishes transient/permanent |
| M4 | 2 - no HTTP; dedupe by business ids | 2 - none | 2 - none |
| M5 | 2 - tests through createNotifier with fake deliver; old mock test replaced | 2 - tests at notify with fake sender; old test deleted | 2 - createNotifier with fakes, old test deleted, injected sleep |
| M6 | 2 - three callers same PR; INotificationRepo deleted, others private via lint rule | 2 - callers same/one PR; repo deleted, helpers unexported | 2 - same commit, no shims; build fails if old imports remain |

Task 2 totals: A 12, B 12, C 12.

## Task 3 (P1-P3)
| ID | A | B | C |
|---|---|---|---|
| P1 | 2 - union keyed by status; partial requires amount and currency; failureReason only on failed | 2 - union; refunded/partial require amount+currency; paidAt only on paid | 2 - union in `state` prop; per-variant data; no impossible state compiles |
| P2 | 2 - 12 internal call sites, one PR, tsc worklist, no compat layer | 2 - same, "I did not keep a compatibility layer" | 2 - single breaking change, all sites same PR, codemod table |
| P3 | 2 - none (pure toBadgeState mapper) | 2 - none | 2 - none (toBadgeState throws on a server invariant violation, a mild edge check) |

Task 3 totals: A 6, B 6, C 6.

## Output quality (Q1-Q5)
| ID | A | B | C |
|---|---|---|---|
| Q1 | 1 - contract.ts exists, input/output split, but ids are plain `number` (Payment.id, Refund.id, paymentId) in task 1 and task 2 | 1 - PaymentId/RefundId branded but `Payment.id: number` and `refundPayment(paymentId: number)` bypass them; no CustomerId | 2 - PaymentId/RefundId/CustomerId/IdempotencyKey branded and used in PaymentDto, RefundDto, handlers, notifications; only the partner SDK signature uses plain string |
| Q2 | 1 - task 1 consumer effects spread over "Consumer-facing shape" and rollout steps, no per-consumer compatibility list; tasks 2 and 3 fine | 2 - task 1 consumer impact table; tasks 2, 3 list changes | 2 - consumer table plus "Change classification" with per-consumer compat |
| Q3 | 2 - concrete checks per task (20 concurrent creates, 422, replay, ts-expect-error) | 2 - same quality | 2 - same quality, plus type/contract tests |
| Q4 | 2 - atomic claim, conflict via ON CONFLICT, in_progress -> 409 not crash, stored status/body replayed, canonical hash, fenced finalise | 2 - same properties; minor: an unknown row older than 24h answers REQUEST_IN_PROGRESS indefinitely (no distinct reconciliation reply) | 2 - atomic claim, completed replay, unknown -> 409, stable hash; decline deletes the claim (stated); sweeper resolution is only a comment |
| Q5 | 2 - plain; "Not verified here", assumptions marked | 2 - assumptions marked ("assumption to confirm") | 2 - dedicated "Not verified / assumptions" section |

Output quality totals: A 8, B 9, C 10.

## Overall: A 50, B 53, C 54

## Most decisive differences
- H11: A has event.id dedupe but no rule stopping `failed` after `paid`; B and C state forward-only transitions.
- H10: A leaves webhook signature verification as "Existing gap, noted not fixed here"; B and C verify HMAC over the raw body before parsing, and C also zod-parses the event.
- Q1: only C carries branded PaymentId/RefundId/CustomerId through DTOs, handlers and notification events; A uses plain numbers, B brands some but leaves `Payment.id: number` and `refundPayment(paymentId: number)`.
- Q2: A has no per-consumer compatibility list for task 1; B (table) and C (change classification table) do.
- Tasks 2 and 3 are indistinguishable (12 and 6 for all three).

## Judgement calls
- A H7 could be 1: the only deprecation path is "announce a sunset date for the guard"; B and C emit Deprecation/Sunset headers. Also A makes a missing key a 400.
- A H11 could be 0 or 1 (event.id dedupe present, ordering handled only for a missing row); H10 for A could be 0 if the signature gap is counted as "webhook stays trusted".
- B H10 could be 1: event shape is not explicitly zod-parsed. C H10 internal clean-up is implied by "parse once at the edge", not stated.
- B Q4 could be 1 for the unknown-over-24h dead end returning REQUEST_IN_PROGRESS; C Q4 could be 1 for the sweeper reconcile being a comment and `stable()` not dropping undefined keys.
- C Q1 could be 1 because the SDK `refundPayment(paymentId: string)` is unbranded.
- H7/H9 for C: the error-body change is flagged as breaking if mobile reads `error` as a string; A and B only assume it is safe. Scored the same since all change the 500 body.
- Variance: one run per arm; one-point differences are within noise.
