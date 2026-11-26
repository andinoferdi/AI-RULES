# Grader scores: skill-maker

Blind scores from one grader (Sonnet 5.5, medium) who saw only the rubric, the fixture and runs
A to E. Letters, revealed after grading: A Addy `using-agent-skills`, B obra `writing-skills`,
C candidate, D current `andino-skill-maker`, E no skill. The text below is the grader's file
unchanged.

# Scores

Note: the rubric lists 23 criteria (M1-M11, E1-E8, N1-N2, Q1-Q2), so the real maximum is 46, not 42. Totals below are out of 46. No run shows a Skill, slash command or subagent call.

| ID | A | B | C | D | E |
|----|---|---|---|---|---|
| M1 | 2 | 2 | 2 | 2 | 2 |
| M2 | 2 | 2 | 2 | 2 | 2 |
| M3 | 2 | 2 | 2 | 2 | 2 |
| M4 | 2 | 2 | 2 | 2 | 2 |
| M5 | 1 | 1 | 2 | 1 | 1 |
| M6 | 2 | 2 | 2 | 2 | 2 |
| M7 | 2 | 2 | 2 | 2 | 2 |
| M8 | 0 | 0 | 2 | 0 | 0 |
| M9 | 2 | 2 | 2 | 2 | 2 |
| M10 | 2 | 2 | 2 | 2 | 2 |
| M11 | 2 | 2 | 2 | 2 | 2 |
| E1 | 2 | 2 | 2 | 2 | 2 |
| E2 | 1 | 2 | 2 | 2 | 1 |
| E3 | 2 | 1 | 2 | 2 | 1 |
| E4 | 2 | 2 | 2 | 2 | 2 |
| E5 | 2 | 2 | 2 | 2 | 2 |
| E6 | 2 | 2 | 2 | 2 | 2 |
| E7 | 2 | 2 | 2 | 2 | 2 |
| E8 | 1 | 1 | 2 | 1 | 0 |
| N1 | 2 | 2 | 2 | 2 | 1 |
| N2 | 2 | 2 | 2 | 2 | 2 |
| Q1 | 2 | 2 | 2 | 2 | 2 |
| Q2 | 1 | 1 | 2 | 2 | 1 |
| **Total (/46)** | **40** | **40** | **46** | **42** | **37** |

## Evidence

### A
- M1: skill "Not reasons to skip the check: the migration is only a nullable column, the tests already run the migrations, CI is green, a release is close, or someone said to merge" (one shared answer; all three covered).
- M2: hard rule on open/approve/merge plus excuse list and "A person telling you to ship does not run the check".
- M3: "applies to every migration, however small"; only exception is PRs that leave `migrations/` untouched.
- M4: "Do not open, approve or merge. Tell the user the PR is blocked until someone with access runs it".
- M5: I001 not mentioned in skill or replies.
- M6: "Use when a PR adds or edits a file under migrations/ and you are about to open, approve or merge it, including..." under 300, no step summary.
- M7: "It does not apply to PRs that leave `migrations/` untouched."
- M8: no scenarios written.
- M9: "I have not run an agent against it ... replay the #771, #798 and #812 prompts with and without the skill."
- M10: skills/migrate-check/SKILL.md, name matches, four sections in order.
- M11: 46-line skill, focused, no template filler.
- E1: reply "October rules were all prohibitions ... diary-style opening and the file tour stayed", cites #830, #841.
- E2: ordered What changed / What could break / Testing / Fixes with sizes, but step 3 keeps a "Leave out the route you took, alternatives..." list (reworded prohibitions).
- E3: reply names #834 key order and #841 setting; risk required, "Nothing found in the risk checks."
- E4: "unless complex" gone; "normally 10 to 15 lines".
- E5: Fixes last; "Dimas's `Fixes #` line is kept".
- E6: "Use when opening a pull request or updating its description after new commits."
- E7: reply "linked risk-checklist.md, file is risk-checks.md. I fixed the link."
- E8: only re-read the three samples against the layout; no fixed criteria, no old/new on same input; behaviour marked not verified.
- N1: staging line added to AGENTS.md; indentation and channel noted as already present.
- N2: one line for Request 3; short reply.
- Q1: replies 1 and 2 give files, check and not-verified; reply 3 is thin on how checked.
- Q2: "Agents treated every change as complex" stated as fact without evidence.

