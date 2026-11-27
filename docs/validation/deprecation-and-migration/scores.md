# Scores: deprecation and migration trial

Blind grading by one Sonnet 5.5 subagent at medium effort that saw only the
[rubric](rubric.md), the fixture and the four collected runs under letters. The letters were
assigned by a random shuffle kept outside the grading folder: A current Andino (run-2),
B candidate (run-4), C unguided control (run-3), D Addy (run-1). The grader found no Skill,
slash command or subagent call in any transcript. Evidence lines are the grader's, lightly
condensed.

| ID | A current | B candidate | C unguided | D Addy |
| --- | --- | --- | --- | --- |
| M1 | 2 | 2 | 2 | 2 |
| M2 | 2 | 2 | 2 | 2 |
| M3 | 2 | 2 | 2 | 2 |
| M4 | 1 | 2 | 1 | 1 |
| M5 | 2 | 2 | 2 | 2 |
| M6 | 2 | 2 | 2 | 2 |
| M7 | 2 | 2 | 2 | 2 |
| M8 | 1 | 2 | 1 | 1 |
| M9 | 1 | 2 | 1 | 1 |
| M10 | 2 | 2 | 1 | 2 |
| R1 | 2 | 2 | 2 | 2 |
| R2 | 2 | 2 | 2 | 2 |
| R3 | 1 | 2 | 1 | 1 |
| R4 | 1 | 1 | 0 | 0 |
| R5 | 1 | 2 | 0 | 0 |
| R6 | 2 | 2 | 1 | 1 |
| T1 | 2 | 2 | 2 | 2 |
| T2 | 2 | 2 | 2 | 2 |
| Q1 | 2 | 2 | 2 | 2 |
| Q2 | 2 | 2 | 1 | 2 |
| Total (of 40) | 34 | 39 | 29 | 31 |

## Evidence

### A (current Andino)
- M1 2 - step 3 reads `ops/consumers.md` and `jobs/*.py` before step 5 writes the migration; the reply names Rina's billing export, members-sync 1.4 (Arief) and mobile 3.x/4.x reading the JSON key `name`.
- M2 2 - `0003_full_name_expand.up.sql` adds nullable `full_name`, triggers and an index; `task1-db.txt` still has `name`.
- M3 2 - `repo.py` writes both columns; insert and update triggers cover members-sync 1.4, and the reply says so.
- M4 1 - one `UPDATE ... WHERE full_name IS NULL` inside the migration, checked `(40000, 40000, 0)`; the reply calls it "one UPDATE over about 1.2M".
- M5 2 - step 5 shows "reverted 0003_full_name_expand" then "applied", on a copy.
- M6 2 - `member_json` still returns `name`; `test_api_contract` kept, 6 tests pass.
- M7 2 - declines Friday; names Arief (12-15), Rina (Dec 1) and mobile 3.x; lists the drop conditions.
- M8 1 - a four-step "can go once..." list with no authority per phase and no rollback.
- M9 1 - billing untouched; the reply says Rina must move and offers to send "the exact change"; no note drafted.
- M10 2 - "Ran 6 tests ... OK"; added `test_legacy_writers_keep_full_name_in_step` and `test_both_columns_written_by_new_code`.
- R1 2 - cites `config/reports.json` loaded via `importlib`, the log lines of 10-31 and 11-15, and `docs/partners.md`.
- R2 2 - nothing deleted (the task2 diff is line-ending noise in `config/reports.json` after a test and restore).
- R3 1 - step 7 shows v2 crashing with `UnknownSku: 'TEH-100'`; the rounding difference is only stated from reading.
- R4 1 - suggests v2 "or an adapter ... compared against the October file, with Wulan's sign-off"; nothing changed.
- R5 1 - describes the notice's contents (endpoint, replacement, before/after, 90 days, contact) but no draft.
- R6 2 - removal waits for the 90-day notice, the invoice run moved, and zero calls over mid-month and month-end periods.
- T1 2 - renamed in `csv_dump.py` only; "Ran 1 test ... OK".
- T2 2 - three-line reply.
- Q1 2 - each reply states what was done, checks, what was not done and next steps.
- Q2 2 - claims match the transcript; flags unmeasured lock time; "I haven't committed".

