---
name: threejs-enemy-systems
description: Build or refactor reusable, data-driven enemy archetype and moveset systems for Three.js action games, plus rigged monster contracts and combat enemy AI. Use for enemy content schemas, model and rig conventions, combat move timing and contact contracts, runtime state boundaries, placeholder fallbacks, monster joints, sockets, hurtboxes and attack volumes, aggro, target selection, spacing, telegraphs, retreats, boss behavior, behavior-state machines, deterministic fixtures and AI regression tests.
---

# Build Three.js Enemy Systems

## AI-RULES integration

Use this specialist only for the domain need described above. Ordinary frontend
work without that need is excluded. Inspect the project's actual Three.js and
renderer versions before applying examples; examples are not compatibility claims.
This is an internal method of the installed threejs-skills family. Resolve selected
siblings as ../<method-id>/GUIDE.md within that family, through authorized resource
reads after family invocation; they are not separate native skill registrations.
An absent sibling is optional guidance, not an installation dependency.
Never bypass explicit-only or denied invocation controls by reading another path.
Load the minimum relevant specialists at the phase where they are needed.

When Andino Workflow is active it owns the single execution plan, checkpoints,
handoff and DONE decision. Focus owns communication; Search First owns relevant
solution/API research. Return domain results, evidence, limitations and recommended
actions to that existing context. Without Andino use the host's normal task context.
Provider job journals and render-resource lifecycles are technical state, not a
second task lifecycle. Installation, discovery, activation and observed use differ.
External services, paid generation, delegation and publication need applicable
task authorization; this skill grants none.

Make each enemy a portable authored definition consumed by shared runtime systems. Keep AI choice, combat resolution, rendering, and feedback as separate consumers of the same stable contract.

## Separate content from runtime state

- Put stable IDs, role/tags, base stats, presentation spec, move IDs, AI hints, feedback hook IDs, rewards, and variant data in immutable authored definitions.
- Put instance ID, transform, health/posture, target, current move and phase clock, cooldowns, statuses, pathing, visibility, and LOD state in runtime instances.
- Reference definitions by ID. Reject duplicate IDs, missing references, invalid ranges, or impossible timing during content validation.
- Never mutate authored definitions, store live timers in content, or duplicate the combat clock across AI, animation, and rendering.

## Normalize presentation contracts

Define these fields before integrating a model:

- source or factory ID, provenance, coordinate system, forward axis, and meters-per-unit;
- root pivot at ground contact, normalized scale, facing offset, and visual height;
- simple movement collider plus named hurtboxes, independent of render geometry;
- stable sockets for contact origins, weapons, projectiles, VFX, audio, UI markers, and targeting;
- rig and semantic clip map for idle, locomotion, moves, reactions, and death;
- LOD tiers with hysteresis, animation/update policy, and unchanged gameplay colliders.

Normalize at the asset boundary. Do not scatter scale fixes, pivot offsets, raw clip names, or compensating rotations through gameplay code.

## Define moves as data

For every move, define:

- stable ID, AI tags, eligibility range/angle/line-of-sight, weight, and state prerequisites;
- startup and telegraph, one or more active windows, recovery, cooldown, and minimum commitment;
- movement, facing, cancellation, armor, interrupt, stagger, and phase rules;
- contact shape/socket, damage, posture, knockback, status, and per-target hit limits;
- semantic animation, VFX, and audio hook IDs with cleanup rules.

Let AI select only legal move IDs; let the combat system own timing and outcomes. Resolve damage from authoritative collision/contact events using stable action and target identifiers. Apply each contact once, then drive animation, VFX, audio, and UI from the resolved event.

## Provide an honest fallback

When a production model is unavailable, use a deliberate placeholder that preserves footprint, height, pivot, collider, sockets, facing, move timing, and state readability. Log the fallback once and keep it visually unmistakable. Never silently substitute a mismatched asset or call placeholder visuals production-ready.

## Add a new enemy

1. **Existing archetype and moves fit?** Configure a new definition; do not add runtime branches.
2. **A new behavior is essential?** Add the smallest reusable move, hook, or AI tag before adding a new subsystem.
3. **Model ready?** Normalize it to the shared presentation contract; otherwise use the honest fallback.
4. **Content complete?** Validate references, timing, contact, cooldown, recovery, interrupts, and feedback hooks.
5. **Proof ready?** Add deterministic fixtures and automated tests, then run desktop and mobile playthroughs.

## Prove the system

- Create deterministic fixtures for spawn, each move phase, wrong range/direction, obstruction, interrupt, stagger, death/reset, missing-model fallback, LOD transitions, and multiple instances sharing one definition.
- Test content uniqueness and references, active-window boundaries, cooldown/recovery, per-target hit deduplication, lifecycle cleanup, and pause/frame-step behavior.
- Play a representative encounter in the repository-approved browser. Confirm telegraphs, contact, state, animation, VFX/audio, targetability, and rewards agree.
- Verify desktop and mobile camera distance, touch controls, reduced motion, console health, frame time, draw calls, memory stability, and crowded-scene LOD behavior. Report baseline failures separately.

## More recipes in this method

| Need | Reference | Runnable example |
| --- | --- | --- |
| Rigged monsters: asset contract, procedural or imported creature rigs, semantic joints and sockets, hurtboxes and attack volumes, enemy-runtime adapters, LODs | [references/monster-system.md](references/monster-system.md) | — |
| Combat enemy AI: aggro, target selection, navigation, spacing, attack choices, telegraphs, retreats, boss behavior, AI regression tests | [references/enemy-ai-tuning.md](references/enemy-ai-tuning.md) | — |
