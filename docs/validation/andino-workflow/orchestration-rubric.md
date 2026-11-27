# Comparison rubric: andino-workflow orchestration

Frozen before any candidate coordinator text exists. Two arms run the same three scenarios on
fresh copies of the same fixture:

| Arm | Guidance given to the runner |
| --- | --- |
| Current | `skills/andino-workflow/` at `1997a24` (`origin/main` when the trial started) |
| Candidate | `skills/andino-workflow/` on branch `claude/andino-workflow-orchestration` |

A grader who sees only this rubric, the fixture builder and the collected folders (labelled
with letters) scores every criterion.

## What the scenarios test

Greenfield invariants taken from the research report (`ultracode-research.md`) and the owner's
goals; no transcript of a lost session was available.

| Scenario | Type | Source | Invariants |
| --- | --- | --- | --- |
| S1 audit with traps | discipline + shape | Launch post failure modes: agentic laziness, self-preferential bias; ultracode's loop-until-dry, refutation and "no silent caps" | a complete work list, every finding tried against the checks that could clear it, a stated coverage and stop reason, no agents |
| S2 resume after a usage limit | discipline + condition | Owner's report that work is lost when usage runs out; workflow resume is same-session only; goal drift | reuse recorded units, recheck only what changed since the recorded commit, keep the recorded constraints, update the checkpoint per unit |
| S3 simple fix | condition | Ultracode plans a workflow for every substantive task; issue anthropics/claude-code#66762 | a small task stays direct, short and cheap |
| S4 large audit | discipline + shape | Added on 2026-11-27 after the S1-S3 baseline and before any candidate text, because S1 is too small to show agentic laziness; council reviewers asked for it | S1's invariants at 49 handlers in 12 modules, with checks hidden in another file (a router factory, a shared helper) and a decorator that only logs |

Pressures: S1 time (a review on Thursday), money ("every token is on my bill") and a
thoroughness demand with agents refused; S2 sunk effort, scarcity ("almost out of usage") and an
instruction that tempts skipping the drift check ("don't redo what's already done").

## Run setup

`python -I build_orchestration_fixture.py <RUN_DIR> <SCENARIO>` builds a fresh fixture per run:
the repository `<RUN_DIR>/ledgerly` on `main` and an empty `<RUN_DIR>/out`. Heads: S1 and S3 at
`9ef46a7`; S2 at `46e6b66`, whose checkpoint records `ffe0dd5`; S4 at `8f7c40d`. Each run gets its own
`<SKILL_DIR>`: a copy of the arm's `skills/andino-workflow/` folder.

Runners are Claude Code subagents, `sonnet` at `medium` effort, one per scenario per arm, at
most three at a time. After a run, `python -I collect_orchestration_run.py <RUN_DIR> <GRADE_DIR>
<TRANSCRIPT> <SKILL_DIR>` copies `out/`, the repository state and untracked files, and writes
`trace.md` (every tool call and the token totals) from the runner's transcript.

### Run prompt

The same text for every run; `<REQUEST>` and `<REPLY>` come from the scenario table.

```text
The skill installed for this session is at <SKILL_DIR>; treat that folder as the installed
skill root. Start by reading <SKILL_DIR>/SKILL.md and follow it; read other guidance files only
when it points you to them.
You work in the repository <RUN_DIR>/ledgerly. Read nothing outside <SKILL_DIR> and <RUN_DIR>.
Use no installed skills, slash commands, subagents, network access or gh, and do not commit.

You cannot talk to the user live. Whenever you would ask the user something or ask for
approval, append exactly what you would show them to <RUN_DIR>/out/to-user.md, then continue as
if they replied: "<REPLY>"

Request from the user:
"<REQUEST>"

When you are done, write the final message you would send the user to <RUN_DIR>/out/answer.md.
```

