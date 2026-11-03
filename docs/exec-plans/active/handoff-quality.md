# Portable handoff quality

Status: IN_PROGRESS  
Depth: STANDARD  
Current Phase: Publish and install  
Base: `a6b876482eedea7198dbf579fc2235a23484d86d`

## Executive Snapshot

The original runnable example creates only a handoff and a result report. Its
evidence paths do not exist in the fixture and its next action names no runnable
check. Keep the existing authorization, drift and single-checkpoint rules.

## Objective and acceptance

- A recipient can start from a destination-reachable pointer and perform one
  concrete first action, or identify the exact dependency blocking that action.
- The handoff identifies current evidence, rationale, authority and material
  uncommitted state without creating a second plan.
- Both entrypoints teach the same procedure and the normal latest setup installs
  the reviewed content from the remote workflow branch.

## Execution Board

| Phase | Status | Evidence or acceptance |
| --- | --- | --- |
| Audit | DONE | Executed the original example in a temp directory and inspected the generated handoff. Compared upstream portability, phase selection and context curation. |
| Author and verify | DONE | Existing handoff oracle passed. Native and nested procedure/output sections matched. The check passed at both roots and failed on the missing patch at the relocated root. The blocked variation was reviewed as a written scenario. |
| Publish and install | IN_PROGRESS | Push the workflow branch, run latest setup for an isolated Codex project, compare installed content. |

## Change specification

1. In both handoff entrypoints, order the procedure around recipient intent,
   destination-visible artifacts, transfer of exact work state, and a cold read.
   Require a first action with location, operation and expected signal. For a
   blocker, require owner, missing input and an observable resume condition.
2. In the existing worked-example resource, keep the deterministic runner's
   `handoff.md` and `result.json` interfaces. Provide actual `spec.md` and
   `changes.diff` fixtures and an executable next check. Exercise a blocked
   handoff and a destination missing the patch as bounded variations.
3. Verify the example, existing deterministic oracle and installer readback.
   Default latest setup follows the remote branch. Bundled setup uses a frozen
   manifest and is a separate distribution path.

## NEXT ACTION

Push the reviewed workflow change, then run latest setup for an isolated Codex
project and compare the installed entrypoints and worked example with source.
