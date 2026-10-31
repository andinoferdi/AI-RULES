# Planning portability assessment (2026-10-31)

Reviewed runtime: `69e797e112ce6c2a48d3e767d0c2c7eb4c7f5ff3` on
`andino-workflow`. Quality-plane changes live on `main`.

## Decision and evidence

Five independent Council lenses and two author-anonymous peer reviews supported
strengthening the existing skill rather than copying an entire upstream workflow.
The original user examples are different applications at different phases, with
accumulated execution history; they demonstrate output shape, not a causal model
benchmark. The current baseline already required paths/interfaces/assertions.
Remaining gaps were generic implementation steps, optional worked examples,
ambiguous wording against code in plans and no shared specification-readiness gate.

The implementation requires task-local Change Specifications: inspected anchor,
operation, exact names/values, decisive code/text, assertion/fixture code and proof.
Readiness is separate from progress. Roadmaps retain bounded unknowns; discovery
must fill dependent contracts before execution. Template, lifecycle and execution
preflight share the same boundary. Code in the plan is permitted; application
source is not edited by a planning-only request.

Source comparison: [Superpowers writing-plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md)
was read on 2026-10-31 as reference data. Its automatic worker/commit/approval
instructions were not imported. Existing MIT provenance remains in the runtime.

## Preregistered consumer assessment

The rubric was recorded before inspecting planner outputs in
`docs/exec-plans/active/planning-portable-detail.md`: zero unresolved consequential
choices in ready tasks; concrete edits/assertions; independent behavior/design
checks; exact static copy; honest discovery; stale-snippet rejection.

Two isolated planners received the same fixture and accepted request, one with
baseline planning at `fc8f21b`, one with the candidate. Two other contexts then
implemented only the saved plan and reachable repository requirements. They did
not receive each other's outputs, the parent's oracle or planner conversation.
These are separate contexts of the same available model, not different providers.

| Observation | Baseline | Candidate |
| --- | --- | --- |
| Application files unchanged by planning | All 8 baseline hashes match | All 8 baseline hashes match |
| Material missing decisions reported before implementation | 0 | 0 |
| Task-local production/test code blocks | Detailed prose, no implementation/assertion blocks | Explicit parser/rendering/schema/copy changes and assertion blocks |
| Executor's final local tests | 12 PASS | 11 PASS |
| Parent's independent oracle | 15 PASS | 15 PASS |
| Provider contract | Unknown; consumer blocked | Unknown; consumer blocked |

The oracle checks CLI JSON/CSV outputs (quotes, commas, multiline title, row order,
empty results and invalid choices), exact schema/copy, public signatures and stdlib
imports/dependency manifests. It does not score matching implementation tokens.
Both behaviors pass: no behavioral superiority is established on this pair. The
candidate demonstrates the requested concrete code/artifact output. Routine
mechanics can differ, such as CSV quoting policy, without changing acceptance.

The candidate plan was preserved before execution (`candidate-plan.md`). Baseline
snapshot instruction arrived after its first status update, so only its final
plan and execution record are preserved; no original was reconstructed. Parent
read both original plans before scoring and did not repair them for the executors.
Artifact hashes are in `artifact-identities.json`. Raw evidence is adjacent.

A third independent preflight received a precise but invalid plan. It detected a
nonexistent `render_rows` anchor, out-of-scope `args`, deletion of an existing
schema state and incomplete tests/discovery; it kept the exact README task ready.
All 8 baseline hashes remained unchanged. See `stale-preflight.md`.

Fixture limitation: the accepted README text intentionally preserves a legacy
command without the positional source. It tests exact authorized copy, not command
usability. Runtime smoke commands supply the source. This is not a recommendation
to publish an incomplete quickstart.

## Reproduction and scope of checks

Run from the main quality-plane checkout (Python 3.11+, stdlib):

```text
python docs/validation/planning-portability/fixture.py prepare <new-directory>
python docs/validation/planning-portability/fixture.py verify <implemented-directory>
python docs/validation/planning-portability/check_example.py --runtime <workflow-checkout>
python docs/exec-plans/active/verify-execution.py --runtime <workflow-checkout>
```

Keep fixture.py/oracle outside the directories exposed to future consumers.
Preparation requires a new directory and never removes existing work. Example
checking executes the literal documentation blocks together: 3 then 6 tests pass.
Execution's drift/missing-identity mutation and complete package validation pass:
7 packages, metadata/relative links and 7 evaluation schemas. These deterministic
checks are separate from the observed fresh-context consumer applications.

## Distribution

The prior runtime HEAD carried three maintainer evidence files rejected by the
package validator. They are relocated to the same paths on main, with the two
Markdown histories preserved and the verifier made portable via --runtime.
Runtime now validates as a complete package, without excluding files to hide errors.

The existing planning distribution test was extended to compare both changed root
lifecycle references as well as all nested/native planning resources on five hosts.
The expected-runtime override first failed against old manifest pin `b223761`.
Release sequence 25 pins the reviewed runtime. After the pin update, the combined
planning/execution/family/bundle/release suite passes 9 tests, including both
five-host distribution cases. Exact workflow bundle staging also passes validation.

The local CLI was refreshed from main using `pip install --no-deps
--no-build-isolation .`; its installed manifest pins sequence 25. Scoped latest
update applied five workflow updates and kept ten dependencies current. All 15
lock targets are VERIFIED. `verify_installation.py` read back 90 native/nested/
lifecycle files against the runtime ref on five hosts and checked the entire saved
profile against its pre-update value (8 capabilities, 5 hosts). Machine-readable
readback is in `installation-evidence.json`. Installer backups are retained.

Local installation/publication details are recorded in the durable execution plan.
An old frozen executable's bundled payload is immutable until a separately built
release; default setup's latest-source path obtains the published branch. No claim
is made that installed files prove native loading or use in a future session.

Independent source review: Spec PASS, Standards PASS. Reviewer's additional
signature/dependency-oracle and root-reference distribution gaps were resolved.
This is a bounded qualitative assessment, not proof that every model will emit
the same program or outperform Superpowers on every project.
