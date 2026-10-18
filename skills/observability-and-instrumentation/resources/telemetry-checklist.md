# Telemetry proof checklist
Start with 2–4 on-call questions. Every field/signal answers one. Logs use JSON/stable event/level/correlation; entryPoint comes from originating scheduler/CLI/replay path, not downstream inference. Propagate both across queue/HTTP. Allowlist identifiers/metadata; never full bodies/tokens/passwords/PII.
RED on endpoint/dependency, USE on pool/queue/resource. Route templates/status classes/provider names are bounded labels; user/tenant/request IDs and raw URLs/errors belong only in appropriately redacted logs/traces. Histograms permit p50/p95/p99; means alone hide tails. Budget cardinality and retention.
Initialize tracing before clients; W3C context travels each async boundary. Manual spans name meaningful work, not every function. Low head sampling/default and error-retaining tail sampling when supported; no sensitive attributes.
Alert symptom + threshold/duration/SLO rationale + owner/runbook. Page for immediate user impact, ticket for slower degradation. Causes feed dashboards. Runbook minimum: what it means, first discriminating query, escalation. Correct stale steps when closing incident.
In authorized test environment emit a real failure; find by requestId and entryPoint, verify structured output and expected series, follow an unbroken trace and test alert delivery/runbook. Offline artifact inspection does not prove exporter or channel works. Recording external notification needs explicit authority.
Output signal/question map, actual artifact identifiers, observed gaps and deployment limitations.

Provenance: independently worded adaptation of the Addy snapshot identified in the owning GUIDE.md; full MIT notice at ../../../references/legal/addy-license.md. No upstream installation or hook is required.
