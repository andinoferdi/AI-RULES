# REMASTER-01 — Environment remaster resume fixture

Status: TODO
Plan Depth: DEEP
Current Phase: Phase 3 — Visual systems
Last Updated: 2026-09-15

## Executive Snapshot

Remaster a low-poly environment without changing gameplay contracts. Baseline and
the shared weather contract are complete. Resume visual systems at `Sky.tsx`; do not
repeat population diagnosis or weather constant extraction.

## Objective

Produce cohesive, deterministic weather visuals while preserving simulation behavior.

## Acceptance Criteria

- [x] Baseline captures current lint, build and population behavior.
- [x] One shared weather contract drives visual consumers.
- [ ] Sky, clouds, rain and vegetation follow that contract across quality tiers.
- [ ] Final lint/build, visual checks and manual acceptance pass.

## Scope

### In Scope

- Weather presentation, deterministic visual generation and evidence-backed cleanup.

### Out of Scope

- New models, gameplay redesign, ecosystem feature expansion and deployment.

## Baseline / Starting Evidence

- Lint baseline: 42 findings; production build passes.
- Population collapse reproduction and the confirmed pre-existing cause are recorded in Phase 1 evidence.

## Constraints & Invariants

- Preserve public scene props, movement values, species behavior and the frozen art direction.
- Use seeded randomness for memoized visuals and refs for per-frame mutable state.

## Architecture / Approach

One weather module owns wind, palette, quality tiers and eased transitions. Sky,
clouds, rain and vegetation consume that contract without importing each other.

## Execution Board

| Phase | Status | Goal | Scope | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 1 — Baseline and population | DONE | Establish proof and remove the blocker | simulation and baseline commands | Root cause fixed; focused stability check passes. |
| Phase 2 — Shared weather contract | DONE | Create deterministic shared primitives | `effects/weather.ts` | Unit/type checks pass; exports are stable. |
| Phase 3 — Visual systems | TODO | Apply the contract across renderers | `Sky.tsx`, clouds, rain, vegetation | Pending. |

# Detailed Execution

## Phase 1 — Baseline and population

Status: DONE
Goal: Establish baseline and resolve the blocking population defect.

### Result / Evidence

- Actual: reproduction confirmed one source of population collapse; focused stability run passes after the fix.

## Phase 2 — Shared weather contract

Status: DONE
Goal: Provide deterministic primitives for all weather consumers.

### Technical Contract

Input: rain state and quality setting.
Output: stable wind, palette, tier and eased blend values.
Postconditions / invariants: no consumer owns a competing wind direction.

### Result / Evidence

- Actual: `effects/weather.ts` exports the agreed constants and helpers; type check passes.

## Phase 3 — Visual systems

Status: TODO
Goal: Apply shared weather state without changing scene APIs.

### Context / Known Evidence

- Phase 2 exports are current. Existing public component props must remain stable.

### Verification

- Planned: targeted visual snapshots followed by lint and build.
- Expected/pass criteria: deterministic visuals, coherent transitions and no gameplay regression.

## Decisions Log

- D-001 — One WIND source prevents direction drift across clouds, rain and trees.
- D-002 — Eased blending preserves visual continuity across weather toggles.

## Plan Revisions

- R-001 — Visual implementation moved after population diagnosis because baseline evidence showed a blocking pre-existing defect.

## Verification Matrix

| Requirement | Verification | Status | Evidence |
| --- | --- | --- | --- |
| Stable population baseline | focused timed census | DONE | No collapse in the bounded run. |
| Shared deterministic weather | type check and source inspection | DONE | Stable exports; seeded generation. |
| Cohesive visual systems | screenshots, lint and build | TODO | Pending Phase 3. |

## Files / Areas Touched

- `simulation/population.ts` — actual root-cause fix.
- `effects/weather.ts` — actual shared weather contract.

## Approval Gates

### APPROVAL GATE — Final visual acceptance

Required before: final squash or release action
Status: WAITING

## Handoff Notes

- Do not repeat: population reproduction/fix or weather contract extraction; current evidence remains valid.
- First inspect: `Sky.tsx` and the exports from `effects/weather.ts`.
- Then: implement the first visual consumer and run its targeted check before expanding scope.

## NEXT ACTION

Inspect `Sky.tsx` against `effects/weather.ts`, wire the shared palette and eased
rain blend without changing public props, then run the targeted type/build check.
