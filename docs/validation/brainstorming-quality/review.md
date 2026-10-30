# Brainstorming revision: 2026-10-30

## Decision and scope

Revise OpenCode's 5706e05 rather than retain it unchanged or replace the Andino
integration. Runtime commit: 91d1f186700cf5945e638504ad49f030cc993c9d.
User reported shallow questioning/exploration, premature convergence and immature
designs, delegated the solution, and authorized commit/push plus setup integration.

Comparison source actually read: [current Superpowers brainstorming](https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md),
2026-10-30. The GitHub tree page fetch failed; raw source succeeded. This comparison
does not replace the historical audited source pin or import upstream runtime code.

## Assessment of the OpenCode revision

The revision improved the explicit structure: local grounding, adaptive pacing,
separate approaches, design contents and builder check. Its worked example still
converged after one answer and offered direct Postgres despite a stated DB-downtime
invariant. It treated existing Redis pub/sub as support for durable buffering and
asserted latency, scale and reliability without evidence. These are observable
instruction/example defects, not measured rates of future model failure.

Its universal approval requirements contradicted delegated decisions in routing,
decision-interview and specification. Availability alone triggered subagent review,
contrary to delegation's benefit/authority conditions. A minimum 5/6 rubric could
pass while an essential criterion failed. Missing-requirement discovery also blurred
the distinction between brainstorming and decision-interview.

The new procedure preserves the useful structure and replaces those defects with
decision-changing questions, constraint-screened alternatives, reversal evidence,
readiness based on material unknowns, substantive design contents, conditional
review and persistent delegation. The example now changes direction after new
evidence. Both SKILL and GUIDE carry the same procedure and local resource.

## Council execution

Five isolated, read-only advisors used the same neutral brief; only their lenses
differed. Host capacity required batches of at most three concurrent direct workers.
No nested agents. gpt-6.1-sol/high: Contrarian and First Principles;
gpt-6.1-sol/medium: Expansionist, Outsider and Executor. These are independent
subagents, not five model providers. Summaries below are not verbatim transcripts.

| Lens | Judgment and distinctive contribution |
| --- | --- |
| Contrarian | Targeted revision; more ceremony can lengthen a shallow conversation. Reject options that violate invariants; include nonsoftware cases. |
| First Principles | Targeted revision; uncertainty reduction is the objective. Questions need consequences, and design claims need evidence. |
| Expansionist | Targeted revision; probe incidents, stakeholder tensions, failed alternatives and discriminating experiments. Show evidence reversing the recommendation. |
| Outsider | Targeted revision; respect delegated users and a builder's need for failure behavior and observable acceptance. Document volume is not maturity. |
| Executor | Targeted revision; synchronize procedure/resource/installable copies and verify real setup output, not only metadata. |

Two independent peer reviewers received the same shuffled A-E summaries without
author identities. One selected response C for concrete counterevidence and
proportionality; the other selected B for actionable workflow/integration checks.
They agreed the missing emphasis was a stopping rule and a question-selection rule:
another question must plausibly change scope, direction, acceptance or risk treatment.
Models: gpt-6.1-sol/medium and high respectively.

Chair synthesis: retain the foundation; strengthen contextual discovery and evidence,
not turn counts. Material disagreement concerned emphasis (discovery depth versus
execution friction), not the recommended option. Adaptive criteria need concrete
examples and behavioral observations because they are harder to audit mechanically.
First action was to rewrite the premature-convergence example and align its procedure.

## Consumer application observations

These were actual isolated subagent applications, not keyword scoring. Actors had
the candidate method and raw scenario, with no expected-answer rubric. No actor
edited files or contacted anyone. They were not full native-host or upstream trials.

### Baseline: delegated, already-grounded webhook design

An isolated gpt-6.1-sol/medium actor loaded the OpenCode version before edits.
Input supplied vendor non-2xx retries for 24 hours, unique event_id, ack after
commit, a ten-minute outage, passing burst test, no new infrastructure, and explicit
delegation to choose and proceed without approval. It selected direct PostgreSQL,
covered commit/response loss, duplicates and DB failure, and did not ask again.
Thus this baseline case PASSED despite contradictory text; it is not evidence of
behavioral improvement on that case. No no-guidance control was run.

