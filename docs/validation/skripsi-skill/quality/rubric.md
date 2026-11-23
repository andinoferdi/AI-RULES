# Skripsi quality evaluation: rubric and protocol

Purpose: compare thesis-artifact quality across arms on the same tasks. This is a
bounded, model-judged comparison on synthetic fixtures, not proof of general behavior.

## Tasks

QUAL-01…QUAL-06 in `evals/skripsi-skill.json` (fixtures in `evals/skripsi-fixtures.json`)
are the six comparison tasks: BAB I draft, BAB II synthesis and framework, BAB III draft,
revision from supervisor notes, BAB IV–V discussion and conclusion with a null result,
and defense preparation. Their `expected` and `forbidden` fields are the must and
must-not lists. QUAL-07…QUAL-12 are additional behavior cases for live runs.

## Arms

Each arm answers all six tasks in one isolated actor context, task by task, with the
same model and effort, writing one reply file per task:

- `vanilla`: no skill files.
- `old`: skripsi-skill at the base revision of the upgrade.
- `reference`: AlterLab `alterlab-thesis-supervisor` plus selected `alterlab-paper-writer`
  and `alterlab-deep-research` guidance (closest MIT reference that one agent can run).
- `new`: the upgraded skripsi-skill.

Actors never see the oracle fields, the rubric or other arms' outputs.

## Scoring (1–5 per dimension)

| Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- |
| D1 Artifact delivery | Mostly process talk or outline; artifact missing | Artifact present but partial or padded with meta commentary | Full requested artifact, usable as a draft; meta kept to a short note |
| D2 Specificity and depth | Generic text that fits any thesis | Mixed generic and case-specific | Every paragraph tied to this case, its sources and constraints |
| D3 Academic reasoning | Claims listed without argument; misaligned RQ and method | Argument present with gaps | Clear argument chain; synthesis and comparison; RQ, method and analysis aligned |
| D4 Evidence integrity | Fabrication or causal overclaim | No fabrication but weak flagging | No fabrication; claim strength matches design; gaps visibly marked |
| D5 Indonesian academic language | Stiff, machine-sounding or informal | Acceptable with formulaic phrases | Natural formal Indonesian, precise terms, no filler |
| D6 Next-step usefulness | No guidance or generic advice | Some next steps | Specific, prioritized next actions and open decisions |

Per task also record: must items met (count of total), must-not violations (list), and
whether internal labels (for example PARTIALLY_READY, PLAUSIBLE, UNKNOWN) appear in the
reply.

## Judging protocol

1. Shuffle arms per task into letters; keep the mapping with the coordinator only.
2. A judge reads the task fixture, the oracle fields and all lettered replies for that
   task, scores D1–D6, records must and must-not results, and ranks the replies 1–4
   (1 = best) with a one-line reason.
3. Two judges split the six tasks (three each). The coordinator reveals the mapping only
   after all judgments and tallies mean rank and dimension means per arm.
4. Surface metrics (word counts, prose share, label count) from the outputs are recorded
   separately as signals, never as the verdict.

## Known fixture inconsistency

The `final` fixture states rho = 0,12, p = 0,21 with n = 40. For a correlation of 0,12 on
40 cases the t approximation gives about p = 0,46 two-sided (0,23 one-sided). The fixture
is kept unchanged so all arms see the same input. Keeping the given numbers while flagging
the p-value for verification is correct behavior, not an error; silently "correcting" the
value without the analysis output would be an integrity violation.

## Acceptance for the upgrade

`new` mean rank ≤ `reference` mean rank across the six tasks; `new` ranks above `old` on
at least five of six tasks; zero must-not violations and zero internal labels for `new`;
QUAL-01 background between 810 and 1,320 words.
