# Standing completion gate
Task acceptance asks whether the requested behavior exists. Standing completion asks whether it is finished to project standards. Both matter, but depth is proportional and irrelevant checks need reasoned N/A.
Per task: current acceptance met; behavior observed, not merely compiled; meaningful regression catches missing behavior; errors/edges addressed; existing tests remain green; changes scoped/readable and no unimplemented placeholders. Canonical tdd owns behavior tests.
Per feature: boundary integration works, compatibility considered, migrations/config/flags accounted for; public contracts/readme/gotchas/ADRs reflect current facts.
Per release: relevant security/trust/PII reviewed, critical telemetry works, rollback/recovery exists and current human release authority is recorded. Missing live/runtime evidence is not equivalent to passing.
Record exact tested file/environment identity, command/result and unresolved limits in Andino's existing plan. A successful unchanged test may be reused; changed inputs require fresh relevant evidence. User's unrelated dirty files are not a failure and no auto-commit/merge/deploy follows.
Example: endpoint's unit tests green but worker retries not integrated→task unit proof exists, feature integration remains open. CLI docs-only typo→browser and telemetry N/A, link/content proof sufficient.

Provenance: independently worded adaptation of the Addy snapshot identified in the owning GUIDE.md; full MIT notice at ../../../references/legal/addy-license.md. No upstream installation or hook is required.
