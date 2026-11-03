# Verification quality

Status: IN_PROGRESS | Phase: execution

## Decision

Superpowers puts a short gate immediately before a success claim. The existing
Andino Procedure covers evidence identity, selective reuse, isolated regression
checks, and permissions, but leaves the final claim decision implicit. Keep
those safeguards and make the decision explicit in both native entry points.
Use the existing runnable regression fixture and compare the three contracts
against the same cases. A structured self-review can assess contract coverage;
it cannot measure model compliance. No council or subagents for this coupled edit.

## Ready tasks

1. **Skill contract** — In `skills/verification/{SKILL,GUIDE}.md`, replace
   Procedure with a pre-claim gate: select proof, check currency, run complete
   checks for missing/stale evidence, inspect outcomes, and report only the
   supported scope. Extend the native trigger to authorized delivery and task
   handoff. Retain existing sections, example, and permission boundaries.
   In `skills/verification/resources/contract.md`, add the claim-to-proof
   matrix and result states. Required cases: changed tested bytes → rerun;
   unaffected matching identity → reuse; empty/skipped → not verified; failed
   → report failure; worker claim → inspect diff and verify integration.
2. **Review and publish** — After task 1, inspect the owned diff, check entry
   point procedure parity, run the embedded good/bad/good regression example
   with Python unittest in a temporary directory, and run `git diff --check`.
   Commit only this ticket and push to `origin/andino-workflow`.
3. **Install and verify** — After task 2, run
   `ai-rules setup --host codex --scope global --capability andino-workflow --source latest --yes --non-interactive`.
   Compare installed native and nested skill files with the reviewed source.

## Result / Evidence

Contract review: both entry points share the same gate. The prior contract
already rejects stale, empty, skipped, and worker-only evidence. The upstream
gate makes claim timing and the report decision explicit. The revised
contract combines those properties and states when unchanged evidence can
be reused. Spec and standards self-review found no material gap in the
edited contract. No independent model behavior baseline has been run.

Local checks: `git diff --check` passed in the workflow checkout. The
embedded fixture ran in a disposable directory via `python -B -m unittest -v`
against the good, faulty, then restored implementation. Each run exercised
one test, with exits 0, 1, 0 and the expected `16 != 15` assertion.

NEXT ACTION: Publish the reviewed paths and verify the global Codex install.
