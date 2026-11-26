# Blind grading, first run (2026-11-26)

Grader: one Claude Code subagent, Sonnet 5.5 at medium effort, given only the rubric, the fixture
and the four output folders labelled A-D. Mapping, revealed after grading: A unguided control,
B candidate (branch commit 713bfd4), C current skill (main 49ad00b), D Addy Osmani's skill
(addyosmani/agent-skills 9c7f62d).

| ID | A control | B candidate | C current | D Addy |
| --- | --- | --- | --- | --- |
| S1 | 2 | 2 | 2 | 2 |
| S2 | 0 | 2 | 2 | 2 |
| S3 | 1 | 2 | 2 | 2 |
| S4 | 2 | 2 | 2 | 2 |
| S5 | 2 | 1 | 1 | 2 |
| S6 | 2 | 2 | 2 | 2 |
| S7 | 2 | 2 | 1 | 2 |
| S8 | 2 | 1 | 2 | 2 |
| S9 | 2 | 2 | 2 | 2 |
| S10 | 2 | 2 | 2 | 2 |
| S11 | 2 | 2 | 2 | 1 |
| S12 | 2 | 2 | 2 | 2 |
| S13 | 2 | 2 | 2 | 2 |
| S14 | 2 | 2 | 2 | 2 |
| S15 | 1 | 2 | 2 | 1 |
| V1 | 2 | 2 | 2 | 2 |
| V2 | 2 | 2 | 2 | 2 |
| V3 | 2 | 2 | 2 | 2 |
| V4 | 2 | 2 | 2 | 2 |
| V5 | 2 | 2 | 2 | 2 |
| V6 | 1 | 2 | 2 | 1 |
| V7 | 2 | 2 | 2 | 2 |
| V8 | 1 | 2 | 2 | 2 |
| P1 | 2 | 2 | 2 | 2 |
| P2 | 1 | 2 | 1 | 2 |
| Q1 | 2 | 2 | 2 | 2 |
| Q2 | 2 | 2 | 2 | 2 |
| Total (of 54) | 47 | 52 | 51 | 51 |

## Grader evidence for the criteria where the arms differ

- S2: A asked 11 questions, most without a default and with no cost note. B, C and D asked four, each
  with a guess and a default, and named the URL and rules-file costs; each added one or two authority
  questions, which the grader still scored 2 (flagged as a judgement call).
- S3: A kept its numbers in `quality/floor.json` with no measured section in the contract; B, C, D
  had every part.
- S5: B and C enforced lint and tests for both deployables but left api coverage, types and the
  ratchets pending; A and D gave each deployable lint or types, tests and coverage.
- S7: C declared the missing coverage provider and had no changed-line computation; A, B and D
  computed changed-line coverage from the report and the diff (B declared the provider as pending,
  A and D added it).
- S8: B wired gitleaks with `--redact` and Semgrep through the quality gate but left dependency
  scanning pending because the copy had no lockfile; A, C and D wired osv-scanner in CI.
- S11: D left the existing edit hook untouched and relied on an `AGENTS.md` instruction for task
  end; A, B and C used or extended the hook.
- S15: A's exception file had no ticket, no individual owner and no expiry limit; D had no ticket or
  narrow-path rule; B and C had every field and the 90-day limit.
- V6: A listed the warning-cap tightening under "Blocks the merge"; D described the W1 removal as
  harmful; B and C treated both as tightening.
- V8: A quoted the full fake key in its review; B, C and D did not.
- P2: A and C wrote only a proposal file in the unattended scenario and applied no guard; B and D
  applied a floor-only contract and the diff guard and flagged the rest.

## Calls the grader was least sure about

- S2 for B, C and D (authority questions beyond four; strict reading gives 1 each).
- S8 for A, C and D (osv-scanner has no severity filter and no lockfile exists; scored 2 as
  stricter than required).
- V6 for A and D, and possibly C.
- S5 and S7 for C (coverage deferred entirely).
- S11 for D.
