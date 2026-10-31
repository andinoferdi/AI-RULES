# Thin coordinator assessment, 2026-10-31

Runtime: `afc2f4496b2314559ef44828d35c33428dc766fd` on andino-workflow.
Baseline: `69e797e`; main baseline `62d07c7`.

The user accepted a thinner coordinator and ten execution/resource guards. This
change implements that direction; it does not claim to prove the sole cause of
earlier deficient plans. The earlier portable-planning contracts remain intact.

## Role and artifact boundaries

Andino selects capabilities, coordinates dependency/phase handoff, maintains shared
progress, applies resource/permission guards and aggregates acceptance evidence.
Selected native members, AI-RULES siblings and relevant installed external skills
own their full procedures, required resources, artifact detail and technical checks.
Tools supply their actual operations and controls, not methodology or authority.

Root entrypoint is reduced from 285 to 138 lines (including frontmatter); no
runtime token/latency savings are inferred from textual size. Domain/method
procedures remain in their guides. All 59 member GUIDE/SKILL ownership paragraphs
were aligned; substantive procedures/outputs/resources were preserved. Delegation
additionally clarifies that the three-worker cap is concurrent, so required
independent participants may run in waves. No nested spawning or shared-write race.

One authoritative progress source may link complete specs, implementation plans,
designs, reports or provider journals. LITE/checkpoint density and Focus govern
coordination/communication, not the required deliverable. Bulk source/log dumps
are distinguished from necessary change snippets and assertion fixtures.

The ten guards cover looping, context reuse, MCP/schema acquisition, reasoning,
tool ping-pong, transient retries, tool output, AI/artifact output, skill overlap
and agent proliferation. Tool/model/token controls remain host-conditional;
instructions do not pretend to unload injected schemas or enforce runtime budgets.

## Source and generator verification

- 79 existing/new dispatch, readiness, debugging order, boundary, unified and case
  tests pass against current runtime bytes. Structural tests are not model behavior.
- Source comparison checks 59 GUIDE/SKILL pairs against baseline, allowing only
  ownership paragraphs and reviewed delegation concurrency wording.
- The real maintainer generator runs with disposable audit/runtime copies. Its
  first test exposed deletion of brainstorming/workflow-advisor from the old
  57-method source audit; review then exposed regression of a current
  decision-interview readiness row. Both fixed. The test compares all 59 current
  trigger/exclusion pairs, not just counts or positive words. Parent also found
  ask-matt/brainstorming aliases absent from old metadata; current aliases now
  survive regeneration and the same test compares all current alias targets.
- Independent source review initially requested two fixes (current-row precedence
  and concurrency). Both resolved; scoped Spec PASS and Standards PASS. Reviewer
  independently reran four boundary/generator regressions.
- Complete package validator passes 7 packages, metadata/relative links and 7 eval
  schemas. Execution's drift/missing-identity fixture and old-algorithm mutation
  still pass. Exact published release bundle stages and validates.
- Nine installer/distribution/family/bundle/release tests pass, including nested/
  native planning/execution and both lifecycle references on all five hosts.

## Fresh consumer applications

The rubric was saved before outputs in
`docs/exec-plans/active/thin-workflow-coordinator.md`. Two fresh independent
contexts of the available model consumed the candidate snapshot without parent
oracles. Their actual inputs/outputs are preserved here.

Internal planning under LITE produced a complete plan with file/symbol changes,
code, assertion/fixture blocks, commands, exact schema/copy and a separate unready
provider consumer. Parent reviewed its task contracts; all 8 original input hashes
match and six Python blocks parse. No implementation was executed by the planner.

The explicit manually installed fixture provider read its two required resources
and produced the complete model plus all 12 ordered cases, with a short STATE link.
Parent compared exact JSON independently. All ten raw trace decisions match the
parent's independently defined oracle: evidence reuse, no repeated ping-pong,
denial/exhausted-retry stops, bounded query/schema, simple inline work, complete
artifact despite LITE, explicit external provider and changed-state recheck.

Observed process failures remain visible: both consumers initially read task/brief
material before selected-guide activation was fully ordered as required. The
internal consumer also first read RTK without its prefix. These are NOT compliant
entry-loader evidence. Required method/resources preceded artifact authoring;
artifact/authority checks pass. The source is not weakened to relabel the failures.

The consumed runtime hashes are in consumer-input-sha256.json. Final reviewed
concurrency clarification followed that snapshot; the actors did not establish
its live scheduling behavior. `verify_consumers.py` checks raw artifacts/decisions,
not live retries, MCP unloading, reasoning settings, future native loading or
universal cross-model performance. No controlled superiority claim is made.

## Reproduction and distribution

From main, use Python stdlib and the runtime directory/ref:

```text
python -m unittest tests.test_andino_thin_coordinator
python docs/validation/thin-coordinator/verify_consumers.py --root docs/validation/thin-coordinator
python docs/exec-plans/active/verify-execution.py --runtime <workflow-checkout>
```

Set ANDINO_RUNTIME_DIR for working-tree candidate checks, or ANDINO_RUNTIME_REF
for a committed ref. Test loader scripts support these explicitly. Runtime-only
docs contain no evaluation fixtures or transcripts.

Release sequence 26 pins the reviewed runtime. Source-installed local CLI was
refreshed. Scoped latest update applied 5 workflow updates and retained 10 current
dependencies, all 15 targets VERIFIED. Entire native/nested/root readback passed
1840 file comparisons on five hosts, with the saved profile byte-for-byte unchanged.
Readback is in installation-evidence.json; publication details are in the checkpoint.
Previously downloaded frozen installers are not rebuilt by changing this manifest;
their default latest-source setup path reads the published branch. File equality
does not establish future native host loading or skill use.
