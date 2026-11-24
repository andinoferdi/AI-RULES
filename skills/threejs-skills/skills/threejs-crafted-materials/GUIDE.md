---
name: threejs-crafted-materials
description: Build close-up wood, metal, cloth and paper materials in Three.js that survive macro views - growth-ring grain and finishes, structured metal reflections and patina, woven threads and sheen, paper fibres, translucency and creases. Use when a hero surface reads flat, plastic or tiled up close.
---

# Three.js Crafted Materials

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

## Pick the material

Each material has one reference with the mechanism, the constants that shipped,
rules paired with the failure they prevent, cost and checks, plus a runnable scene
that implements it. Read the one reference for the material in view; its constants
are the shipped values, so start from them instead of guessing.

| Material | Reference | Runnable example |
| --- | --- | --- |
| Wood: growth rings, figure, pores, rays, end grain, oil, wax or lacquer | [references/wood.md](references/wood.md) | `examples/wood-demo.html` |
| Metal: steel, brass, gold, copper, iron; polished, brushed, aged | [references/metal.md](references/metal.md) | `examples/metal-demo.html` |
| Cloth: woven threads, sheen, folds, hems, stitches, fray, translucency | [references/cloth.md](references/cloth.md) | `examples/cloth-demo.html` |
| Paper: washi, rag, kraft; fibres, deckle, creases, back-lit translucency | [references/paper.md](references/paper.md) | `examples/paper-demo.html` |

The examples load Three.js r169 from a CDN; when the project pins another version or
works offline, import the project's own `three` instead and keep the material code.

## Shared rules

- Procedural detail is data: build its fields in `NoColorSpace`, keep lighting linear
  and tone-map once at the end.
- Fade fine bands (pores, threads, fibres) by their own pixel footprint so they do not
  shimmer at grazing angles.
- Judge every material under the light it will live in, at the closest camera
  distance and at 2x, against a neutral reference.

## Related methods

- Scanned or authored PBR texture sets, texel density and delivery:
  `threejs-hires-textures`.
- Scoring a lit wood interior out of 10: `threejs-lighting-scorecard`.
- Where these surfaces sit in a photoreal scene: `threejs-realism-director`.
