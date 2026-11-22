# Constraint-driven development skill quality

- Base: `8ecb8108b3d721fb2c584ff389afe348b519f228`
- Branch: `andino-workflow`
- Execution base: `88c4928d93068a2b727c77b67af08669c643c9c3`; intervening commits did not touch the target.
- State: DONE
- Phase: Delivery verified

## Objective and acceptance

Improve the quality of the generated constraint contract and gate decisions against the Addy Osmani reference while preserving the Andino layout, offline resources, floor guard, redaction, and governance. Compare unguided, current, upstream, and revised behavior under matched pressure. Run applicable repository checks and verify that public setup installs the reviewed bytes.

## Findings and proposed direction

- Upstream gives the agent a sequential recipe for producing and wiring a runnable contract. The Andino entrypoint leads with prohibitions and an offline synthetic check. Its fuller recipe is spread across the guide and worked example.
- Candidate change: put the decision sequence and output contract on the execution path. Cover contract reuse, floor-only startup, unavailable baselines and checks, comparable measurements, and gate placement. Keep long tooling details in the existing resources. Let the baseline determine which additions earn space.
- The local and remote branch tips matched at the base above. Existing deprecation-and-migration edits and their active plan are unrelated.
- The installer capability catalog names the `andino-workflow` branch. Prior setup evidence uses `--source latest`. Confirm the default public source separately before deciding whether a release is required.

## Execution board

| Task | State | Acceptance |
| --- | --- | --- |
| Observe unguided baseline | DONE | Five fresh contexts on gpt-6.1-sol/low. All retain the baseline and reject partial coverage; zero wire a diff floor guard. |
| Compare and specify changes | DONE | Current and upstream samples both wire the floor. Upstream gives concrete negative gate probes; current omits them. Neither sample separates pending checks as an explicit artifact section. |
| Implement and verify | DONE | Both embedded examples and six floor-guard probes passed; five revised samples produced a pending section and negative gate probes. |
| Publish and verify setup | DONE | Workflow and manifest pushed; default setup and staged bundle matched Git blob bytes. |

## Evaluation fixture

Use a legacy Python API with a clean base, 52% existing coverage, no quality contract, a 5-second edit budget, a scanner available only in CI, and a failing check. The deadline creates pressure to skip the test or loosen a threshold. Ask for the actual contract and gate wiring. Score whether the output holds the measured bar, specifies runnable checks and cadence, distinguishes missing evidence from success, protects the floor, and records an authorized exception without changing the global rule. Use the same prompt and scoring across conditions.

## Change specification

- In `skills/constraint-driven-development/SKILL.md`, replace the rationalization and red-flag sections with an ordered `Procedure`, `Permissions and safety`, and `Verification`. Use the table columns `ID | Rule | Checked by | Runs at`, a measured-only section and an exceptions section. Load existing policy and inspect CI first. Pin the comparison base and measurement configuration, allow floor-only onboarding, wire the floor to local fast/task and required CI, and require clean, known-bad and unavailable probes. Preserve intake, floor, resource links, offline example and MIT notice.
- In `GUIDE.md`, align the external-check requirement, ratchet and exception descriptions with the procedure. A floor-only bootstrap can precede production readiness; the ratchet uses comparable passing runs; diff heuristics cannot authorize exceptions.
- Verification from workflow: run both SKILL.md example branches and exercise the actual Python and Node floor guards against temporary Git repositories. From main run `python scripts/validate_skills.py --andino-ref <reviewed-ref>`. Compare independent revised outputs. Run the installed CLI with isolated project scope and its default source. Default source is latest; update the main bundled manifest to the reviewed workflow commit as a separate delivery step.

## Result and evidence

- Workflow commit `6ec3d5a74315e3917bf8d5be910aef6c14a9240d` and main commit `2f25eb31893e63c4e7f7d6595c605e5a1926cadd` confirmed at their remote refs.
- Two SKILL.md example variants and Python/Node floor guard clean, untracked skip, and missing-base fixtures passed. Guard reference implementations are unchanged. These probes do not prove coverage of all Git states or semantic evasion.
- Focused Andino package plus eval schema validation passed. The combined validator returned 1 for the unrelated Search First runtime file `references/consolidation-provenance.json`.
- The installed Windows CLI used default-source project setup for Codex. Three targets installed with no failures or blocks. Both standalone and nested SKILL.md and GUIDE.md matched the committed Git blobs. Initial hashing against the CRLF worktree failed; raw Git blob hashes matched all four installed files.
- Release manifest sequence 31. Stage-only build exported eight bundles. The two staged constraint skill documents matched the committed bytes. The public default path reads the workflow branch, so an additional binary release was unnecessary for availability.
- Evidence is one simulated scenario: five unguided, one previous Andino, one upstream, and five revised samples, all gpt-6.1-sol/low. Five revised samples specify a diff guard, pending measurements, and deliberate failure/unavailability probes. Some stage scripts rely on repository-specific guard adaptation and did not enforce the time budget in code. This is output-quality evidence, not an executed production CI gate or a broad superiority benchmark.
- Structured self-review covered spec and standards for the two documents and manifest. Separate isolated agents evaluated behavior. No council was run.

## NEXT ACTION

None. Default public setup and bundled source staging verified.
