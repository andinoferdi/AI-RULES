---
name: threejs-procedural-fields
description: Build coherent procedural scalar and vector fields for Three.js materials and geometry. Use for terrain, planets, wear, biomes, clouds, water masks, displacement, roughness, normals, domain warping, and any visual where several channels must derive from shared causes.
---

# Procedural Fields

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

Do not start by stacking noise. Start by defining the fields the object physically or stylistically needs.

## Field contract

Before shader code, write a field bundle:

```text
coordinates
  → macro form
  → meso structure
  → derived causes
  → material channels
```

Example:

```text
sphereDirection
  → warpedDirection
  → elevation + ridges + craterDepth
  → slope + cavity + latitude + moisture
  → biome + color + roughness + bump
```

## Required workflow

1. Choose coordinates that remain stable under camera and object motion.
2. Lock real or perceptual scale for each frequency band.
3. Create named primary fields. Never hide the whole look in one expression.
4. Derive secondary fields from causes: slope from normals, shore from sea-level distance, wear from exposure, dirt from cavity.
5. Reuse the same fields across color, roughness, normal, displacement, emission, and scattering.
6. Add debug output for every named field.
7. Filter high-frequency fields by derivatives, tessellation density, or camera distance.

Read [references/field-stack-recipes.md](references/field-stack-recipes.md)
before implementation. It records sphere, terrain, water, and
structured-placement field contracts plus common parity defects.

Read the
[procedural planet surface](examples/shared-procedural-planet-surface/planet-system.js)
for a shared CPU/GLSL field bundle whose height, continents, climate, biomes,
roughness, and normals remain independently inspectable.

## Non-negotiable rules

- Independent noise per channel produces visual soup. Share structure.
- Domain warp the coordinates, not every result.
- Warp spherical coordinates tangentially, then renormalize.
- Use different frequency bands for silhouette, regions, surface breakup, and micro-normal.
- Do not displace geometry with frequencies the mesh cannot represent.
- Keep categorical masks broad enough to avoid isolated “bubble” regions.
- Parameter names must describe perception: `ridgeWidth`, `coastBlend`, `cavityDarkening`, not `noise3Amount`.

## Routing boundary

Use this skill when the shared field model is the task. Use
`$threejs-procedural-materials` when the task is channel assembly and material
response, and `$threejs-procedural-planets` when the deliverable is a complete
planetary body.
