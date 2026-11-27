# Release checklist by surface

Walk the sections the candidate's diff touches (step 3). Record every item you check as a gate:

```text
| Gate | Expected | Observed (command or file, and result) | Status | Owner / next action |
```

Status is PASS, FAIL, UNAVAILABLE (could not be checked: say why and who can) or NOT APPLICABLE
(say why). Use the repository's Definition of Done and release policy first; the items below fill
the gaps. A routine Standard release keeps the table short: one row per touched surface, with the
items that matter for this diff.

## Build and behaviour

- [ ] Clean build of this exact candidate (tag, commit or digest), with no new warnings.
- [ ] Unit, integration and end-to-end tests for the changed paths ran and passed; count the
      skipped and quarantined ones and name what they would have covered.
- [ ] Lint and type checks pass.
- [ ] The change was reviewed and approved.
- [ ] Staging (or a production-like environment) ran this candidate and a smoke test of the
      critical journeys passed. Staging that was down or skipped is UNAVAILABLE, not PASS.
- [ ] No leftover debugging output (`console.log`, `print`, `dbg!`) or TODOs that block launch.
- [ ] Error handling covers the expected failure modes of the new paths.
- [ ] Both flag states (off and on) are tested.

## Security

Deeper review belongs to `security-and-hardening`. At release time check:

- [ ] No secrets in code, config or history of the candidate (`git log -p` on the diff, a secret
      scanner when the project has one). A found secret is a FAIL: remove it, rotate it, report
      the file and the key name only.
- [ ] The ecosystem's dependency audit (`npm audit`, `pip-audit`, `cargo audit`, `govulncheck`)
      shows no critical or high finding in new or changed dependencies.
- [ ] Input validation on every new or changed user-facing endpoint.
- [ ] Authentication and authorization checks on new routes and actions, including who may see
      shared data.
- [ ] Security headers unchanged or improved (CSP, HSTS, X-Content-Type-Options).
- [ ] Rate limiting on authentication and other abusable endpoints.
- [ ] CORS lists specific origins; a wildcard origin never combines with credentials.

## Performance

Deeper work belongs to `performance-optimization`. At release time compare with the current
production baseline:

- [ ] Critical-path latency (p95) and throughput on comparable load.
- [ ] Core Web Vitals for changed pages at the 75th percentile: LCP at most 2.5 s, INP at most
      200 ms, CLS at most 0.1 (web.dev "good" thresholds).
- [ ] No N+1 queries on critical paths; new queries have the indexes they need.
- [ ] Bundle size within its budget; images compressed, sized and lazy-loaded.
- [ ] Caching configured for static assets and repeated queries.
- [ ] Saturation headroom: CPU, memory, database connections, queues.

## Accessibility

For changed UI:

- [ ] Every interactive element works with the keyboard, in a sensible order, with visible focus.
- [ ] Focus is managed for dialogs and content that appears or changes.
- [ ] Controls and images have accessible names; structure reads correctly in a screen reader.
- [ ] Text contrast meets WCAG AA: 4.5:1 for normal text, 3:1 for large text.
- [ ] Error messages are specific and tied to their fields.
- [ ] axe-core or Lighthouse shows no new accessibility violations.

## Infrastructure and data

- [ ] Production configuration and environment variables are set, in code or the secret store,
      not by hand from memory.
- [ ] Every migration works with both the previous version and the candidate (expand, migrate,
      contract). Destructive steps are deferred to a later release.
- [ ] A backup exists from before the change, and a restore of it has been tested; record when.
- [ ] Health endpoint responds and reports the deployed version.
- [ ] Logging, error reporting and metrics for the new paths reach the dashboards, split by cohort.
- [ ] DNS, TLS certificates and CDN configuration are in place for new hosts or assets.
- [ ] The flag mechanism can turn the feature off; the time it takes is known.
- [ ] Capacity covers the 100% stage at peak.

## Documentation

- [ ] Release notes and changelog describe what users and operators will see, including
      removals.
- [ ] Runbook: deploy steps, the stage plan, the rollback plan and who is on call.
- [ ] API documentation and compatibility notes for changed contracts.
- [ ] README or setup notes for new configuration; an ADR for an architectural decision
      (`documentation-and-adrs`).
- [ ] User-facing help updated where behaviour changed.

## Pointers

- Pipeline gates, artifact promotion and deploy order: `ci-cd-and-automation`.
- Alert rules, SLOs and dashboards: `observability-and-instrumentation`.
- Designing the phases of a schema or API change: `deprecation-and-migration`.
- Browser checks of a changed page: `browser-testing-with-devtools`.

Provenance: concrete items adapted from Addy Osmani's `shipping-and-launch` and its shared
checklists (addyosmani/agent-skills 3d78ead, MIT); thresholds from web.dev and WCAG. Full notice
in [../references/license.md](../references/license.md).
