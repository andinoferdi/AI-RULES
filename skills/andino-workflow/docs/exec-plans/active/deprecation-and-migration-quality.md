# Deprecation and migration skill quality

- Base: `8ecb810`
- State: Published and setup verified; model comparison open
- Phase: Verification

## Decision and evidence

The current guide specifies what evidence matters but compresses the handoff into one paragraph. The Addy Osmani reference demonstrates a consumer-facing notice and migration steps, but leaves the production evidence and authority boundaries less explicit. Use the same Andino structure and add an actionable handoff, pattern selection criteria, and a separate contract decision. Keep the activation, safety, offline example and provenance.

## Tasks

1. In the skill's Procedure, identify why a team should keep, migrate or retire an interface, choose among adapter, flags and strangler routing, and specify how to keep concurrent writes and a resumable backfill consistent. Gate destructive contract on evidence for old consumers and recovery.
2. In Output and verification, define fields for the decision, consumer handoff, deployment ledger and contract decision. Add one worked handoff with explicit missing production evidence.
3. Compare guidance against external API retirement, mixed-version schema change and incomplete usage evidence. Run both existing SQLite example variants and check their exact JSON. Review the diff, commit to and push `andino-workflow`, then verify a project-scoped setup installs the published guide.

## NEXT ACTION

When a model comparison is available, run the three scenarios on the same model with isolated contexts for the baseline, reference and revision. Score the outputs against the handoff and contract criteria above.

## Verification evidence

- Static review: the external API case now has a consumer handoff and notice fields, the mixed-version case has writer coverage and reconciliation gates, and the incomplete-usage case holds contract until the missing observation is checked.
- Both embedded SQLite variants matched the documented JSON values. One allowed contract with zero old consumers, and the other held contract with one old consumer.
- The project-scoped Codex setup installed the prior published bundle in a disposable project. Use that project for the upgrade check.
- Published skill revision `63718b8`. Default-source project-scoped setup applied an update in the disposable project and installed the skill in a fresh project, with zero failed or blocked targets. Both installed guides had identical SHA-256 `b3d6f2b2835c96d856967f198116ae2a372ed712ddeece7bc122c7914b106926`. The installed guide matched the checkout after normalizing line endings.
- The scenario review covers the written procedure. Independent model output quality remains unmeasured.
