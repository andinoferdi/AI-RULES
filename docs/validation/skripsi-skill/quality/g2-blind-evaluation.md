# G2 blind quality evaluation

Date: 2026-11-24. Actors: Claude Code subagents, Sonnet, effort medium, one isolated
context per arm (inputs: [actor-tasks.md](actor-tasks.md)). Arm `new` = skripsi-skill at
commit 9ff7cd69 (skill files identical to d85a01a). Arms `vanilla`, `old`, `reference`
are the baseline runs in [baseline.md](baseline.md). Judges: two Claude Code subagents,
Sonnet, effort medium; judge 1 scored QUAL-01…03, judge 2 QUAL-04…06, using the oracle
lists and the [rubric](rubric.md). Arms were shuffled per task into letters A–D
([mapping.json](judging/mapping.json), revealed only after both judges finished); judge
notes are in [judging/](judging/). Outputs: `outputs/<arm>/Q0n.md`.

Scope of proof: six synthetic tasks, one model family for actors and judges, one run per
arm. This shows the upgraded skill outperformed the other arms on these tasks under these
conditions; it is not proof of behavior on other models, hosts or real theses.

## Rankings (1 = best)

| Task | new | reference | vanilla | old |
| --- | --- | --- | --- | --- |
| QUAL-01 BAB I | 1 | 4 | 2 | 3 |
| QUAL-02 BAB II | 1 | 3 | 4 | 2 |
| QUAL-03 BAB III | 1 | 3 | 2 | 4 |
| QUAL-04 revision | 1 | 2 | 4 | 3 |
| QUAL-05 BAB IV–V | 2 | 3 | 1 | 4 |
| QUAL-06 defense | 1 | 2 | 3 | 4 |
| **Mean rank** | **1.17** | 2.83 | 2.67 | 3.33 |

## Judge observations on the `new` arm

- QUAL-01: the only reply inside the requested length (section 1.1 measured 1,010 words by
  the judge; the other arms 543–629). Clear chain from Program P context to RQ; specific
  placeholders. No must-not violations; no internal labels.
- QUAL-02: "cleanest and most usable chapter"; S2 vs S5 contrasted by population,
  measured aspect and instrument validity; every framework link tied to a source.
- QUAL-03: reads like chapter prose in planned tense with few inline placeholders; weaker
  than other arms on next steps (D6 = 3).
- QUAL-04: the only reply mapping each of the four supervisor comments to a location and
  status, with tracked changes and reasons; caught non-statistical "signifikan".
- QUAL-05: ranked second; the `vanilla` reply was preferred for a per-source comparison
  that also checked the Pearson/Spearman change and gave a fuller limitations list.
- QUAL-06: the only reply with full answer cards (answer, rationale, evidence location,
  boundary, follow-up), fixing BAB V and the title first.

Judges also found issues in other arms: the invented detail that S3 "interviewed"
students (old, reference, vanilla), internal labels in student-facing text (old in
QUAL-01, QUAL-03, QUAL-05, QUAL-06), a causal slip and an out-of-scope source in the
reference arm, and length misreports.

## Acceptance (plan R12)

| Criterion | Result |
| --- | --- |
| `new` mean rank ≤ `reference` mean rank | 1.17 ≤ 2.83 — met |
| `new` above `old` on ≥ 5 of 6 tasks | 6 of 6 — met |
| Zero must-not violations for `new` | 0 recorded by both judges — met |
| Zero internal labels for `new` | 0 (judges and grep) — met |
| QUAL-01 background 810–1,320 words | 1,014 by script (1,010 by judge) — met |
