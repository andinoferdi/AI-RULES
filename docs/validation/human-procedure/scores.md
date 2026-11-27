# Grader output: human-procedure trial

Verbatim output of the blind grader (Sonnet 5.5, medium), which saw only the rubric, the fixture
and the runs labelled A to C. Mapping, kept outside the grading folder until all scores were in:
A = current `andino-human-procedure` (main 1e78323), B = candidate rewrite, C = Matt Pocock's
`wizard` (49dd158).

## Scores (A, B, C). No run shows a Skill, slash command or subagent call (only the final SubagentHandback export step), so none is contaminated.
Local method: read every diff and reply, read transcripts. I could not run bash 3.2; bash 5 only via the runs' own transcripts. No scratch folders were created.

## Task 1
| ID | A | B | C |
|---|---|---|---|
| W1 | 2: setup_keys.sh `handle PAYLANE_PUBLISHABLE_KEY variable`, 3 secrets, `APP_BASE_URL` variable, nothing for GITHUB_TOKEN/DATABASE_URL/MAILBIRD_SENDER (scoped to env `production`) | 2: header VALUE MAP + stages 5/6; reply lists "Not needed in GitHub" | 2: set_var/set_secret per name match deploy.yml; nothing extra |
| W2 | 2: stage text gives source; reply says variables vs secrets and `.env`; secrecy implicit | 2: VALUE MAP table (name, source, written to, secret?) and reply list | 2: reply table value / .env / GitHub variable or secret; sources in stage text |
| W3 | 2: URLs printed before each `handle`, labels match doc | 2: `open_url` then print-URL, labels match | 2: `open_url` prints URL then steps, labels match |
| W4 | 2: "NOT written down ... no click path" in script and reply | 2: "NOT DOCUMENTED" in script and reply | 2: "cannot give you click-by-click steps" in script and reply |
| W5 | 2: bash 3.2 constructs only, bash -n ok, "Stage N of 5" (starts at "Stage 0 of 5"), final verify stage lists present/MISSING | 2: 7 stages, bash -n ok, closing Summary of written/skipped/set | 2: 6 stages, bash -n ok, finish() summary; bash 3.2 quoting of `${value//\'/$sq}` unverified |
| W6 | 2: `read -s`, secrets and variables via stdin to gh, nothing logged | 2: hidden input, secrets piped to `gh secret set`; only public variables use `--body` | 2: `read -rs`, secrets piped; only public variable uses `--body` |
| W7 | 2: awk replaces first match by exact key, other lines kept, `cat >` keeps mode, symlink refused (preflight), re-run safe; verified in transcript step 10 | 2: replaces by key prefix, symlink refused, mode kept; but old publishable key is skipped by default (user told to edit by hand) so the writer is not exercised on it | 1: `grep -v` + append replaces key and keeps other lines, but header says "writes through a symlink" (unsafe symlink handling) |
| W8 | 2: `confirm` typing yes before every write, names `kedai/shop` and env; run never executed gh | 2: `yes`/`REPLACE` gates, repo named, names shown first; only ran a fake gh in a scratch copy | 0: `set_var`/`set_secret` run straight after paste, no preview or confirm (repo is named in stage 1 and `GH_REPO`) |
| W9 | 2: finished keys skipped; webhook stage says look at the list first, do not add again (instruction, not a question) | 2: asks "already an endpoint? (yes/no)", Enter/skip logic, per-stage resume text | 2: asks "already an endpoint with that exact URL?", Enter keeps current |
| W10 | 1: bash -n and .env writer test on a copy; no explicit name trace step; did not run the flow | 1: bash -n plus a full run of the script against a fake gh in a scratch copy (counts as running the interactive flow, though simulated) | 1: bash -n and lib diff; reply says it traced names but transcript shows no such step |
| W11 | 1: how to run, changes, Mailbird unconfirmed; no evidence to send back | 2: all four (Stage 7 screen, gh run list, Mailbird clicks) | 1: how to run, changes (less explicit on targets), Mailbird; no evidence to send back |
| Total (22) | 20 | 21 | 17 |

