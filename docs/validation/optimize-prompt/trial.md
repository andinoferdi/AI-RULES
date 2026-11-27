# Comparison trial: optimize-prompt

Run on 2026-11-26 on the fixture in `fixture/`, scored against the [rubric](rubric.md), which was
frozen (commit ede6737) before the candidate was written. Every arm ran once; one blind grader
scored all six outputs together.

Result: the candidate scored 32 of 32 from the grader, against 26 for the current skill, 18 for
ECC, 17 for Sentry, 14 for Hashaam101 and 13 for awesome-copilot. A stricter reading of one
criterion (A2, below) gives the candidate 31. It meets the gate either way: highest total, and every
K criterion at least as high as the current skill's.

## Setup

- Arms: the current `andino-optimize-prompt` (AI-RULES main at 1e78323); ECC `prompt-optimizer`
  (affaan-m/ECC); GitHub awesome-copilot `prompt-optimizer`; Sentry `prompt-optimizer`
  (getsentry/skills, with its four references, `SPEC.md` and `SOURCES.md`); Hashaam101
  `prompt-optimizer`; the candidate (branch `claude/optimize-prompt-skill-upgrade-5522f1`, skill
  folder as committed with this record). Reference skills were downloaded from each repository's
  default branch on 2026-11-26.
- Runners: six Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each with the
  rubric's run prompt, its own skill copy and its own run folder. The five baseline arms ran before
  the candidate was written. The candidate's runner reported one deviation: it read all six prompt
  files in one batch instead of opening each when it started it.
- Blinding: outputs were shuffled to letters (A Sentry, B candidate, C ECC, D current, E Hashaam101,
  F awesome-copilot) and scanned for names of the guidance used; none appeared. The grader, one
  Sonnet 5.5 subagent at medium effort, saw the rubric with the arm list removed, the fixture and the
  six output folders. Its scores and evidence are in [scores.md](scores.md).

## Scores

| Group | Sentry | Candidate | ECC | Current | Hashaam101 | awesome-copilot |
| --- | --- | --- | --- | --- | --- | --- |
| Keeping what the user wrote (K1-K4, max 8) | 2 | 8 | 4 | 8 | 4 | 2 |
| Making the prompt actionable (A1-A5, max 10) | 6 | 10 | 6 | 5 | 3 | 4 |
| Gaps, diagnosis and delivery (Q1-L1, max 14) | 9 | 14 | 8 | 13 | 7 | 7 |
| Total (max 32) | 17 | 32 | 18 | 26 | 14 | 13 |
| Words across the six replies | 2897 | 1495 | 4314 | 621 | 2756 | 1838 |

## What the baseline showed

- The current skill kept every choice and fact but never read the project: no test command, no
  file facts, no verification step (A1 0, A4 0), and on p5 it asked for the Next.js version that
  `package.json` already shows.
- ECC and Sentry read the project and added strong verification (characterization tests, failing
  test first, before and after measurement), but rewrote the user's shape into their own template
  (K4 0), wrote a suspected cause or invented requirements into the prompt (K3 0) and ran long. ECC
  also handed back two versions of every prompt.
- awesome-copilot produced the most directive prompts and a self-check, but invented requirements
  and options (CSV escaping and permissions on p3, a list of auth libraries on p5, three visual
  directions on p2), settled the `ponytail` conflict itself and gave no explanation.
- All three strong references told the refactor agent to report odd behaviour without fixing it;
  the candidate's refactor row adopts that as part of its verification step.

## What changed in the candidate

The task checklists (`resources/intent-checklists.md`), the project read with a source for each
fact, the labelled added blocks (`fakta proyek (dicek)`, `batasan`, `selesai jika`, `verifikasi`,
or the template's own slots), the diagnosis table and the sibling heading layout. The pin rules,
inventory step, three-question limit and run-only-after-yes rule are unchanged.

## Limits

- The grader's totals row gives the current skill 27; its own per-criterion scores add up to 26,
  which this record uses. The other five totals match their columns.

- One run per arm and one grader from one model family. The A2 score for the candidate is
  generous: on p3 its done-when checks the saved plan ("a plan is saved that names ... files ...
  and the check") rather than the rubric's example, the admin orders page offering a CSV export.
  Scored 1, the candidate total is 31.
- The rubric weighs keeping the user's text (4 of 16 criteria) because that is the skill's purpose;
  on the actionability criteria alone the candidate scored 10 of 10 against 6 for ECC and Sentry.
- The fixture is one small Next.js project. Behaviour on other stacks, very long prompts or prompts
  about another project than the working directory was not run.
