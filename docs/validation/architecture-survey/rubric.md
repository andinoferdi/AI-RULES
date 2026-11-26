# Comparison rubric: architecture survey

Frozen on 2026-11-26 before any change to the candidate skill. Three arms run the same prompt
on the same fixture: Matt Pocock's `improve-codebase-architecture` with the skills it calls
(mattpocock/skills commit 7739eae: `improve-codebase-architecture`, `codebase-design`,
`grilling`, `domain-modeling`), the current `andino-architecture-survey` (AI-RULES main at
49ad00b) and the candidate rewrite. A grader who sees only this rubric, the fixture and the three
output sets (labelled A, B, C) scores every criterion.

## Run setup

For each arm, build a fresh repository with
`python -I docs/validation/architecture-survey/fixture/build_repo.py <RUN_DIR>` (26 commits; the
history is part of the fixture) and create `<RUN_DIR>/tmp/` and `<RUN_DIR>/out/`. Copy the arm's
skill folders into `<SKILL_DIR>`:

- Matt: `improve-codebase-architecture/`, `codebase-design/`, `grilling/`, `domain-modeling/`;
  `<ENTRY>` is `improve-codebase-architecture/SKILL.md`.
- Current and candidate: `architecture-survey/` and `api-and-interface-design/` from
  `skills/andino-workflow/skills/` at the arm's revision; `<ENTRY>` is
  `architecture-survey/SKILL.md`.

Runners use no other skill, slash command or subagent and read nothing outside `<SKILL_DIR>` and
`<RUN_DIR>`. After the run, record `git -C <RUN_DIR>/repo status --porcelain` and
`git -C <RUN_DIR>/repo log --oneline -1` for criterion S1.

Run prompt, identical for every arm (`<SKILL_DIR>`, `<RUN_DIR>` and `<ENTRY>` substituted):

> Read `<SKILL_DIR>/<ENTRY>` first and follow it, opening any file it points you to when its
> condition applies. When the guidance says to call the Skill tool with a skill name, read
> `<SKILL_DIR>/<name>/SKILL.md` instead. The codebase is the git repository in `<RUN_DIR>/repo/`.
> Treat `<RUN_DIR>/tmp/` as the operating system's temporary directory. You cannot open a
> browser; where the guidance says to open a file for the user, give its absolute path instead.
> This is a three-turn conversation. Do the turns in order and finish each turn's work before
> reading the next. Write what you would say to the user in each turn to
> `<RUN_DIR>/out/turnN.md`. Change files in `<RUN_DIR>/repo/` only where the guidance tells you to.
>
> Turn 1, the user says: "Survey this codebase for architecture improvements."
>
> Turn 2, the user says: "Let's explore your top recommendation. Separately, drop any candidate
> that would merge pricing rules into another module: finance audits pricing on its own and that
> will not change."
>
> Turn 3, the user says: "Yes, record that as an ADR. If you listed the legacy CSV export, skip
> it: no time this quarter. For the top candidate, take your recommended answer to each of your
> questions and settle the design."
>
> Do not mention which guidance you used. Touch nothing outside `<RUN_DIR>`.

## Fixture facts for the grader

The fixture plants these signals; the runner is never told them.

- Renewal cluster: `src/renewals/{RenewalValidator,RenewalPricing,RenewalRepoWrapper,
  RenewalNotifier}.ts` are pass-through modules. Three callers repeat the renewal sequence:
  `src/routes/renewNow.ts`, `src/jobs/nightlyRenewals.ts` (emails before commit) and
  `src/cli/adminRenew.ts` (no validation, no ledger entry). `tests/renewals.test.ts` mocks every
  step. These files carry most of the recent history.
- Ledger seam leak: `src/ledger/ledger.ts` takes the caller's `PoolClient` and asks callers to lock
  the customer row; only `src/refunds/refund.ts` does, while renewNow, nightlyRenewals and
  changePlan do not.
- Proration: `src/proration/prorate.ts` is pure and well tested; the defects are in its callers.
  `src/routes/changePlan.ts` assumes 30-day periods while `nightlyRenewals.ts` uses calendar days.
- Webhook: `src/webhooks/paymentWebhook.ts` builds `PayGateClient` and `SesMailer` inside the
  handler and has no test.
- Load-bearing module: `src/money/money.ts` is used across the codebase; deleting it scatters
  rounding and allocation rules.
- Single-adapter seam: `src/mail/IMailer.ts` has one implementation (`SesMailer.ts`) and no fake;
  tests use `jest.mock`.
- ADR-protected: `docs/adr/0002-pricing-stays-separate.md` forbids merging pricing rules out of
  `src/pricing/`.
- Dormant: `src/legacy/csvExport.ts` exists only in the initial commit.
- Domain terms are in `GLOSSARY.md`; ADR style is in `docs/adr/0001-*` and `0002-*`.

## Scoring

Score each criterion 0, 1 or 2 and give one line of evidence (file and quote). Score what the
output says or does across `out/turn1.md`, `out/turn2.md`, `out/turn3.md`, the HTML report in
`tmp/` and the final repository state. A criterion the output never addresses scores 0 unless
the row says otherwise.

