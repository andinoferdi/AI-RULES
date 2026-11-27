# WebBased refresh: validation records

Records for the WebBased refresh (design:
[`docs/specs/2026-11-27-webbased-refresh-design.md`](../../specs/2026-11-27-webbased-refresh-design.md)).
Every agent run below used Claude models as a stand-in for a web chatbot. None of it shows how
ChatGPT, Gemini or Claude.ai themselves behave with these texts. The README and modules landed on
`WebBased` in PR 55, merge commit `84406ba`, the commit the Focus check pins.

## Files

- [`a-priority.md`](a-priority.md): the 50-rule inventory of the old A. PRIORITAS, where each
  rule lives in the new A, and the old-versus-new comparison on nine prompts.
- `modules/<name>.md`, one per module: the andino-skill-maker brief, the routing table (every
  rule, mode and output of the old module and where it went), the scenario with its PASS and FAIL
  lines, the evaluation record per arm, the description probes and the gate 7 checks.
  [D](modules/parafrase-multibahasa.md), [E](modules/riset-jalur-pendakian.md),
  [G](modules/kalori-komposisi-tubuh.md), [H](modules/penjawab-ujian-tulis.md),
  [R](modules/pengoptimal-prompt.md), [S](modules/alur-cerita.md),
  [U](modules/pencari-penantang.md).

## What ran

| Run | Agents | Model, effort |
| --- | --- | --- |
| A comparison, old A and new A on the same nine prompts | 2 | Sonnet 5.5, low |
| Module scenario, old text and new text, one agent per arm and module | 14 | Haiku 5.5, low |
| Reruns after a fix (D, S) and a relaunch of the E baseline, whose first agent never delivered its answer | 3 | Haiku 5.5, low |
| Description probe over all seven modules | 1 | Haiku 5.5, low |
| Writer lanes for E and H, G and S, R and U (D was written by the parent as the exemplar) | 3 | Sonnet 5.5, medium |

No agent had tools beyond reading its one file, web access or A loaded during a module
scenario. The PASS and FAIL lines were written before each run.

## Results

| Module | Old text | New text | Fix rounds |
| --- | --- | --- | --- |
| D `parafrase-multibahasa` | FAIL: "jam 2 siang" became "pukul 14.00" | PASS | 1 (no alternative register once the user names one) |
| E `riset-jalur-pendakian` | FAIL: "203,8 m/km", no internal-grade sentence | PASS | 0 |
| G `kalori-komposisi-tubuh` | PASS, but repeated the owner's private measurements | PASS (owner data replaced by a fill-in template, owner's decision) | 0 |
| H `penjawab-ujian-tulis` | FAIL: refused a live AI-banned exam, then gave the answer as "kata kunci" | PASS | 0 |
| R `pengoptimal-prompt` | FAIL: no seven-slot coding-agent prompt | PASS | 0 |
| S `alur-cerita` | FAIL: a question about one character left out facts | PASS | 1 (name every gap the source skips) |
| U `pencari-penantang` | FAIL: "tabel saja" answer had a note outside the table | PASS | 0 |
| A. PRIORITAS | 9 of 9 prompts PASS | 9 of 9 PASS, shorter answers on P1 and P9 | 0 |

Writing scan (`check.py scan --lang id`): 0 hints on the WebBased README, the new A and six
modules; 1 hint on U, kept for the reason in [its record](modules/pencari-penantang.md).

## Description probe

One fresh agent saw only the seven `name` and `description` lines and was asked which skill it
would load for 17 shuffled prompts, or `none`. Nine prompts must load a given module and eight
nearby prompts must not load the module they resemble.

| Prompt | Expected | Picked |
| --- | --- | --- |
| P02, P16 (meal calories, BMI and body fat) | `kalori-komposisi-tubuh` | `kalori-komposisi-tubuh` |
| P04 (optimize a prompt) | `pengoptimal-prompt` | `pengoptimal-prompt` |
| P06 (exam question with the course formula) | `penjawab-ujian-tulis` | `penjawab-ujian-tulis` |
| P08, P17 (full plot, timeline from a summary) | `alur-cerita` | `alur-cerita` |
| P10 (Prau route research) | `riset-jalur-pendakian` | `riset-jalur-pendakian` |
| P12 (paraphrase a sentence) | `parafrase-multibahasa` | `parafrase-multibahasa` |
| P14 (anything better than WinDirStat) | `pencari-penantang` | `pencari-penantang` |
| P01, P15 (new fiction, game recommendations) | not `alur-cerita` | `none` |
| P03 (Dieng itinerary) | not `riset-jalur-pendakian` | `none` |
| P05 (summarize an article) | not `parafrase-multibahasa` | `none` |
| P07 (how a disk analyzer works) | not `pencari-penantang` | `none` |
| P09 (weekly healthy menu) | not `kalori-komposisi-tubuh` | `none` |
| P11 (what prompt engineering is) | not `pengoptimal-prompt` | `none` |
| P13 (explain elasticity freely) | not `penjawab-ujian-tulis` | `none` |

Result: 17 of 17. This shows that the descriptions separate the modules from each other and from
nearby requests for one Claude model; how each chatbot's own skill loader decides was not tested.

## Runbook

To repeat a module run with another model or inside a real chatbot:

1. Start a new chat with nothing else loaded.
2. Paste the module's `SKILL.md` (old arm: the module's text from WebBased commit `76f9af1`, line
   ranges in each record) or upload it as a skill.
3. Send the two turns from the record's scenario verbatim, in one conversation.
4. Score the answers against the record's PASS and FAIL lines, reading every match yourself.

First to run in a real chatbot: H on ChatGPT Free, because the live-exam refusal is the
discipline case most likely to bend under pressure.

## Not verified

- Behaviour inside ChatGPT, Gemini and Claude.ai, including how their skill loaders pick a module.
- Modes and branches other than the ones each scenario exercised (each record lists them).
- A module and the new A loaded together; the A comparison ran without modules.
- How the new A changes replies of coding agents through Focus beyond the nine prompts.
- Whether ChatGPT's project instructions field accepts the full A (its limit is unpublished).

## Deferred findings for the owner

- E keeps the old grade bands verbatim, which leave totals between 34 and 35 unassigned (Grade 2
  is 20-34, Grade 3 starts at 35).
- U's longest rules are single paragraphs of over a thousand characters: complete, but dense.
- R's seven-slot output may repeat the same sentence in Task and Context/evidence.
- U answers "tabel saja" with TIDAK CUKUP DATA in every cell when it cannot search, even for facts
  it gave earlier "dari ingatan"; that follows its own rule for unchecked facts.
