# Skripsi quality baseline and G1 checkpoint

Date: 2026-11-23. Host: Claude Code subagents, model Sonnet, effort medium, one isolated
actor context per arm, six tasks answered in order (inputs: [actor-tasks.md](actor-tasks.md);
oracles and rubric: QUAL-01…06 in `evals/skripsi-skill.json`, [rubric](rubric.md)).
Outputs: `outputs/<arm>/Q0n.md`. Arms `vanilla`, `old` (skripsi-skill at
4bc769c3db95eab11463fe12b0a53a28ab8006a7) and `reference` (AlterLab thesis-supervisor +
paper-writer guidance, commit 3ab6d034385ec4fedc3f6f4099292d4e91f60300) ran before any
change; `new-g1` ran on the uncommitted working tree after Phase 1–2 content was written.

Status: surface metrics and coordinator reading only. Not blind-judged; the blind
comparison is gate G2 with the final skill.

## Surface metrics

Signals, not verdicts. `prose%` = share of words outside list, table, heading and quote
lines; `status_labels` = internal labels such as PARTIALLY_READY, PLAUSIBLE, UNKNOWN.

| Task | Arm | Words | Prose % | Bullets | Table rows | Status labels | Placeholders |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q01 BAB I | vanilla | 1147 | 64 | 11 | 0 | 0 | 0 |
| Q01 BAB I | old | 1082 | 65 | 14 | 0 | 1 | 0 |
| Q01 BAB I | reference | 1060 | 60 | 11 | 0 | 0 | 0 |
| Q01 BAB I | new-g1 | 1277 | 87 | 5 | 0 | 0 | 7 |
| Q02 BAB II | vanilla | 1089 | 14 | 7 | 9 | 0 | 0 |
| Q02 BAB II | old | 1052 | 19 | 11 | 6 | 0 | 0 |
| Q02 BAB II | reference | 1187 | 57 | 8 | 9 | 0 | 0 |
| Q02 BAB II | new-g1 | 1284 | 75 | 5 | 9 | 0 | 3 |
| Q03 BAB III | vanilla | 993 | 17 | 10 | 4 | 0 | 4 |
| Q03 BAB III | old | 1080 | 33 | 16 | 4 | 1 | 11 |
| Q03 BAB III | reference | 1046 | 25 | 13 | 12 | 0 | 0 |
| Q03 BAB III | new-g1 | 1155 | 79 | 5 | 4 | 0 | 16 |
| Q04 revision | vanilla | 616 | 56 | 11 | 0 | 0 | 2 |
| Q04 revision | old | 726 | 10 | 5 | 0 | 0 | 0 |
| Q04 revision | reference | 826 | 9 | 11 | 6 | 0 | 0 |
| Q04 revision | new-g1 | 837 | 51 | 4 | 6 | 0 | 4 |
| Q05 BAB IV–V | vanilla | 989 | 19 | 21 | 0 | 0 | 0 |
| Q05 BAB IV–V | old | 887 | 17 | 22 | 0 | 1 | 0 |
| Q05 BAB IV–V | reference | 1052 | 6 | 21 | 0 | 0 | 0 |
| Q05 BAB IV–V | new-g1 | 994 | 70 | 8 | 0 | 0 | 3 |
| Q06 defense | vanilla | 817 | 27 | 23 | 8 | 0 | 0 |
| Q06 defense | old | 848 | 30 | 20 | 10 | 1 | 0 |
| Q06 defense | reference | 1060 | 38 | 23 | 18 | 0 | 0 |
| Q06 defense | new-g1 | 856 | 21 | 16 | 16 | 0 | 0 |

The surface label counter matches only bare labels; a manual grep of the `old` arm found
"(PARTIALLY_READY)" in Q01 and Q03, "(PLAUSIBLE)" three times in Q05 and "(UNKNOWN)" in
Q06. Q01 background (1.1) word count: vanilla 630, old 789, reference 639, new-g1 850
(requested 900–1,200).

## Coordinator reading

- All arms avoided invented sources and statistics, reported the null result honestly and
  caught the "Pengaruh" title and the BAB V overclaim. Integrity did not separate the arms.
- `old` opened drafts with a status block, leaked internal labels and wrote BAB II and
  BAB IV discussion mostly as lists.
- `reference` wrote BAB II and BAB IV as argued paragraphs with captioned tables.
- `new-g1` delivered each artifact first, wrote BAB I–IV as connected prose, kept labels
  out of the text and used placeholders for missing context and bibliographic data. It
  also flagged that p = 0,21 is inconsistent with rho = 0,12 at n = 40 (see rubric) while
  keeping the given numbers. Its closing note reported the background as "sekitar 900
  kata" against a counted 850; the length rule now requires the counted number and
  aiming for the middle of a range.

## G1 result

Thresholds from the plan: internal labels 0 on all six (met), BAB II prose share ≥ 50%
(75%, met), Q01 background 810–1,320 words (850, met), no must-not violation in the
coordinator reading (none found). G1 passed; G2 decides acceptance.