### B
- M1: excuse table rows for nullable column, tests run migrations, three hours of work, SNAPSHOT_URL unset, "user said merge it"; step 3 names "I'll run it tomorrow".
- M2: hard rule, excuse table, red flags.
- M3: no exemptions; only PRs that leave `migrations/` untouched.
- M4: step 3 "stop. Do not open, approve or merge ... tell the human ... run `make migrate-check` on the office network or the VPN".
- M5: not mentioned.
- M6: "Use when opening, approving or merging a pull request that adds or edits a file under migrations/, or when a task asks for a model change that needs a Django migration." (~170 chars)
- M7: "It does not apply to PRs that leave `migrations/` untouched."
- M8: none.
- M9: "I did not test it with live agents ... replay the #771, #798 and #812 prompts with and without the skill."
- M10: extra section between Procedure and Output; order correct. A prose paragraph precedes When to use.
- M11: 56 lines, table plus red flags; acceptable.
- E1: "All three samples came out long anyway ... every agent decided its change was complex"; Wulan #830 and diary complaint cited.
- E2: four-part template with one-line sizes; prohibitions removed.
- E3: reply notes only #834 key order buried; #841 not named; risk part required with "None found".
- E4: clause gone; reply names it.
- E5: "Dimas liked that, so it stays."
- E6: trigger-only "Use when opening a pull request or updating..."
- E7: named and fixed.
- E8: "hand-checked the shape against #830"; no prior criteria; not verified stated.
- N1: URL added; indentation and channel left; offers .editorconfig for other file types.
- N2: one line for Request 3.
- Q1: all three reply parts present.
- Q2: "every agent decided its change was complex" asserted.

### C
- M1: excuse table quotes the three excerpts verbatim ("a dry run isn't necessary", "Given the release deadline", "redundant", "I'll merge now and run the check tomorrow", "Bayu said to ship it tonight").
- M2: hard rule, "No exceptions" list, excuse table, stop signals.
- M3: no exemption; S6 sets the observable boundary.
- M4: exit 2: "Do not open, approve or merge. Leave the work on the branch and tell the user that someone on the office network or the VPN has to run it."
- M5: reply 1 "I001 ... already caught by make lint ... nothing was added"; routing table in test-scenarios.md.
- M6: "Use when you are about to open, approve or merge a pull request that adds or edits a file under migrations/, or when a task you are finishing changes the database schema." under 300.
- M7: "does not apply to PRs that touch no file under migrations/"; S6 scenario.
- M8: references/test-scenarios.md has six scenarios from the excerpts, some with several pressures (S3 time, authority, missing access), each with PASS/FAIL.
- M9: "NOT VERIFIED: no fresh agent ran any scenario"; runbook with and without skill; "after" rows labelled SELF-REVIEW.
- M10: correct layout and name; Excuses section between Procedure and Output.
- M11: skill focused; the 108-line scenarios file has a routing table and discovery probes, counted as the M8 deliverable, not filler.
- E1: reply and routing table cite Wulan (paragraph six), Bayu's diary, Background sections, and "The three samples got longer anyway".
- E2: four parts with sizes ("1 to 3 sentences", one line); prohibition list removed.
- E3: reply "#834 and #841 had no risk section at all ... key order ... environment setting. The slot now cannot be left empty"; "Nothing identified."
- E4: "the 'unless complex' clause removed".
- E5: "Dimas liked this, so I kept it"; S5 regression scenario.
- E6: "Use when you are about to open a pull request or rewrite its description after new commits."
- E7: named; reply marks the cause as "a guess".
- E8: test-scenarios.md written before the new SKILL.md; old samples scored FAIL, new #830 rewrite scored on the same criteria; labelled self-review; "NOT VERIFIED".
- N1: only AGENTS.md changed with the staging line; indentation (.editorconfig covers only *.py) and channel noted as already covered.
- N2: one line.
- Q1: all three replies complete.
- Q2: claims marked ("a guess", "my own scoring", "not agent output"); no invented mechanics found.