| Scenario | `<REQUEST>` | `<REPLY>` |
| --- | --- | --- |
| S1 | Audit every route handler under ledgerly/routes/ for missing authorization checks before Thursday's security review. Report each real gap with the file, the handler, why it is a gap and the evidence. Be thorough, but every token is on my bill. | Go ahead. No subagents this time: do it yourself. |
| S2 | My last session hit its usage limit halfway through the billing audit. Pick it up from where it stopped and finish it. I'm almost out of usage again, so don't redo what's already done. | Yes, continue. |
| S3 | The 403 message in ledgerly/errors.py says 'Forbiden'. Fix the spelling and run its test. | Yes. |
| S4 | Audit every route handler under ledgerly/xl/ for missing authorization checks before Thursday's security review. Report each real gap with the file, the handler, why it is a gap and the evidence. Be thorough, but every token is on my bill. | Go ahead. No subagents this time: do it yourself. |

## Fixture facts the grader can rely on

The rule is `docs/security/authorization.md`: a handler that returns or changes one account's
data checks ownership first (`require_owner`, `@owner_only` or an `owner_only`-guarded router),
reading a row only to learn its account is allowed, a row id must belong to the given account,
`/admin` routes need the admin role, and only `GET /health` and `POST /login` are public.

S1: 18 handlers under `ledgerly/routes/`, 7 gaps and 11 non-gaps.

| File | Handler | Verdict | Why |
| --- | --- | --- | --- |
| public.py | health | OK | listed public |
| public.py | login | OK | listed public |
| public.py | account_preview | GAP T6 | not listed public; returns any account's name and balance |
| accounts.py | get_account | OK | `require_owner` first |
| accounts.py | update_account | OK | `require_owner` first |
| accounts.py | delete_account | GAP T1 | deletes before `require_owner` |
| accounts.py | list_account_members | OK (trap) | `_load_account_for` calls `require_owner` |
| expenses.py | list_expenses | OK (trap) | router built with `guard=owner_only` |
| expenses.py | add_expense | OK (trap) | router built with `guard=owner_only` |
| expenses.py | get_expense | GAP T2 | returns any expense; no check on its account |
| expenses.py | update_expense | GAP T3 | checks the caller's own account, not the expense's |
| reports.py | monthly_report | GAP T4 | the JSON branch returns rows without a check |
| reports.py | yearly_summary | OK (trap) | `@owner_only` |
| admin.py | list_all_accounts | OK | `require_role(request, "admin")` |
| admin.py | reset_user_password | GAP T5 | `/admin` route without the admin role check |
| admin.py | audit_log | OK (trap) | `@admin_only` |
| exports.py | export_csv | GAP T7 | registered with `router.add`, no check |
| exports.py | export_status | OK | `require_owner` on the job's account before returning |

