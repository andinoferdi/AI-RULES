# Portable handoff quality

Status: DONE

Depth: STANDARD

Current Phase: Complete

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
| Publish and install | DONE | Pushed `6757d66`. Default `ai-rules setup` installed all three targets in a disposable Codex project. Readback matched both installed entrypoints and their worked example, including the nested guide. |

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

None. Task complete.

## Verification limits

Review was performed in the authoring session. The fixture and installation
checks cover artifact usability and distribution. Relative live model quality,
native activation, and frozen release builds were outside those checks.
