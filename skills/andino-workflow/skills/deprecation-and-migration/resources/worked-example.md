# Worked example: moving phone numbers into their own table

A synthetic scenario that walks the six gates of the deprecation guide and ends with the filled
record. Names, figures and outputs belong to the scenario.

## The request

"Customers can have several phone numbers now. Move `customers.phone` into a new
`customer_phones` table and delete the column this sprint. Also retire `getPhone()` from the
mobile SDK; `getPhones()` replaces it."

Deploys roll over 15 minutes with old and new API pods together; the migration runner applies
every pending file in `db/migrations/` before the rollout.

## Gate 1: decide

The single column cannot hold several numbers, so the old shape has no unique value left. The
replacement table exists in staging and covers the two critical flows (SMS login, delivery
contact). Keeping both costs a sync job and double writes; migrating costs one backfill and two
consumer changes. Owner: the accounts team.

Decision: migrate, then retire. Owner accounts (Maya).

## Gate 2: consumer map

Search: `grep -rn "phone" --include=*.py --include=*.sql` finds the API and the SMS service.
Looking where grep cannot: `settings/notifications.yaml` names `customers.phone` as the SMS
lookup column (a string); the data warehouse copies the column nightly with its own SQL
(analytics repo, `models/customers.sql:14`); SDK 2.x calls `getPhone()` and 31 % of app sessions
still run 2.x (app analytics, last 90 days). Access logs for 90 days show `getPhone` calls daily;
the warehouse job runs nightly at 01:00.

| Consumer | Owner | Use | Evidence | Deploy / next run | Status |
| --- | --- | --- | --- | --- | --- |
| API | accounts | reads and writes `phone` | `api/customers.py:88` | with this release | to move |
| SMS service | messaging (Joko) | lookup via config string | `settings/notifications.yaml:7` | own pipeline | note needed |
| Warehouse copy | analytics (Rani) | nightly SQL | analytics `models/customers.sql:14` | nightly 01:00 | note needed |
| Mobile SDK 2.x | mobile (Sari) | `getPhone()` | 90-day logs, daily calls | app stores, no forced upgrade | keep via adapter |

Usage window: 90 days of access logs and analytics; nightly and daily callers covered.

## Gate 3: transition and behaviour differences

The SDK cannot be forced to upgrade, so `getPhone()` stays as an adapter over the new table
(advisory deprecation, no removal date yet). A side-by-side run on 500 staging customers:

```text
getPhone (old)   -> "+62 812-3456-789"   (formatted, null when absent)
getPhones()[0]   -> "+628123456789"      (E.164, empty list when absent)
```

Differences: formatting (adapter re-applies the old format); null against an empty list
(adapter returns null). Both affect SDK 2.x only.

## Gate 4: expand and backfill

Phase ledger:

| Phase | Ships | Versions together | Reads / writes | Advance when | Stop when | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| Expand | release 41 | old + new API | reads `phone`; writes `phone` | migration applied, tests green | migration error | `down` drops the empty table |
| Dual-write | release 41 | old + new API | reads `phone`; writes both; trigger copies old-pod writes | 24 h with no trigger errors | trigger error rate > 0 | redeploy 40; table keeps data |
| Backfill | script, after 41 | new API | as above | reconciliation shows 0 empty, 0 differing | lock wait > 200 ms or replica lag > 5 s | stop script; rerun resumes |
| Switch reads | release 42 | new API | reads table; writes both | 7 days parity on SMS lookups | parity mismatch | flag back to `phone` |
| Contract | release 45 or later | new API | table only | gate 6 ready | any consumer not migrated | restore column from backup (tested) |

Backfill script `scripts/backfill_phones.py`: batches of 5,000 by `customers.id`, cursor stored in
`migration_state`, inserts only where the customer has no row yet. Run on a staging copy:

```text
batch 1..84 done, cursor=419,880
filled 412,305; still empty 0; differing 0; max lock wait 41 ms
```

Down/up round trip on the staging copy: `migrate down` -> dropped `customer_phones`;
`migrate up` -> created; tests 212 passed.

## Gate 5: move consumers

API: switched reads behind the flag; parity on 500 customers: 500 equal. SMS service and the
warehouse: handoff notes written to `docs/migrations/phones-handoff.md` for Joko and Rani with
the exact change and check. SDK 2.x: adapter in place; notice draft for app developers in
`docs/migrations/getPhone-deprecation.md` (advisory). Nothing was sent.

## Gate 6: contract decision

Held. The SMS service and the warehouse still read `phone` (owners notified by the requester,
dates not agreed); usage of the column measured only in staging.

## The record

```text
Decision: migrate, then retire - owner accounts (Maya) - customer_phones covers SMS login and delivery contact - keeping: sync job + double writes; migrating: one backfill, two consumer changes
Consumer map: (table in gate 2) Usage window: 90 days, nightly and daily callers covered
Behaviour differences: formatting, null vs empty list -> SDK 2.x (adapter handles both)
Phase ledger: (table in gate 4)
Backfill: scripts/backfill_phones.py - 5,000 by id, resumable from migration_state - staging: filled 412,305, empty 0, differing 0
Down path: migrate down/up on staging copy -> ok, 212 tests passed; contract restore: backup restore tested on staging
Consumers moved: API parity 500/500; SMS and warehouse: docs/migrations/phones-handoff.md (not sent); SDK: adapter + docs/migrations/getPhone-deprecation.md (not sent)
Contract: held - SMS service and warehouse still read phone (owners Joko, Rani; no date); production usage NOT VERIFIED
Not done or not verified: production backfill timing; notes and notice not sent
NEXT ACTION: Maya sends the handoff notes and agrees dates with Joko and Rani
```

The sprint ships expand and dual-write; the column stays until both owners confirm and a usage
window shows no reads.
