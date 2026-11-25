# AI Codebase Rescue: checkout fixture trial

Date: 2026-11-25. Purpose: compare rescue work with no skill, the previous skill, the
reference collections it was compared against, and the upgraded skill, on one task.

## Setup

- Fixture: a checkout service built by [build_checkout_fixture.py](build_checkout_fixture.py)
  (11 commits of patch-on-patch history). Planted defects and expected treatment are in
  [checkout-oracle.md](checkout-oracle.md), written before any run.
- Task given to every arm (identical): users report that the cart preview total sometimes
  differs from the amount charged and that some failed payments were reported as
  successful; rescue the checkout subsystem, with edits and commits authorized inside the
  disposable repository only, standard library only, no network.
- Host: Claude Code subagents, model sonnet, effort medium, one trial per arm, each arm on
  its own fresh copy of the fixture. Installed skills were not loaded; each arm read only
  the skill files named in its prompt.
- Grading: repository state (commits, diffs, test run) and the final report, scored against
  the oracle: 8 defect items and 9 process items, 0 missed, 1 partial, 2 full (max 34).

## Results

| Arm | Skill files | Defects /16 | Process /18 | Total /34 | Tokens / tool uses |
| --- | --- | --- | --- | --- | --- |
| Control | none | 12 | 10 | 22 | 81k / 4 |
| Previous skill | `skills/ai-codebase-rescue` at 4b98247 | 16 | 16 | 32 | 97k / 9 |
| Reference | Rune rescue, autopsy, safeguard, surgeon, hallucination-guard; Wondel.ai working-with-legacy-code | 15 | 17 | 32 | 136k / 20 |
| Upgraded skill | this branch, snapshot before review (see note) | 16 | 17 | 33 | 104k / 13 |

Previous skill versus reference:

- Reference did better: characterization tests committed before any change with known
  bugs pinned and flipped in each fix commit; one commit per concern; a git-churn starting
  point; both phantom imports fixed; downstream impact (orders already marked paid with no
  transaction need reconciliation; callers must handle the new failed status).
- Previous skill did better: findings with severity, confidence and disposition; a
  test-trust verdict; KEEP for healthy areas; no invented health score and no state file or
  tags written into the project; lower cost.
- Previous skill's process slips: tests were written red-first but did not pin current
  behavior; the deletion of the duplicate module landed in the payment commit.

Upgraded skill, observed from the repository and report:

- 19 characterization pins committed first, with known bugs named after their finding IDs;
  the pin commit passes on the unmodified code (rechecked by the grader).
- Six commits, one concern each: two behavior fixes that flip exactly their known-bug pins,
  then the preview change, the duplicate module removal (after a code, test and config
  consumer check), the phantom package removal and an explicit unsupported-currency error.
- KEEP for tax rules and for the config-loaded tax plugin; no health score, state file or tag.
- Report in the rescue-report shape: severity, confidence and disposition per finding,
  PASS/UNVERIFIED checks, owner decisions, and downstream impact including orders already
  stored as paid without a transaction that need reconciliation.
- Remaining gap: the starting point came from the symptoms and history, without a churn
  ranking (process item P7 scored 1); the triage reference was not opened.

## Limitations

The upgraded arm ran on a snapshot taken before review. Review then restored four
passages from the previous skill to SKILL.md (missing-test fallback, risk signals to
inspect, the justified-boundary rule and the report's remake-gate, risk and blocker
fields). These are rules the previous arm also had; the committed skill was not rerun.

One trial per arm, one fixture, one model family. The same author wrote the fixture, the
oracle and the upgraded skill, so the upgraded arm can overfit; the skill's worked example
uses an unrelated domain to reduce that risk. Scores grade observable behavior on this
fixture only and do not establish behavior on other codebases or hosts.
