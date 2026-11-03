# Brainstorming quality

Status: IN_PROGRESS  
Current phase: Execution and delivery

## Objective and acceptance

Improve observable interview and handoff quality while preserving path selection, decision dependencies, progressive resources, ADRs and glossary. Verify that `ai-rules setup` installs the revised member before delivering to `origin/andino-workflow`.

## Execution board

| Phase | Status | Evidence or exit condition |
| --- | --- | --- |
| Source review | DONE | Canonical checkout clean on `andino-workflow`. Read the four upstream SKILL.md files via GitHub raw. No user transcript exists. |
| Baseline | DONE | Approved read-only Luna/low run. A agreed to start and asked two questions. B cited repo facts but made no recommendation. C agreed to start despite an unresolved sharing policy. |
| Design and planning | DONE | Tasks below are ready under the existing execution authorization. |
| Execution and delivery | IN_PROGRESS | Revised all four member files. `git diff --check`, operational fixture in both modes, local links, and path/contract assertions passed. |

## Decision and evidence

The current procedure and grilling protocol treat a short answer as fatigue and permit a subjective predictability score to end the interview. The parent output contract lists all three artifacts without distinguishing spike and bounded paths. Evaluate these as hypotheses, alongside grounded recommendations and decision playback. Preserve the default one-question cadence and compare output by scenario rather than counting process steps.

## NEXT ACTION

Publish the verified source on `origin/andino-workflow` and verify setup from latest. No council panel was needed for this bounded change. Revised-model behavior remains unverified by a fresh evaluator.

## Ready tasks

**T1 | Interview and handoff contract.** In `skills/brainstorming/SKILL.md`, replace numeric intent and exit thresholds with repo-grounded playback, one material question and a reasoned, revisable proposal. Preserve Spike, Bounded and Architectural. Replace the fatigue cutoff with synthesis after three same-branch questions or a user request to accelerate. Treat an unambiguous short answer as resolution of its node. Close only with material decisions resolved and design confirmation. Split output by path and preserve accepted ADR/glossary capture. Synchronize `resources/grilling-protocol.md`, replace the existing contradictory executable fixture with a state-based fixture, and revise `resources/worked-example.md` to exercise concise assent and a dependent question. In `resources/adr-and-glossary-template.md`, align persistence with design confirmation and conditional artifacts.

**T2 | Verify and distribute, depends on T1.** Run `git diff --check`, execute the embedded fixture in positive and negative modes, check Markdown targets and walk the three scenario contracts. A should ask one outcome question without agreeing to build. B should use the supplied access facts and make a revisable recommendation. C should accept `Ya` for the role decision, withhold implementation and ask about sharing before expiry. A fresh revised-model comparison is a separate evaluation from these checks. Commit and push the canonical branch, then run `ai-rules setup --host codex --capability andino-workflow --scope project --project-root <temporary-directory> --state-dir <temporary-state> --source latest --yes --non-interactive` and compare installed member files against the pushed source.
