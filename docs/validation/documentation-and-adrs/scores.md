# Scores: documentation and ADRs trial

Written by the blind grader (Sonnet 5.5, medium effort) against the [rubric](rubric.md). The grader
saw the arms as A, B and C; the mapping, revealed after grading, is A = Addy, B = Candidate,
C = Current. Column headers below keep the letters the grader used.

## Task 1
| ID | A | B | C |
|---|---|---|---|
| A1 | 2: architecture/decisions/0009-...md, template headings and Status/Deciders/Date | 2: same | 2: same |
| A2 | 2: 0009, reservation noted | 2: same | 2: same |
| A3 | 2: "proposed", "Rina Hartono (decides on 2026-11-27)" | 2: same | 2: same |
| A4 | 2: index row proposed, 0004 untouched, linked | 2: same | 2: same |
| A5 | 1: pros/cons per option on different points, no shared criteria | 2: "judged on the same criteria (a)-(e)" per option | 1: pros/cons on differing points |
| A6 | 2: INC-311, 900, "once", staging, 5%, 1,200, 41 s, 30 s | 2: same | 2: same |
| A7 | 2: "not supported... not part of the proposal" | 2: "not measured" | 2: "unmeasured and not adopted" |
| A8 | 1: one-worker and retention, no revisit trigger | 2: one worker, retention, "Revisit trigger" p95 >60 s / second worker | 2: single worker, retention, "Revisit:" re-measure / before >1 worker (weakly measurable) |

## Task 2
| ID | A | B | C |
|---|---|---|---|
| B1 | 2: reason, required <24h, max 200 | 2 | 2 |
| B2 | 2: full / half rounded down | 2 | 2 |
| B3 | 1: all five outcomes, caller action only for 409 | 2: "What the client should do" column | 1: "When" column, action only for 409 and "correct and send again" |
| B4 | 2: "no longer a safe retry", 409, no repeat refund, no e-mail on rejected | 2: not idempotent, before/now table | 2: "used to return 200... now 409", no e-mail |
| B5 | 1: "on a successful cancellation only" | 2: "once per successful cancel" | 1: "when the booking is cancelled", 409 no e-mail |
| B6 | 1: Added/Changed under Unreleased, 409 change but no "breaking" label | 2: "**Breaking:**" labels and client actions | 1: no breaking label, action to treat 409 as success |
| B7 | 2: insert-only under Unreleased | 2 | 2 |
| B8 | 2: "Docs were not executed beyond [tests]", compared with code | 2: ran api.handle_cancel scenarios | 2: ran handler example, "Not checked: no HTTP server" |

## Task 3
| ID | A | B | C |
|---|---|---|---|
| C1 | 2: 15->20, code and CHANGELOG | 2: WEEKEND_SURCHARGE_PERCENT = 20 | 2: hall/pricing.py |
| C2 | 2: both lines to 2 h | 2 | 2 |
| C3 | 2: accurate, rename-only commit, unchanged | 2 | 2 |
| C4 | 2: "commit order is can't tell", decided from code | 2: "can't tell (parallel branches merged)" | 1: accurate from code, no mention history cannot decide |
| C5 | 2: dated entries with reason appended at end | 2: appended, with reason (since commit) | 1: pricing entry has no reason; reminders entry inserted before the 2026-09-20 entry, not at end |
| C6 | 2: four docs, verdict, history+content | 2: table | 1: four verdicts, no history evidence for auth/pricing/reminders |

## Task 4
| ID | A | B | C |
|---|---|---|---|
| D1 | 2 | 2 | 2 |
| D2 | 2 | 2 | 2 |
| D3 | 1: removed, report lists it as removed, not as follow-up | 2: "Follow-up: decide what invalid input should do" | 1: removed as "no owner or issue", no follow-up |
| D4 | 2: TODO(#88) kept (moved) | 2 | 2 |
| D5 | 1: naive times, host tz, ADR-0005, but no Europe/Amsterdam | 2: Amsterdam, UTC host, 2 h (1 winter), ADR-0005 | 1: no Amsterdam, no consequence |
| D6 | 2: comment lines only, 22 OK | 2 | 2 |

## Whole run
| ID | A | B | C |
|---|---|---|---|
| E1 | 2: run vs read separated | 2 | 2 |
| E2 | 2: no commit, only needed files, 22 OK | 2 | 2 |

## Totals
| Section | A | B | C |
|---|---|---|---|
| Task 1 (16) | 14 | 16 | 15 |
| Task 2 (16) | 13 | 16 | 13 |
| Task 3 (12) | 12 | 12 | 9 |
| Task 4 (12) | 10 | 12 | 10 |
| Whole run (4) | 4 | 4 | 4 |
| Total (60) | 53 | 60 | 51 |

## Close calls
- A8 for C (1 vs 2): "Revisit" line is re-measure / before second worker, not a measured delay budget.
- B5 for A and C (1 vs 2): "successful cancellation only" / 409 queues no e-mail implies once-only but is not stated.
- B6 for A and C (1 vs 2): the 409 change is described as a change with client action, but not labelled breaking.
- B3 for C (1 vs 2): "When" column plus generic "safe to correct and send again" only partly gives caller action.
- C6 for C (1 vs 2): verdicts for all four but history evidence missing for most.
- A5 for A and C (1 vs 2): pros/cons are partly parallel (ADR-0002, single-kill) but not the same points.
