# Debugging Guide

Internal Andino resource. Operates under Andino Workflow governance. The
[member entrypoint](SKILL.md) defines the phase gates and completion criteria.

## Establish a usable signal

Read the first meaningful error and compare the failing environment with a working
one using the same input. Check recent code, configuration and dependency changes.
Read relevant module contracts and local architecture decisions when present.
An import, login or fixture error may prevent the target path from running.
Resolve that prerequisite or record the gap before interpreting the result.

Choose the cheapest [feedback loop](resources/triage-and-feedback-catalog.md)
that reaches the defect. Capture the command, prerequisites, expected and actual
result and elapsed time. Retain a slow exact loop while developing a faster probe.
For flaky cases record failures over attempts under fixed inputs, seed and load.
For performance compare repeated measurements on the same workload and
environment. State the metric and meaningful regression threshold first, then use
a profile, query plan or known-good revision to isolate the cost.

When reproduction requires a human action, use the catalog's HITL driver to
capture a structured signal. When no exact signal can be obtained, report the
attempted loops and ask for the smallest useful input, such as a redacted trace
or access to the failing environment. Mark cause and fix as unverified.

## Isolate the first divergence

Preserve the original trigger. Remove inputs, callers or dependencies one at a
time and check that the minimized loop still shows the same defect. For intermittent
failures compare rates before and after cuts. Stop minimizing when further cuts
change the failure or cost more than they would clarify.

Use [backward tracing](resources/root-cause-investigation.md) to find the first
violated invariant. Compare failing and working paths across each relevant
boundary. Record each plausible cause with the evidence for it, the expected
observation if true and a result that would refute it. Share the ranked shortlist
when domain context could change the next probe and continue within authorization.

Prefer existing telemetry, a debugger or a read-only comparison. Use one tagged
probe when existing evidence cannot distinguish the causes. Record what happened
and update the shortlist. Remove the probe before trying another. When probes
stop producing new evidence, change the observation point or report the missing
signal. For test pollution and timing use
[flaky and concurrency debugging](resources/flaky-and-concurrency-debugging.md).

## Fix, recover and report

Use the original trigger or a faithful automated harness when no narrower test
seam represents the defect. Document the gap if the regression cannot be retained
and leave any unverified acceptance explicit. A mitigation for an unavailable
dependency can have its own verification and status. Keep the defect open until
its cause and resolution are verified.

After a failed fix, compare the diff against the pre-attempt baseline. Restore
only identified attempt-owned changes and return to the evidence. After three
failed fixes, halt autonomous mutations and follow
[defense and recovery](resources/defense-and-recovery.md). Preserve uncertain
or overlapping edits. Disproved hypotheses update the investigation and are
tracked separately from attempted fixes.

Use the [worked example](resources/worked-example.md) to see the difference between
a symptom assertion and a test that reaches the shared seam. Record the supported
cause or remaining uncertainty, the discriminating evidence, the original trigger
result, regression and affected checks, plus cleanup and any remaining gaps.

## Provenance

See [upstream sources and MIT notices](references/license.md).
