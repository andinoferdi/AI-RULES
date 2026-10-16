---
name: threejs-procedural-architecture
description: Build authored procedural buildings and architectural kits in Three.js. Use for massing grammars, exposed-edge analysis, façade bays, profiles, arches, cornices, roofs, ornaments, material-slot mesh compilation, deterministic variants, and procedural city assets.
---

# Procedural Architecture

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

Separate design planning from mesh emission. A building generator should produce an inspectable plan before it produces triangles.

This skill contains exemplary examples and assets beyond descriptive guidance,
they're worth studying, referencing, or even copying. Use them sufficiently
when relevant and do NOT blindly skip them.

## Required architecture

```text
settings
  → mass grammar
  → exposed-surface graph
  → façade/roof placements
  → module registry
  → material-slot mesh writer
  → geometries
```

Read [references/grammar-and-mesh-compiler.md](references/grammar-and-mesh-compiler.md) before implementing the generator.

Read the
[procedural financial tower compiler](examples/procedural-financial-tower/building-system.js)
for seeded tier planning, semantic façade placement, reserved zones,
material-slot BufferGeometry output, projected detail, and mechanism-specific
diagnostics.

## Rules

- Massing, façade rhythm, and detail modules are separate layers.
- Resolve exposed edges before façade placement. Do not decorate hidden internal faces.
- Modules own semantic anchors and construction depth, not global building coordinates.
- Compile by material slot to reduce draw calls without destroying material separation.
- Preserve real dimensions for floor height, bay width, trim projection, and texture density.
- Randomness may select among valid designs; it must not repair invalid geometry.
- Provide topology, façade ownership, material/geometry, and shadow diagnostics
  appropriate to the renderer path.

## Acceptance

The generated building must survive:

- silhouette-only view;
- flat untextured material;
- grazing light;
- close inspection of corners and roof transitions;
- seed variation without broken bays, overlapping ownership, or floating ornament;
- triangle and module-count reporting.

## Routing boundary

Use `$threejs-procedural-geometry` for a reusable profile, sweep, ring, or mesh
writer without a building grammar. This skill owns massing, façade semantics,
architectural modules, and building-plan compilation.