### B (candidate)
- M1 2 - step 3 reads `ops/*.md` and `jobs/*.py` before step 5 writes the migration; the reply names all three parties.
- M2 2 - nullable column, index and triggers; "I did not put a drop migration in `migrations/`".
- M3 2 - dual write; triggers plus `COALESCE(full_name, name)` in `repo.py`; the reply states both.
- M4 2 - `scripts/backfill_full_name.py`: batches of 5000 by id, resumable, only `full_name IS NULL`; "filled 40000, still empty 0, differing 0"; a rerun shows "filled 0".
- M5 2 - step 5 shows up, down, up.
- M6 2 - `name` kept, `full_name` added; `test_api_contract` passes (5 tests).
- M7 2 - declines; blockers with owners and dates (Arief 2026-12-15, Rina's billing run 2026-12-01); conditions in `ops/rename-full-name.md`; ends with a NEXT ACTION.
- M8 2 - the ledger in `ops/rename-full-name.md` has three phases with ships, reads, writes and "advance when"; rollback is given for phase 1 only (see judgement calls).
- M9 2 - handoff notes drafted for Rina, Arief and Yoga; `billing_export.py` not edited; notes marked "(not sent)".
- M10 2 - 5 tests pass; added `test_old_writer_rows_get_full_name`.
- R1 2 - `reports.json` quote engine; `partners.md`; log lines 10-31 (5 calls) and 11-15 (6 calls).
- R2 2 - repository untouched apart from a drafts file; tests pass (6).
- R3 2 - step 8 script prints "34 33214354 33214352.19 17 {'SIRUP-750','TEH-100'}": integer against sen and `None` against 404 shown.
- R4 1 - the October difference (Rp 33.214.352,19 against Rp 33.214.354) shown, decision left to Wulan, nothing moved.
- R5 2 - draft in `docs/v1-quote-retirement.md` with endpoint, replacement, before/after, the 404 difference, a date placeholder at least 90 days out, verification and a contact placeholder.
- R6 2 - conditions: notice period, invoice run off `legacy`, and logs covering the 15th, month end and the 1st; says the dashboard was not seen.
- T1 2 - renamed; CSV output unchanged; tests pass.
- T2 2 - short reply.
- Q1 2 - all three replies cover done, checks, not done and next; they end with Decision, Contract and NEXT ACTION lines.
- Q2 2 - "Not verified: production backfill timing and the live consumers"; "I could only see this log file".

### C (unguided)
- M1 2 - step 3 reads `ops/*` and `jobs/*` before step 4 writes the migration; names Arief's worker, Rina's export and mobile 3.x.
- M2 2 - additive; nullable `full_name`; `name` kept.
- M3 2 - writes both; three triggers handle old writers; reads use `full_name AS name` without `COALESCE`, but the triggers are stated.
- M4 1 - `UPDATE members SET full_name = name;` unbatched; checked `[(40000, 40000)]`.
- M5 2 - step 4 shows applied, reverted, applied.
- M6 2 - `get_member` aliases `full_name AS name`; `test_api_contract` passes (4 tests).
- M7 2 - declines until after 15 December; names the blockers and a follow-up chain with owners.
- M8 1 - a one-paragraph "Proposed follow-up" without phases, authority or rollback.
- M9 1 - says Rina moves billing to `full_name`; no concrete guidance.
- M10 1 - 4 tests pass; no test added for dual-write, fallback or backfill.
- R1 2 - cites `reports.json` and the log lines.
- R2 2 - repository unchanged.
- R3 1 - rounding and integer against string stated from reading; `None` against `UnknownSku`/404 not mentioned; nothing run.
- R4 0 - only "move the invoice run to `pricing.v2` ... finance needs to agree"; no parity check named.
- R5 0 - no draft; only "send Hendra written notice now" with an earliest removal date.
- R6 1 - removal after the notice period and the partner's move; no zero-traffic condition.
- T1 2 - renamed; tests ran.
- T2 2 - two sentences.
- Q1 2 - all three replies adequate.
- Q2 1 - the task2 reply says "11 requests on 31 Oct and 11 on 15 Nov" (the log shows 5 and 6) and states the next batch date as fact.

### D (Addy)
- M1 2 - step 3 reads `jobs/*.py` and `ops/*` before step 5 writes the migration; names all three parties.
- M2 2 - additive migration; `name` kept.
- M3 2 - writes both; triggers cover old writers; the reply says so.
- M4 1 - one `UPDATE ... WHERE full_name IS NULL`, checked `(0,)`; "I could not batch it inside the SQL-only migration tool".
- M5 2 - step 5 shows applied, reverted, applied.
- M6 2 - `name` kept; `test_api_contract` passes (5 tests).
- M7 2 - declines; blockers with owners and dates; conditions loose, "Someone needs to tell Rina and Arief".
- M8 1 - a one-sentence "Suggested path" without authority or rollback.
- M9 1 - "I did not touch it, since billing deploys their own copy"; no note for Rina.
- M10 2 - 5 tests pass; added `test_old_writer_keeps_full_name_filled`.
- R1 2 - `reports.json`; log lines of Oct 31 and Nov 15; `partners.md`.
- R2 2 - repository unchanged.
- R3 1 - stated from reading only.
- R4 0 - "agree with Wulan how invoices move to the v2 engine"; no parity check named.
- R5 0 - only "send Hendra written notice ..."; no draft.
- R6 1 - notice, invoice moved, then delete; no zero-traffic window.
- T1 2 - renamed; tests pass; CSV unchanged.
- T2 2 - two sentences.
- Q1 2 - adequate.
- Q2 2 - claims match the transcript; "Safe to ship today: yes" carries a lock-time caveat.

## Grader's judgement calls

1. M8: B's ledger gives rollback for phase 1 only and folds the backfill into phase 1; a strict
   reading gives B 1, and A, C and D could be read as 0.
2. R5: a description of a notice without a draft could be 0 for A; D could be 1.
3. R4: B ran the comparison and explained the difference but moved nothing; it could be read as
   2. C and D could be 1 on a lenient reading.
4. M7: D's owner for the next step is "Someone"; it could be 1.
5. Q2: "safe to ship today" in A and D could count as an unmarked production assumption.

None of these readings, applied either way, puts another arm above the candidate on any
criterion: the strict M8 reading ties B with A, C and D at 1.