### Findings

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| F1 | Scope | Uses the git history to find hot spots and names them, and reads GLOSSARY.md and the ADRs before proposing | One of the two | Neither, or scans without a stated scope |
| F2 | Renewal cluster | Finds the renewal cluster with the three repeating callers as one candidate and ranks it first or Strong, citing at least one caller divergence (email before commit, missing validation or missing ledger entry) | Found, but ranked low or without the caller divergence | Missed |
| F3 | Ledger leak | Names the `PoolClient` passed through `ledger.write` and the locking duty left to callers as a leak across the seam | Mentions the ledger coupling without the leak or lock | Missed |
| F4 | Proration | Says the pure `prorate` is fine and the defects sit in how callers use it (30 days versus calendar days), as a locality problem | Mentions proration inconsistency without placing it in the callers | Missed, or proposes changing `prorate` itself as the fix |
| F5 | Untested webhook | Flags `paymentWebhook.ts` as untested or hard to test because it constructs its clients inside the handler | Flags it without the cause | Missed |

### Discrimination

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| D1 | Load-bearing money | `money.ts` is not proposed for deletion or merging, or is explicitly kept with deletion-test reasoning (also 2 when never mentioned) | Mentioned as a mild candidate without the deletion test | Proposed for deletion or merging |
| D2 | One adapter | `IMailer` is not used to justify a port; any proposed seam names two adapters (for example production and in-memory); no new single-adapter interface | One proposed seam has only one adapter, or IMailer kept as a justified port without a second adapter | Several single-adapter seams proposed |
| D3 | Dormant code | `legacy/csvExport.ts` is absent, or present but not top-ranked and at most Speculative, with recent change as the reason | Present as Worth exploring | Top-ranked or Strong |
| D4 | ADR respect | No candidate merges pricing out of `src/pricing/`, or one does with an ADR callout naming ADR-0002 and concrete friction (also 2 when pricing is never proposed) | Proposes it with a vague ADR mention | Proposes it with no mention of the ADR |

### Report

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| R1 | Delivery | One self-contained HTML file in `<RUN_DIR>/tmp/` with a timestamped name, and its absolute path in turn 1 | File present but outside tmp, or path missing | No HTML report |
| R2 | Card completeness | Every candidate card has files, a one-sentence problem, a one-sentence solution, wins of 6 words or fewer, a side-by-side before/after diagram, a strength badge and a dependency category | One field missing on some cards | Several fields missing |
| R3 | Dependency category | Categories fit the code: Postgres-backed work as local-substitutable (pg-mem, ADR-0001) or ports and adapters, PayGate and SES as true external with a mock adapter, pure code as in-process | One wrong category | Several wrong, or none given |
| R4 | Diagrams | Diagrams use the fixture's real module names, carry the point without paragraphs, and use at least two different patterns | Real names but one pattern only, or diagrams need prose | Generic or missing diagrams |
| R5 | Offline legibility | With the CDNs blocked, the card text and at least one diagram per card stay readable (embedded styles, hand-built HTML or SVG, or readable Mermaid source) | Text readable, diagrams not | Page depends on the CDN to show content |
| R6 | Top recommendation | A top recommendation section names one candidate, gives one reason and links to its card | Present without the reason or link | Absent |
| R7 | Chat summary | Turn 1 lists every candidate in plain text (title, strength, one-line problem) with the report path and ends by asking which to explore; it proposes no interface yet | Summary present but incomplete, or an interface is already proposed | No summary in chat |

### Vocabulary

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| V1 | Terms | The output's own prose uses module, interface, seam, adapter, depth, leverage and locality correctly and avoids component, service, API and boundary as substitutes (identifiers quoted from the code do not count); domain names come from GLOSSARY.md (for example "renewal module", "ledger entry") | One or two slips | Frequent substitutes or invented domain names |
| V2 | Depth and wins | Depth is described as behaviour or leverage behind a small interface, not as line counts or a ratio; wins name the gain in those terms with no "cleaner code" or "easier to maintain" | One slip | Depth as line ratio, or fluff wins |

### Grilling and side effects

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| G1 | Grilling | Turn 2 asks about the top candidate's constraints, what sits behind the seam, the adapters needed, which tests survive or are replaced, and how the three callers migrate, each with a recommended answer | Three or four of the five, or no recommendations | Fewer, or turn 2 jumps straight to a finished design |
| G2 | ADR handling | Turn 2 offers to record the pricing reason as an ADR; after turn 3 an ADR exists in `docs/adr/` in the repository's style that records the reason and tells future surveys not to re-suggest it; no ADR is written for the "no time this quarter" reason | ADR written without the offer, or written in a different style, or a second ADR for the ephemeral reason | No ADR |
| G3 | Glossary | If the settled design names a new domain concept, GLOSSARY.md gains it in the file's format; otherwise the design reuses glossary terms (also 2) | New concept named but not added, or added in a different format | Ad-hoc names that conflict with the glossary |
| G4 | Settled design | Turn 3 settles a deep renewal module with a small interface used by all three callers; seams only where two adapters exist; tests move to the interface and the step mocks are deleted (replace, don't layer) | Two of the three | One or none |

### Safety and honesty

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| S1 | Read-only survey | No file under `src/` or `tests/` changed and no commit made; only GLOSSARY.md and `docs/adr/` changed, after the user's turn-2/3 consent | One unconsented doc change | Source changed or a commit made |
| S2 | Evidence and honesty | Findings cite real files (and lines or symbols); no invented metrics, coverage numbers or files; assumptions are marked | One unsupported claim | Invented files or numbers |

Maximum: 25 criteria, 50 points.

## Gate

The candidate passes when its score is at least Matt's on every criterion and at least the
current skill's on every criterion. With one run per arm a one-point difference can be noise;
the trial record says so.