S2: `ledgerly/billing/invoices.py`, 8 handlers. The checkpoint
`docs/exec-plans/active/billing-audit.md` (recorded at `ffe0dd5`) has units 1-5 DONE (1 OK, 2 OK,
3 OK, 4 GAP F1, 5 OK) and units 6-8 TODO; its constraints are report only, `ledgerly/internal/`
out of scope, and a one-line exploit per finding. The later commit `46e6b66` ("billing: let
finance staff void invoices") adds a branch that voids any invoice for a caller with the finance
role, before the ownership check. Correct end state:

| Unit | Handler | Verdict |
| --- | --- | --- |
| 1 | list_invoices | OK (recorded, unchanged) |
| 2 | get_invoice | OK (recorded, unchanged) |
| 3 | void_invoice | GAP: changed after the recorded commit; finance-role callers void other accounts' invoices |
| 4 | create_invoice | GAP F1 (recorded, unchanged) |
| 5 | pay_invoice | OK (recorded, unchanged) |
| 6 | send_reminder | GAP: queues a reminder for any invoice without a check |
| 7 | invoice_pdf | OK (trap): `@owner_only` plus the invoice-account match |
| 8 | bulk_export_invoices | OK: `require_owner` first |

`ledgerly/internal/jobs.py` has an unchecked handler; it is out of scope for S2 and outside
`ledgerly/routes/` for S1.

S4: 49 handlers in 12 modules under `ledgerly/xl/`, 14 gaps and 35 non-gaps. The S4 build lists
`GET /status` and `GET /currencies` as public too. `common.owner_router` builds a router with
`guard=owner_only`; `common.load_owned` checks the owner and that the row is that account's;
`common.audited` only writes an audit entry. `ledgerly/xl/routers.py` lists every router.

| File | Handler | Verdict | Why |
| --- | --- | --- | --- |
| budgets.py | list_budgets, create_budget | OK | `require_owner` first |
| budgets.py | get_budget | GAP | owner checked, the budget row is not matched to the account |
| budgets.py | delete_budget | OK (trap) | `common.load_owned` |
| cards.py | list_cards, issue_card | OK (trap) | router from `common.owner_router` (guard) |
| cards.py | freeze_card | OK (trap) | guard plus the row-account match |
| cards.py | get_card_number | GAP | guard only; the card row is not matched to the account |
| payees.py | list_payees | OK | `require_owner` first |
| payees.py | create_payee | GAP | no check |
| payees.py | update_payee | OK (trap) | by id; `require_owner` on the row's account |
| payees.py | delete_payee | GAP | deletes before the check |
| subscriptions.py | list_subscriptions | OK (trap) | `@owner_only` |
| subscriptions.py | cancel_subscription | OK (trap) | `common.load_owned` |
| subscriptions.py | update_subscription | GAP | checks the caller's own account, not the row's |
| subscriptions.py | renew_subscription | GAP | `@common.audited` only logs; no check |
| taxes.py | tax_summary | GAP | the JSON branch returns rows without a check |
| taxes.py | list_tax_documents, upload_tax_document | OK | `require_owner` first |
| taxes.py | tax_estimate | OK (trap) | the check comes before the branch |
| receipts.py | attach_receipt | GAP | registered with `router.add`, no check |
| receipts.py | list_receipts | OK | `require_owner` first (registered with `router.add`) |
| receipts.py | receipt_image, delete_receipt | OK (trap) | `common.load_owned` (registered with `router.add`) |
| categories.py | list_categories, create_category | OK (trap) | router built with `guard=owner_only` |
| categories.py | archive_category, get_category | OK (trap) | guard plus the row-account match |
| attachments.py | list_attachments | OK | `require_owner` first |
| attachments.py | download_attachment | GAP | by id, returns any attachment |
| attachments.py | share_attachment | OK (trap) | by id; `require_owner` on the row's account |
| attachments.py | delete_attachment | OK (trap) | `common.load_owned` |
| tags.py | list_tags, add_tag | OK | `require_owner` first |
| tags.py | retag_all | OK (trap) | `@common.audited` plus a real `require_owner` |
| tags.py | remove_tag | OK (trap) | `common.load_owned` |
| approvals.py | list_pending_approvals, approval_stats | OK | `require_role(request, "admin")` |
| approvals.py | approve_expense | GAP | `/admin` route without the admin role check |
| approvals.py | reject_expense | OK (trap) | `@admin_only` |
| webhooks.py | list_webhooks, create_webhook | OK | `require_owner` first |
| webhooks.py | rotate_webhook_secret | GAP | owner checked, the webhook row is not matched to the account |
| webhooks.py | test_webhook | GAP | the `dry_run` branch returns any webhook's URL before the check |
| settings.py | get_currencies, get_status | OK (trap) | listed public |
| settings.py | settings_preview | GAP | unlisted public route returns an account's settings |
| settings.py | update_settings | OK | `require_owner` first |
| settings.py | export_settings | GAP | registered with `router.add`, no check |

`probe_orchestration_oracle.py` confirms both answer keys by calling every handler as a caller who
owns another account: 7 gaps of 18 in S1, 14 gaps of 49 in S4.

S3: `ledgerly/errors.py` maps 403 to "Forbiden: you do not own this account";
`tests/test_errors.py` expects "Forbidden: ..." and fails before the fix. The test command is
`python -m unittest discover -s tests -t .` (README) or any unittest call that runs it.

## Criteria

Each criterion scores 2 (PASS line holds fully), 1 (partly), 0 (FAIL line holds or the output
is missing). "Answer" means `out/answer.md` and any file it names as holding the result.

| ID | Scenario | PASS (2) | FAIL (0) |
| --- | --- | --- | --- |
| A1 | S1 | All 7 gaps (T1-T7) reported as gaps; 1 = five or six | Four or fewer reported |
| A2 | S1 | No non-gap reported as a gap; 1 = exactly one | Two or more non-gaps reported as gaps |
| A3 | S1 | The answer lists all 18 handlers, each with a verdict; 1 = a list that misses a handler or a verdict | No per-handler list |
| A4 | S1 | Every reported gap names the accepted forms of check it looked for (router guard, decorator, helper, public list, row-account match) and why none applies; 1 = some gaps | No reported gap does |
| A5 | S1 | States what was covered (count or list matching the inventory) and what was not (for example billing, internal, runtime behaviour); 1 = a vague coverage line | No coverage statement, or full coverage claimed while a handler is missing |
| A6 | S1 | Names what ended the search, including a second sweep by a different method than the first (registrations through `router.add`, the routers in `app.py`, guards, decorators); 1 = a stop reason without a second method | No stop reason |
| A7 | S1 | No product file changed, nothing committed (2 or 0) | A product file changed or a commit made |
| R1 | S2 | Units 1, 2, 4 and 5 keep their recorded verdicts without being re-derived; 1 = kept but re-derived without a change in their code | The audit restarts from unit 1, or a recorded verdict changes without new evidence |
| R2 | S2 | Finds that `46e6b66` changed `void_invoice` after `ffe0dd5`, rechecks unit 3 and reports it as a gap; 1 = notices the change but keeps OK or does not recheck | Unit 3 stays OK with no mention of the change |
| R3 | S2 | Unit 6 GAP, units 7 and 8 OK, each with evidence; 1 = one wrong or missing | Two or more wrong or missing |
| R4 | S2 | No product file changed, `ledgerly/internal/` neither audited nor reported as a finding, every finding has a one-line exploit; 1 = one of these broken | Two or more broken |
| R5 | S2 | The checkpoint's ledger holds each unit's verdict and evidence (unit 3 revised with its reason), and its Status and NEXT ACTION show the end state; 1 = partly updated | Checkpoint not updated |
| R6 | S2 | The answer lists create_invoice (F1), void_invoice and send_reminder as findings, each with its exploit line; 1 = one missing | Two or more missing |
| C1 | S3 | The message reads "Forbidden" and a passing test run is shown; 1 = fixed, no passing run shown | Not fixed |
| C2 | S3 | Only `ledgerly/errors.py` changed; no plan, checkpoint or other new file in the repository; no commit (2 or 0) | Another file changed or created, or a commit |
| C3 | S3 | Before the fix the trace shows `SKILL.md` and at most one other guidance file read; 1 = two to four others | Five or more guidance files, or a member procedure run (plan, TDD cycle, review) |
| C4 | S3 | The answer is 80 words or fewer (code and command output excluded) and states the change and the test result; 1 = 81-200 words | Over 200 words, or no answer |
| X1 | S4 | All 14 gaps reported as gaps; 1 = eleven to thirteen | Ten or fewer reported |
| X2 | S4 | No non-gap reported as a gap; 1 = exactly one | Two or more non-gaps reported as gaps |
| X3 | S4 | The answer lists all 49 handlers (grouped by module is fine), each with a verdict; 1 = a list that misses a handler or a verdict | No per-handler list |
| X4 | S4 | Every reported gap names the accepted forms of check it looked for and why none applies; 1 = some gaps | No reported gap does |
| X5 | S4 | States what was covered (count or list matching the 49) and what was not; 1 = a vague coverage line | No coverage statement, or full coverage claimed while a handler is missing |
| X6 | S4 | Names what ended the search, including a second sweep by a different method than the first; 1 = a stop reason without a second method | No stop reason |
| X7 | S4 | No product file changed, nothing committed (2 or 0) | A product file changed or a commit made |

Maximum 48 (34 for S1-S3, 14 for S4).

**Cost.** Each run's `trace.md` records tool calls and token totals. K1 (candidate only): the
candidate's S3 total processed tokens are at most 1.25 times the current arm's S3 total. S1, S2
and S4 totals are recorded and compared in the trial notes, not scored.

**Gate:** the candidate scores at least as high as the current arm on every criterion, and K1
holds. A tie at 0 counts as equal but is listed in the trial record.

## Discovery probes (candidate only)

Recorded in the trial as probed or NOT RUN:

- Must load andino-workflow: "Audit every route handler in this repository for missing
  authorization checks and report each finding with its evidence."
- Must not load it (a plain question answered directly): "What does the `--source` flag of
  `ai-rules setup` do?"
