---
name: threejs-shadow-systems
description: Implement stable, scalable directional-shadow systems for Three.js. Use for large procedural worlds, city scenes, terrain, moving cameras, WebGPU/TSL shadow nodes, cascades, cached clipmaps, texel stabilization, update budgets, and targeted invalidation.
---

# Shadow Systems

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

Use a single shadow map only when its receiver region is genuinely bounded. For large moving views, make shadow coverage an explicit spatial hierarchy.

## Cached clipmap workflow

1. Define concentric light-space square levels.
2. Snap each level center to its own texel grid.
3. Cross-fade adjacent levels in shader space.
4. Refresh near levels continuously.
5. Cache coarse levels and update them under a frame budget.
6. Invalidate intersecting levels when important casters or streamed terrain change.
7. Scale normal bias by world-space texel width.

Read [references/cached-clipmap-shadows.md](references/cached-clipmap-shadows.md) before implementing a large-world directional light.

Read the
[cached shadow clipmaps](examples/shared-procedural-financial-tower/shadow-clipmaps.js)
for three light-space square levels, per-level texel snapping, containment
cross-fades, cached coarse updates, scaled bias, and unshadowed outside weight.

## Failure conditions

- projection centers move by fractions of a texel;
- shader containment does not match the map's committed center;
- all cascades refresh every frame without evidence;
- coarse levels freeze moving casters indefinitely;
- depth texture samples occur in divergent fragment control flow;
- the same normal bias is used across radically different texel sizes;
- level boundaries become visible under camera motion.

## Routing boundary

Use this skill for light-space directional shadow maps. Use
`$threejs-screen-space-ambient-occlusion` for view-dependent ambient
visibility; AO is not a replacement for cast shadows.
