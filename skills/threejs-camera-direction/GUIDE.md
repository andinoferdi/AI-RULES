---
name: threejs-camera-direction
description: Direct advanced Three.js camera systems. Use for scale-aware chase rigs, thrust lag, side/orbit cameras, body-relative up vectors, quaternion handoffs, authored cinematic framing, floating origins, pointer-look controls, camera collision constraints, projection ownership, and lifecycle restoration.
---

# Camera Direction

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

Treat the camera as an authored visual system, not a passive viewport. Compose
the subject, establish scale, choose a stable up frame, and make every mode
handoff explicit.

## Build order

1. Define the design frame: subject size, screen occupancy, lens, near/far,
   motion, and horizon/up convention.
2. Build camera targets in semantic frames: ship, body surface, docking axis,
   or scene-authored shot.
3. Derive position and orientation independently, then combine them once.
4. Add input orbit/look only inside declared yaw/pitch and spatial constraints.
5. Add frame-rate-independent follow or a bounded spring where the reference
   uses inertia.
6. Snapshot and restore camera projection/state when a scene owns it.
7. Test mode transitions, cuts, pointer-lock reacquisition, resize, and large
   coordinates.

Read [references/camera-rig-and-cinematic-systems.md](references/camera-rig-and-cinematic-systems.md)
for exact chase/side/orbit rigs, projection values, transition
rules, floating-origin shot, pointer controls, and implementation limits.

## Non-negotiable rules

- Use subject dimensions to derive offsets; do not tune one fixed distance for
  differently scaled assets.
- For planetary motion, derive up from the dominant body rather than global Y.
- Interpolate position with `lerp` and orientation with `slerp`.
- During an explicit handoff, use one interpolation stage. Do not stack a
  transition blend and a second follow smoother over the same interval.
- Re-sync yaw/pitch from the camera when pointer lock is acquired.
- Update the projection matrix whenever FOV, near, far, or aspect changes.
- Keep stars or infinite backgrounds camera-relative when large translation
  would create false parallax or precision loss.
- Restore camera and input ownership on scene disposal.

## Routing boundary

Use `$threejs-procedural-animation` for object motion timelines, springs,
docking, staging, and debris. This skill owns how the scene is viewed and how
camera modes hand off.
