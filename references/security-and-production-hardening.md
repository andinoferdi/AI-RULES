# Risk-based security and production hardening

Read when the target crosses trust, sensitive data or release/migration boundaries,
or when evidence indicates a security/correctness risk. This is selective triage,
not a universal audit or a certification of production readiness.

Identify exposed entry points, actors, protected resources and irreversible effects
within scope. Prioritize critical correctness, data loss and security findings over
cosmetic debt. Severity expresses impact, not an instruction to replace the system;
prefer the smallest safe remedy with relevant regression proof.

## Inspect only implicated boundaries

| Signal / boundary | Evidence to collect | Targeted verification |
| --- | --- | --- |
| Authentication/authorization | Trace identity establishment and server-side enforcement for the resource/action, including ownership/tenant boundaries. UI hiding is not enforcement. | Allowed and denied actors, direct requests, expired/missing credentials and failure paths in a safe fixture. |
| Secrets/configuration | Check whether credentials enter source, artifacts, logs or client output; inspect effective configuration and unsafe defaults without exposing values. | Redacted evidence and project-native secret/config checks. Report exposure for authorized containment; do not silently rotate live credentials. |
| Dependency integrity | Verify package identity, installed/locked versions, source and reachability of the risky API or dependency. Use current authoritative advisories when needed. | Native lock/build/audit tooling and relevant execution paths; scanner output alone does not prove exploitability or safety. |
| Untrusted input/output | Trace input to command, query, file, network or rendered output sinks; examine validation, encoding and resource limits relevant to that sink. | Safe malformed/boundary/abuse fixtures without attacking external services. |
| Sensitive data and writes | Identify access, logging, retention/deletion, transaction and retry/concurrency behavior; distinguish validation from integrity constraints. | Fixture state before/after success, partial failure and duplicate/reordered work where applicable. |
| Migration/release | Inspect artifact/config provenance, old/new contract compatibility, operation ordering, destructive steps and recovery prerequisites. | Native build/migration dry run or isolated rehearsal; demonstrate recovery where risk requires it. |

Do not invent a required framework, security scanner, compliance regime or dependency.
Use installed project-native tooling when it answers the question; record unavailable
checks as UNVERIFIED. Consult version-specific official documentation for uncertain
semantics rather than copying a generic security recipe into core instructions.

## Containment, scope and proof

For a credible severe issue, stop lower-value cleanup and return concrete boundary,
impact and confidence evidence. Safe local remediation can proceed within existing
authorization. Live account changes, credential rotation, production-data changes,
deployment or irreversible containment require their applicable authorization.
Do not exploit real users or copy secrets into reproduction artifacts.

A successful rollback command may not recover deleted or incompatible data. Identify
backup/restore, reconciliation or forward-recovery needs before high-risk mutation.
If protection or recovery is insufficient, use INVESTIGATE with the next evidence
action rather than asserting the migration safe.

Return findings using the existing schema, including residual risks and deliberately
deferred work. "No issue found in these checked paths" is narrower than "secure".
Keep the remediation disposition independent of severity and provenance; retain
one acceptance/checkpoint owner: Andino when active, otherwise the host task context.
