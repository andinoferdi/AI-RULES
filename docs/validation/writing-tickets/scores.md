# Scores: writing tickets

Scored against the frozen [rubric](rubric.md) (commit 195541c) from the collected folders. The
grader is the session that wrote the candidate and knew the arm mapping (P = None, Q = Matt,
R = Candidate), so this is not a blind or independent grading; every score cites the file or
output it rests on so it can be re-graded. Graph-check lines come from running
`ticket_graph.py` on each collected folder.

| ID | P (None) | Q (Matt) | R (Candidate) | Evidence |
| --- | --- | --- | --- | --- |
| V1 | 2 | 2 | 2 | All three cut the waitlist into join, show, holder refusal, hand-on and expiry slices, each through command, logic and storage. |
| V2 | 2 | 2 | 2 | Each arm's `01` consolidates the Slot-taken check and blocks the join ticket. All three noticed the code holds two copies, not three. |
| V3 | 2 | 2 | 2 | 24-hour expiry ticket with 23/25-hour cases in every arm; email notification stated out of scope in every arm. |
| V4 | 1 | 2 | 2 | P: ticket 06 holds the question for Dana, but its proposal says ticket 02 "allows it with no check", which decides it. Q: ticket 02 "Out of scope until Dana decides ... do not enforce or forbid it", no tracker item for the decision. R: ticket 07 `human-ready`, **Owner:** Dana, and 02 to 06 "neither build nor forbid either answer". |
| V5 | 2 | 2 | 2 | No "reservation", "queue" or "standby" in any arm's tickets. |
| A1 | 1 | 1 | 2 | P: build tickets use commands and outputs, but its three decision tickets have no criteria. Q: several criteria have no input or expected output ("A Waitlist is still there after a restart", "No code in this batch reads member_id", "Command output is unchanged"). R: every ticket, decisions included, has criteria with a command or stored state and the expected value (`roomy export --room orion --from 2026-03-02 --to 2026-03-02` prints only b-0003). |
| G1 | 2 | 2 | 2 | No unknown blocker, cycle or later-numbered blocker in any arm. |
| D1 | 0 | 2 | 2 | P: 28 path or line findings, e.g. recurring `01: file path in body roomy/store.py`, `01: line number in body line 9`. Q and R: no path or line findings. |
| T1 | 1 | 2 | 2 | All arms: right folders, one file per ticket, disclaimer first line. P labels its three decision tickets `waiting` (the needs-info string) instead of `human-ready`. |
| Q1 | 2 | 2 | 2 | Every arm wrote S1 to S4 proposals listing each ticket's title, blocker and what it delivers (Q's were written under `roomy/out/`; see S0). |
| W1 | 0 | 2 | 2 | P: one ticket renames everything in code and tests, no contract step. Q: expand 01, migrate 02 to 04, data 05, contract 06 blocked by 02 to 05. R: expand 01, migrate 02 to 06, decision 07, contract 08 blocked by 02 to 07. |
| W2 | 2 | 2 | 2 | All three keep old files loading and raise the export field name as a contract for its readers (P ticket 04, Q ticket 04, R tickets 06 and 07). |
| W3 | 0 | 2 | 2 | P: a single code batch. Q: three batches by area. R: four batches by area (booking logic, list and cancel output, usage report, export). |
| R1 | 2 | 2 | 2 | `git diff -- .scratch` is empty in every arm: export 01 and 02 unchanged, new tickets numbered 03 and 04. |
| R2 | 2 | 2 | 2 | CSV after 01, date range after 02 and 03, combination with `--room` in the criteria, and each report names what was added. |
| P1 | 0 | 2 | 2 | P: tickets 01 to 04 are plan tasks T1 to T4 ("Store a list of series (plan T1)", "The --weekly flag (plan T3)"). Q and R: one end-to-end weekly booking slice plus refusal slices. |
| P2 | 2 | 1 | 2 | P: ticket 05 holds D1 for facilities via Rin. Q: D1 appears only as a sentence in ticket 01 and the report, with no tracker item naming who answers it. R: ticket 04 `human-ready`, **Owner:** Rin (asking facilities). |
| S0 | 2 | 1 | 2 | Tracked diff outside `.scratch` empty in every arm. Q wrote its proposal files to `roomy/out/` inside the repository instead of `<RUN_DIR>/out`. |
| F1 | 2 | 2 | 2 | P wrote `out/report.md`. Q's and R's writes of `out/report.md` were refused by the host's Write tool; both reports were taken verbatim from the runner's final message (see trial.md). Each lists tickets per request and what can start now. |
| **Total (of 38)** | **27** | **35** | **38** | |
