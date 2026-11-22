# Human procedure quality

Status: DONE
Depth: STANDARD
Current phase: Complete
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
| Deliver | Push workflow, verify remote default setup and update the stable manifest from isolated main | DONE |

## NEXT ACTION

None. Task complete.


## Evidence

- Targeted human-procedure case passed the existing independent oracle.
  Both entrypoint bodies matched and the owned diff passed git diff --check.
  The historical full runner reported 24 failures on other methods.
- Workflow runtime e97c319 was pushed. Default project setup installed three
  targets and reported zero failures. All six human-procedure files matched
  their source after normalizing line endings.
- Stable manifest dc5f9f4 was pushed to main. Stage-only release build
  exported eight validated bundles. Existing bundled executables need a new
  release build to carry the updated pin.
- Author performed the review directly. Relative live model quality and
  live dashboard interaction were outside the observed checks.
