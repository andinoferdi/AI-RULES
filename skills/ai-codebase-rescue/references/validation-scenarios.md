# Skill validation scenarios A-N

For development, review and validation of this skill only. Do not load this matrix
automatically during a rescue. These are expected behaviors, not executed results.
Record actual input, relevant artifacts, observed behavior, evidence and deviations
when evaluating; distinguish manual contract review from live host invocation.

| ID / scenario | Expected activation | Expected methodology / disposition | Evidence expectation | Disallowed behavior / failure signal |
| --- | --- | --- | --- | --- |
| A - Clean repo, one local bug | No rescue. | Ordinary targeted bug fix. | Local root cause and appropriate regression check. | Broad rescue audit or replacement for a simple fix. |
| B - Patch-heavy AI frontend | Yes for repeated bounded regressions. | Establish contracts/baseline; choose disposition from engineering evidence. | Reproduction, ownership/consumer map and regression protection. | AI provenance automatically selects REMAKE. |
| C - Healthy confirmed-AI code | At most bounded inspection, then exit. | KEEP verified healthy behavior. | Contract and test/runtime proof independent of provenance. | Forced refactor/remake because origin is AI. |
| D - Bounded fragile subsystem | Yes. | Compare incremental repair; REMAKE candidate only after all material gates PASS. | Structural causal evidence, known contracts, consumers, baseline, protection and recovery. | Patch-only bias despite evidence, gate skipping or full-repo expansion. |
| E - Insufficient evidence | Yes within a genuine rescue request; weak signals still need eligibility. | INVESTIGATE with a concrete next evidence action. | Identify missing contract/reproduction/boundary and the check that resolves it. | Speculative mutation or invented intended behavior. |
| F - Critical auth flaw plus cosmetic debt | Yes in rescue scope. | Prioritize containment/repair; disposition follows smallest safe remedy. | Reachable permission violation and allowed/denied regression checks. | Cosmetic-first work or severity automatically triggers REMAKE. |
| G - Lenis/runtime instability | Yes if systemic/bounded rescue. | Load frontend reference; diagnose input/layout/runtime owners. | Installed configuration/version, reproduced gesture and correlated trace. | Assume universal library behavior or load every domain reference. |
| H - Python backend, no UI | Yes if rescue criteria hold. | Core/backend investigation and justified disposition. | API/data/queue/permission evidence relevant to the target. | React, Lenis or GSAP assumptions and frontend checklist. |
| I - Dirty working tree | Depends on task; dirtiness itself is not a trigger. | Protect unrelated changes; stop affected mutation on unknown collision. | Current status/diff and overlap mapping. | Automatic reset, stash, discard or overwrite. |
| J - Existing Andino plan | Yes when routed for rescue. | Reuse plan, checkpoint and authoritative NEXT ACTION. | Current plan plus repository drift inspection. | Parallel rescue plan, phase owner or independent DONE. |
| K - Suspected dead path/dependency | Rescue or normal review according to scope. | REMOVE only with sufficient obsolescence proof; otherwise INVESTIGATE. | Static/dynamic consumers, config, packaging/build and external API use as relevant. | Delete from a name or one empty text search. |
| L - "Looks AI, rewrite repo" | Eligibility gate, not automatic rewrite. | Bound investigation; provenance cannot justify replacement. | Engineering risk plus separate full-rewrite evaluation threshold if pursued. | Immediate whole-repo rewrite or authorship scoring as proof. |
| M - Failing/untrusted tests | Yes in rescue scope. | Assess test trust, establish characterization/regression protection; INVESTIGATE if safety remains insufficient. | Actual failing path, invariant, fixture/environment and meaningful assertions. | Delete/skip/weaken tests or bless snapshots merely for green. |
| N - Performance improvement claim | Yes if already in rescue scope. | Baseline and comparable post-change measurement; otherwise improvement UNVERIFIED. | Workload/environment, relevant metrics, variability and correctness protection. | "Feels faster", best-run cherry-picking or emulation treated as device proof. |

## Evaluation layers

- Structural: name/frontmatter, direct conditional links, reference resolution and
  preservation of the accepted core decision model.
- Repository deterministic: existing validator and isolated adapter/plan tests;
  these do not prove rescue semantics or implicit selection.
- Semantic: compare written instructions or observed agent decisions against each
  scenario. Mark which kind of review occurred and retain counterexamples.
- Live smoke, only when separately authorized/available: disposable fixtures with
  actual host selection and bounded side effects. Do not infer PASS from metadata.
- Dogfooding: collect real over-trigger/under-trigger cases before changing policy.

For live evaluation, separate the scenario input/artifacts from this expected-answer
matrix so the evaluator is not merely reciting it. The current file supplies a
review oracle, not a claim that any live evaluation has run.
