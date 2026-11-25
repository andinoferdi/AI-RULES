---
name: threejs-small-wildlife
description: Build and animate small 3D wildlife in Three.js - a bird with a recognizable species silhouette, folding wings, independent head and tail and grounded toes, and a butterfly that banks in flight, settles on a real plant surface with hinged wings and takes off when disturbed. Use for perching, takeoff, flight and landing in wildlife or garden scenes.
---

# Three.js Small Wildlife

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

Each animal has one reference with the rig, the motion states and the review steps,
plus a runnable study that implements it. Read the one reference for the animal in
view, then open its study before writing code.

| Need | Reference | Runnable example |
| --- | --- | --- |
| Bird: species silhouette, two-tract folding wings, independent head and tail, toes planted on a perch, hop, takeoff, flight and landing, a close-up contact shadow | [references/birds.md](references/birds.md) | `examples/birds/index.html`; reusable rig `examples/birds/assets/wagtail.js`; check `node references/birds/check-perch.cjs` |
| Butterfly: hinged wings mirrored at the thorax, cruise, approach, settle on a real plant surface, take off when disturbed, banking from turn rate | [references/butterfly.md](references/butterfly.md) | `examples/butterfly/index.html` |

## Shared rules

Each example opens from disk: it loads the classic Three.js build stored beside it in
`assets/` (keep its license file next to it). When the project pins another Three.js
version or bundles `three` as a module, import the project's own copy and keep the
technique code. Judge the result at the size and camera distance it will ship at,
with reduced motion on and off.

## Related methods

- Spring-follow motion, analytic timelines and quaternion control:
  `threejs-procedural-animation`.
- The plants they perch on: `threejs-procedural-vegetation`.