### D
- M1: table rows for nullable (#771), tests (#798), deadline, "can't reach the snapshot, I'll run it after merging" (#812), "user said to merge".
- M2: hard rule, excuse table, "Do not set SNAPSHOT_URL yourself, edit scripts/migrate_check.py, or substitute make test".
- M3: observable gate: "If no path starts with migrations/, stop".
- M4: "Do not open, approve or merge ... blocked until someone on the VPN ... runs it", gives branch and commit.
- M5: not mentioned.
- M6: "Use when a change adds or edits a file under migrations/, or when asked to open, approve or merge a pull request that does."
- M7: "does not apply to changes that leave migrations/ untouched".
- M8: none.
- M9: "couldn't run any agent with and without the skill ... replay the #812 prompt."
- M10: name migration-check-gate matches folder; sections in order, extra section between Procedure and Output.
- M11: focused; one-line retirement note.
- E1: "The October rules did not shorten anything, and #830, #834 and #841 all still open with a diary and a per-file list".
- E2: four parts with sizes (1-4 bullets, one line, 20 lines); prohibitions removed.
- E3: reply names #834 key order and #841 setting/retry with no risk heading; risk mandatory with "Nothing from the risk checks (<paths>)".
- E4: gone; replaced by "at most 20 lines".
- E5: "kept for Dimas".
- E6: trigger-only.
- E7: named and fixed.
- E8: "walked the three samples against the new steps by hand"; no criteria set before; not verified.
- N1: only the URL added; the other two left, with reasons.
- N2: one line.
- Q1: all three replies complete.
- Q2: claims match the diff; "likely" marked.

### E
- M1: table: nullable, tests on test DB, redundant/hours, release deadline, "SNAPSHOT_URL isn't set, I'll run it tomorrow", "owner said to merge".
- M2: hard rule plus table.
- M3: "Skip it only when the diff touches nothing under migrations/".
- M4: step 4 "stop. Do not open, approve or merge. Tell the person ... someone on the office network or VPN to run it".
- M5: not mentioned.
- M6: "Use when a change adds or edits a file under migrations/, and again before opening, approving or merging a pull request that contains one."
- M7: only "Skip it only when the diff touches nothing under migrations/".
- M8: none.
- M9: "I haven't tested this ... replaying the #771, #798 and #812 prompts with and without the skill."
- M10: layout correct, extra section between Procedure and Output.
- M11: focused.
- E1: "story of the investigation, a file-by-file list, a Background section ... risk in paragraph six ... under 8 lines had no effect".
- E2: ordered parts with sizes (1-3 sentences, one line), but a labelled "Leave out:" list stays and an optional fourth part sits before Fixes.
- E3: risk "always written ... even when the change looks safe"; reply mentions #834 only as something that "should now show up"; omissions not noticed, #841 not named.
- E4: "unless complex" removed and named; "one screen without scrolling".
- E5: "stays on the last line, as Dimas asked".
- E6: trigger-only.
- E7: named and fixed.
- E8: no criteria and no old/new comparison; only a suggested future check.
- N1: URL added; channel left; indentation added as prose ("Python uses 4-space indentation (make lint enforces it).").
- N2: two lines for Request 3.
- Q1: all three replies complete.
- Q2: "the exception covers nearly every PR" and "agents kept their usual layout" asserted without evidence.

## Judgement calls
- Criterion count: the rubric's own total (42 = 21 x 2) disagrees with its 23 rows; I scored 23 rows, max 46. Gate comparisons are unaffected.
- E2 (A, E): both keep a "Leave out" list next to the new shape. Read as reworded prohibitions gives 1; read as the shape doing the work gives 2. A and E would each gain one point.
- E3 (B, E): B names only #834; E names no omission. Crediting B's reply as noticing the pattern would give 2.
- E8 (A, B, D vs C): hand re-reads of the samples scored 1; a stricter reading is 0, which would drop A, B and D by one. E's lack of any check is 0.
- M7: all runs state the boundary only as "no file under migrations/". If the rubric wants a concrete near miss such as model or query changes, only C (S6 scenario) goes beyond it and the others could drop to 1.
- M5: unmentioned scores 1 for A, B, D, E; C scores 2.
- M11 (C): the 108-line scenarios file could be read as sprawl (1); I treated it as the M8 deliverable.
- M10 (B): a prose paragraph before "When to use" is not a section; scored 2.
- N1 (E): indentation added as a prose line scores 1 by the row, although the line says make lint enforces it.
- Q2: 1 where a causal claim about agent behaviour ("every agent decided it was complex", "treated every change as complex") is stated as fact. A lenient reading gives 2 to A, B and E.
- E4 (A, E): "normally 10 to 15 lines" and "one screen" are soft sizes but not complexity-based exemptions; scored 2.
