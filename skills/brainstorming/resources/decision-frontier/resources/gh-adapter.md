# GitHub Issues Adapter Protocol

This protocol defines how `andino-decision-map` optionally synchronizes local decision maps with remote GitHub Issues via the `gh` CLI.

---

## 1. Safety Invariant: Read/Propose-First

The local Markdown file (`docs/decision-maps/<topic>/map.md`) is always the authoritative single source of truth.

- **No Unsolicited Mutations**: Never create, edit, or close remote GitHub Issues or comments without explicit user permission or authorization in the active plan.
- **Dry-Run Review**: Always display the proposed `gh` CLI commands and markdown payloads to the user before executing mutations.

---

## 2. Label Mapping Schema

When interacting with a remote GitHub repository, use the standard `wayfinder` taxonomy:

| Local Ticket Type | GitHub Label | Purpose |
|---|---|---|
| Map Issue (Root) | `wayfinder:map` | Master tracking index for the entire multi-session effort. |
| `research` | `wayfinder:research` | Autonomous AFK investigation issue. |
| `interview` | `wayfinder:grilling` | Human-in-the-loop dialog and requirements settlement. |
| `prototype` | `wayfinder:prototype` | Disposable spike issue to validate technical assumptions. |
| `task` | `wayfinder:task` | Concrete prerequisite action issue. |

---

## 3. Remote Map Issue Format

The master issue carries the label `wayfinder:map`:

```markdown
## Destination
Migrate monolith session storage to distributed Redis cluster with <5ms p99 latency without downtime.

## Notes
- **Domain**: Authentication and Session Lifecycle
- **Skills to consult**: `andino-brainstorming`, `andino-decision-interview`, `andino-planning`
- **Standing preferences**: Zero schema modifications to production database during peak hours.

## Decisions so far
- [#101](https://github.com/org/repo/issues/101): Selected Redis Sentinel over DynamoDB DAX based on 3.2x lower cost and 1.2ms read p99 latency.

## Not yet specified
<!-- Fog of War: Uncharted areas awaiting upstream decisions -->
- Session token rotation and refresh window parameters.
- Cross-region failover and read replica topologies.

## Out of scope
<!-- Explicit non-goals -->
- Biometric authentication integration.
- Custom cryptographic token signing routines.
```

---

## 4. Child Ticket Lifecycle via `gh` CLI

### A. Creating Child Tickets
Create child tickets as issues referencing the map issue:

```bash
# Example creating an interview ticket
gh issue create \
  --title "Define session timeout and concurrent login policies" \
  --label "wayfinder:grilling" \
  --body "## Question
What are the hard organizational limits for idle session timeouts and maximum concurrent active sessions per user account?

## Parent Map
Ref: #100

## Blocked By
None"
```

### B. Claiming a Ticket
Before starting work on an unblocked ticket, assign it:

```bash
gh issue edit 102 --add-assignee "@me"
```

### C. Resolving a Ticket via Comment
Always post the resolution, empirical evidence, and design implications as an issue comment, then close the issue:

```bash
gh issue comment 102 --body "## Resolution
Set idle session timeout to 30 minutes, absolute timeout to 12 hours, and allow maximum 5 concurrent sessions per user.

## Evidence
- Security compliance policy SEC-042 requires <= 30 min idle.
- Stakeholder sign-off: @security-lead confirmed in interview.

## Design Implication
Configures Redis TTL keys to 1800s with sliding window; unblocks token refresh architecture."

gh issue close 102 --reason "completed"
```

### D. Updating the Root Map Issue
After closing child issues, update the `## Decisions so far` section of the master map issue:

```bash
# Read current issue body
gh issue view 100 --json body -q .body > current-map.md

# Append new resolution line under ## Decisions so far and update
gh issue edit 100 --body-file updated-map.md
```