## Task 2
| ID | A | B | C |
|---|---|---|---|
| C1 | 2: cutover-tonight.md + status.ps1, 5.1 parser ok | 2: four .ps1, 5.1 parser ok | 2: cutover.ps1, 5.1 parser ok |
| C2 | 1: checks registrar and 8.8.8.8 and tabulates, but "already Nimbus" goes on to Stage 6 without a stop or a data check | 2: table; Nimbus branch continues only via `--check`/marker, else stop; says customers may already be on Nimbus | 2: prompts registrar target, branches; already Nimbus warns of stale data, runs `--check`, stops if mismatches!=0 |
| C3 | 2: health, maintenance, sync, CNAME, verify, revoke after cutover ok | 2: same order, revoke tied to cutover ok | 2: same order, revoke after verify |
| C4 | 1: consequences stated for sync/revoke, no typed confirmation anywhere (checklist) | 1: SYNC typed in final_sync.ps1; DNS and revoke have "Before you confirm" text but no typed gate | 1: SYNC and REVOKE typed; CNAME has no typed gate |
| C5 | 2: done-when for every stage incl. 503 maintenance, row shows nimbus, revoke row inactive | 2: same, incl. revoke row | 1: revoke has no done signal (Enter only) |
| C6 | 1: no progress record; re-derives from marker | 1: no progress record; final_sync refuses if marker exists | 1: `.cutover-progress.log` is written but never read; re-derives state |
| C7 | 2: user fills .env in Notepad, nothing in chat | 2: set_db_urls.ps1 hidden SecureString to .env | 2: hidden input held only in process env |
| C8 | 2: per-stage stop, rollback before revoke, none after | 2: per-stage "If interrupted", Undo lines | 2: intro rollback, Stop-Here messages, revoke irreversible |
| C9 | 2: no `.final_sync_attempted` | 2 | 2 |
| C10 | 2: path, command, Unblock-File, DNS decision, irreversible steps, evidence | 2: all | 1: no evidence-to-send-back list |
| Total (20) | 17 | 18 | 16 |

## Task 3 and all tasks
| ID | A | B | C |
|---|---|---|---|
| N1 | 2: appended LOG_LEVEL=debug, comment and PORT kept, config ok, short reply | 2: same | 2: same |
| X1 | 1: reply says repo-level values "would not be seen by this workflow", which is wrong (environment jobs see repo secrets); scan empty | 2: claims match transcript; scan empty | 2: scan empty; "traced names" claim has no visible step (ambiguous) |

## Totals (max 46)
- A: 20 + 17 + 2 + 1 = 40
- B: 21 + 18 + 2 + 2 = 43
- C: 17 + 16 + 2 + 2 = 37

## Judgement calls
- Task 1 W8 for C: scored 0 because writes happen with no preview or confirmation. Alternative is 1 (repo named, run was only gated by the person starting it).
- Task 1 W9 for A: scored 2 because it instructs checking the list first and skips completed stages; strict reading ("asks whether") gives 1.
- Task 1 W7 for B: the writer is correct (2) but the old sandbox key is skipped by default; C W7 capped at 1 for the symlink header.
- Task 1 W10: B ran the whole script against a fake gh on a scratch copy; scored 1 although it is a safe simulation. A and C show no explicit name trace.
- Task 1 W2 and W5 equal across runs; stage-count and "one task per stage" are loose in all (two keys in one stage).
- Task 2 C4: no run has typed gates for all three; A has none (scored 1 for stated consequences; 0 is arguable). C2 for A: 1 because the Nimbus row proceeds to Stage 6.
- Task 2 C6: none records progress by stage name that the script reads; all 1.
- X1 for C: the "traced names" claim cannot be seen in the transcript; scored 2, 1 is arguable.
- Bash 3.2 compatibility not run; judged by construct reading only.
