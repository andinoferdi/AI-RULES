# Human procedure quality

Status: IN PROGRESS
Depth: STANDARD
Current phase: Delivery
Base: 6bca170

## Decisions and acceptance

The upstream wizard makes progress and next actions concrete with a reusable
Bash layout. The original Andino fixture names a dashboard without a link or
completion signal. Adopt the stage layout for both checklists and scripts.
Keep native-shell choice, safe credential storage and explicit authority.

| Work | Acceptance | State |
| --- | --- | --- |
| Compare | Review the upstream guide and template against the Andino guide and fixture | DONE |
| Author | Match both entrypoints. Cover credential setup, a manual action with no value, and interrupted cutover. Preserve the deterministic example interface | DONE |
| Verify | Check representative outputs, run the existing oracle and review the owned diff | DONE |
| Deliver | Push workflow, verify remote default setup and update the stable manifest from isolated main | PENDING |

## NEXT ACTION

Publish the reviewed workflow commit, then verify default setup and the stable manifest.