### Candidate: open nonsoftware goal, four-turn conversation

Fresh gpt-6.1-sol/medium actor loaded the candidate. Raw first request: help elderly
neighbors, perhaps build an app, no selected direction. It asked for a concrete
incident. The next supplied answer described a missed medical visit, working family,
and some residents without smartphones. The actor asked how help was sought rather
than choosing an app. Next supplied facts: calls failed on the morning; RT can take
phone calls; two volunteers need a day's notice; voluntary small trial; no health
data. Actor compared RT coordination and a volunteer rota, recommended RT coordination,
named coordination-load/conflict conditions for changing direction, and left choice
to the user. After user chose RT and requested a draft for review, actor drafted
intake/confirmation, unavailable-driver and cancellation handling, minimal information,
and evaluation. It contacted nobody and did not implement an app.

Reviewer observation: useful progression and failure handling. Minor limitation:
one-week duration was stated as settled even though only the start week was supplied;
the 18:00 deadline and deletion policy were correctly labeled proposals. Existing
guidance requires marking agent defaults, but this observation shows compliance is
not guaranteed. Do not report every aspect of the output as perfect.

### Candidate: incomplete consequential design with forbidden delegation

Fresh gpt-6.1-sol/high actor received a proposed HMAC -> existing Redis -> immediate
200 -> Postgres worker design, no acknowledged-event loss requirement, unknown Redis
durability/full-queue/recovery behavior, and no project tools or subagents. It refused
readiness, separated acknowledgment durability, worker recovery, idempotence and
overflow, and said checks were needed rather than claiming they ran. Its question
asked whether non-2xx/retry was permissible, which changes overflow design. No workers
or project investigation were used; guide loading was the only permitted file read.

These applications used the draft before the final textual clarification that
worker limits mean at most three concurrent direct children. That clarification
does not change the observed questioning or durability behavior. Final source
identities are recorded separately by procedural/distribution checks.

## Verification and limits

- Package validation: PASS for seven packages, metadata, local links and eval schemas
  against a disposable snapshot of tracked runtime files. Direct directory validation
  initially included pre-existing untracked binaries; those diagnostic failures were
  avoided by selecting the actual package scope, without deleting user work.
- Procedural checks: two methods, five extended policies, seven killed mutations.
  Added explicit delegated and reopened-spec cases to the existing checker.
- Installer regression initially FAILED because old manifest commit 46b3bc3 lacked
  the worked-example resource. Updating the runtime pin is therefore required.
- After pin update, the installer regression PASSED across Codex, Claude Code,
  OpenCode, Antigravity CLI and IDE project paths. It compares all three files with
  Git source bytes in both nested workflow and direct member locations and resolves
  their local Markdown links. This proves distribution, not native agent discovery.
- Separate content/diff review found no material Spec or Standards blockers. Parent
  added explicit local worker cap and exercised delegated routing as suggested.

- Frozen release staging PASSED for all eight bundles, including the exact three
  brainstorming source files. Hashes are in publication-lineage.json; staging
  used build_release.py --stage-only and built no new executable.
- Real remote default setup PASSED fresh/repeat and old-official upgrade/backup/repeat
  with no catalog, source or network override. See published-setup.json. Other
  capability pins and the actual global skill installation were untouched.
- First full suite: 350 tests, 12 failures, one opt-in skip. Eleven failing subcases
  came from Search First tests expecting only three installed folders despite the
  existing 59-member family; the other expected index GUIDE links and forbade native
  member SKILL files, contradicting the accepted family contract. Updated those
  assertions to require exactly the 59 source-declared members plus dependencies,
  and to require each canonical guide plus correctly named native entrypoint.
  No skips, thresholds or production behavior were weakened. Focused recheck PASSED.
  Complete rerun PASSED: 350 tests, no failures/errors, one existing opt-in candidate
  test skipped, 306.078 seconds on Windows Python 3.12. See full-suite.json.

No statistical quality ranking, upstream head-to-head benchmark,
autonomous cross-host routing, or new standalone installer release is claimed.
Default setup uses latest remote source; the frozen manifest now also names this
runtime for source-mode bundled setup and subsequent executable builds. Previously
released offline executables keep their embedded snapshots.
