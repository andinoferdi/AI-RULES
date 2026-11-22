# Regression protection and verification

Use when establishing a rescue baseline, protecting a remediation contract or
substantiating an outcome claim. Match proof to risk and the affected integrations.

## Baseline before mutation

Record target revision and dirty state, relevant runtime/configuration, input or
fixture, command/manual procedure, expected invariant and actual observation.
Separate existing failures from missing checks. Reproduce intermittency with
bounded repeated trials and recorded conditions, not unlimited retries until green.
Use safe test data and the project's native tools; avoid live destructive probes.

Inspect whether the test actually reaches the affected path, has meaningful
assertions, uses representative data and models failure/permission boundaries.
Check stale snapshots, over-mocked dependencies, disabled assertions and flaky
environmental assumptions where they could invalidate the proposed proof.

Characterization captures behavior, not its correctness. Compare observed behavior
with requirements and consumer contracts; preserve verified behavior and explicitly
mark the defect that should change. If no trusted suite exists, establish a small
meaningful fixture, integration check or repeatable manual procedure. High-risk
replacement without adequate protection remains INVESTIGATE.

## Tie each claim to evidence

| Claim or risk | Appropriate protection and post-change comparison |
| --- | --- |
| Local correctness fix | A failing example tied to the invariant, then passing corrected behavior plus nearby edge cases. |
| Public contract preserved | Consumer/contract checks for input, output, errors and relevant side effects. |
| Permission boundary repaired | Authorized and unauthorized identities/resources, including direct access and failure cases. |
| Data/retry/concurrency correctness | Fixture-backed state comparison, duplicate/reordered requests and partial failure where relevant. |
| Bounded replacement | Critical behavior characterization plus integration/cutover checks; repeat after obsolete-path cleanup. |
| UI stability | Reproduce the interaction in an actual browser; inspect visual/runtime outcome and shared primitives. Compilation alone cannot prove it. |
| Performance improvement | Comparable workload and environment, before/after measurements and preserved correctness. |

Use targeted checks first, then broaden according to actual consumers and blast
radius. Run project-required checks. Do not repeat unchanged full suites without
new evidence or changes that warrant them.

## Performance comparison

Define the metric and acceptable outcome before editing: latency distribution,
throughput, memory, frame duration, dropped frames or another relevant measure.
Record hardware/browser/runtime, data volume, workload, cache/warmup conditions,
sample count and instrumentation overhead. Compare equivalent conditions and report
variation and tradeoffs, not just a best run or average that hides tail failures.

For animations, consider the target device's refresh rate and frame budget; 60 Hz
is about 16.7 ms per frame, not a universal threshold for every device. A desktop
CPU-throttled trace does not reproduce a mobile GPU. For APIs, distinguish service
work from network/client effects. If comparable baseline evidence is unavailable,
report current measurements and label improvement UNVERIFIED.

## Manual and unavailable checks

A manual check needs environment, starting state, exact interaction/input, expected
result, actual result and an inspectable artifact when useful. Record limitations
such as emulation instead of a physical device. A screenshot may show appearance
but cannot alone prove absence of intermittent flicker or a memory leak.

Use PASS only for an executed check meeting its criterion; FAIL for an executed
check that does not. Use UNVERIFIED for unavailable or unexecuted checks and name
the blocker plus the next feasible verification action. Mixed results stay mixed.
Do not infer full acceptance from a subset of green checks.

Never delete, skip or weaken tests, loosen thresholds, fabricate fixtures/results
or bless snapshots merely to obtain PASS. Repair a demonstrably incorrect test only
against a verified contract, recording its reason and replacement protection.
Return commands/procedures, actual outcomes, before/after comparison, residual
failures and limits to the active task. When Andino is active, it owns acceptance
and the authoritative checkpoint; otherwise use the host's normal task context.
