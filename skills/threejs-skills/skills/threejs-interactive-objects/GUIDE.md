---
name: threejs-interactive-objects
description: Build interactive 3D objects for product pages and interfaces in Three.js - lit feature-grid objects that turn on hover, a hover lean with a click-to-inspect view you can turn and dolly, surfaces that break into grains around the pointer and reassemble, and detailed miniature control icons in a reusable atlas. Use for product instruments, hero sculptures, specimen viewers, feature cards and small interface controls.
---

# Three.js Interactive Objects

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

## Pick the recipe

Each interaction has one reference with the mechanism, the constants that shipped and
the review steps, plus a runnable page that implements it. Read the one reference for
the interaction in view, then open its page before writing code.

| Need | Reference | Runnable example |
| --- | --- | --- |
| Feature grid: a lit 3D object per HTML card that turns on hover and eases back to its composed pose | [references/feature-objects.md](references/feature-objects.md) | `examples/feature-objects/index.html` |
| Orbit and inspect: hover leans the camera around one object, click lifts it into the hand to turn, coast and dolly, Esc puts it back | [references/orbit-inspect.md](references/orbit-inspect.md) | `examples/orbit-inspect/demo.html` |
| Hover dissolve: the surface breaks into grains around the actual pointer hit and reassembles when the pointer leaves | [references/hover-dissolve.md](references/hover-dissolve.md) | `examples/hover-dissolve/index.html` |
| Control icons: detailed miniature objects with physically based materials, lit for small interface controls, delivered as a high-density atlas | [references/control-icons.md](references/control-icons.md) | `examples/control-icons/index.html` |

## Shared rules

Each example opens from disk: it loads the classic Three.js build stored beside it in
`assets/` (keep its license file next to it). When the project pins another Three.js
version or bundles `three` as a module, import the project's own copy and keep the
technique code. Judge the result at the size and camera distance it will ship at,
with reduced motion on and off.

## Related methods

- Raycasting, pointer and touch input, camera controls: `threejs-interaction`.
- Camera rigs and handoffs for a whole scene: `threejs-camera-direction`.
- Close-up wood, metal, cloth and paper: `threejs-crafted-materials`.
