# Refine one dependency-aware implementation plan — supporting contract

## Task contract

One existing plan/checkpoint records the objective and accepted outcomes, relevant spec and decisions, current system constraints, affected boundaries, dependencies, ownership, integration or approval gates, and one `NEXT ACTION`. For each task record: id and user outcome; exact owned paths; consumers/producers with verified signatures and source pointers where available; dependencies; a concrete acceptance example; verification command and expected result; relevant failure conditions; current state and evidence. Producer and consumer names/types must match. If a path, signature or command cannot be verified yet, mark it `UNKNOWN` or provisional and block only the dependent task until inspection resolves it. Replace vague "edge cases" with a specific input and outcome.

Test steps carry independent assertions; implementation steps carry verified signatures/pinned values; verification carries command and signal. Keep the plan proportional: record decisions an implementer cannot safely infer, leave routine choices open when safe, and avoid pseudocode that merely transcribes the implementation. A plan several times longer than its code often dictates unnecessary detail.

Review Focus covers real missing inputs: empty/malformed, authorization, concurrent request, restart and partial failure. Assign each to its owner. Estimates guide splitting, not acceptance.

The same plan survives executor changes and compaction. Resolve conflicts against accepted spec/current repo with reason and cost if wrong. No automatic plan commit.

## Task acceptance and the standing quality floor

Per-task acceptance asks whether the requested behavior exists; the existing project Definition of Done asks whether it meets the standing quality bar. Map both into the same plan. Do not renegotiate thresholds under deadline pressure.

For each task check correctness and quality: runtime behavior, meaningful regression, relevant edge/error cases, naming, scoped changes and native lint/format checks. For the feature check integration, migration/config/flags, interface compatibility and current documentation. For release preparation also check relevant security, critical-path observability and rollback evidence. Only checks applicable to the actual project become requirements; the guide does not invent universal thresholds or grant merge/deploy authority.
