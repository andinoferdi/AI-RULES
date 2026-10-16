---
name: threejs-procedural-animation
description: Build advanced procedural animation in Three.js. Use for launch kinematics, gravity turns, staging, spin docking, target-frame decomposition, spring-follow motion, rotating-frame alignment, peeling debris, analytic transform timelines, frame-rate-independent response, and quaternion control.
---

# Procedural Animation

## AI-RULES integration

Use this specialist only for the domain need described above. Ordinary frontend
work without that need is excluded. Inspect the project's actual Three.js and
renderer versions before applying examples; examples are not compatibility claims.
Use the host's permitted discovery/invocation mechanism for selected siblings;
an absent sibling is optional guidance, not an implicit installation dependency.
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

Animate semantic state, not unrelated transform curves. Define phases,
coordinate frames, velocities, and ownership before writing per-frame updates.

## Build order

1. Define the timeline phases and event boundaries.
2. Choose the frame for each motion: world, subject local, orbital radial,
   docking axis, or camera shot.
3. Derive target position/orientation from that frame.
4. Use analytic kinematics for authored travel and springs for responsive
   convergence.
5. Preserve world transforms when detaching children from a hierarchy.
6. Separate translation, alignment, spin, and secondary debris state.
7. Clamp integration delta and reset every state variable on replay/disposal.

Read [references/procedural-motion-and-docking-systems.md](references/procedural-motion-and-docking-systems.md)
for the launch, staging, docking, debris, spring, quaternion, and
frame-rate-independent response implementations.

## Non-negotiable rules

- Use elapsed seconds and `deltaSeconds`; do not make motion frame-count based.
- Derive orientation from direction/frame, then apply roll or spin as a
  separate quaternion.
- Decompose docking error into axial and radial components.
- Switch from spring convergence to an exact terminal pose at the end of a
  sequence.
- When reparenting an animated object, capture world position, quaternion, and
  scale before removal.
- Use seeded randomness when motion must be reproducible.
- Keep visual shake in a bounded envelope and separate it from trajectory.

## Routing boundary

Use `$threejs-camera-direction` for shot composition and camera handoffs.
Use `$threejs-procedural-vfx` when the deliverable is primarily plasma, sparks,
or effect pooling rather than object transform motion.
