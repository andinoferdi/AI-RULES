---
name: threejs-exposure-color-grading
description: Build a measured exposure and grading path in Three.js. Use for a 64x36 encoded luminance meter, asynchronous readback, weighted log-average exposure, asymmetric adaptation, single tone-map ownership, and a generated 32-cube post-tone-map LUT.
---

# Exposure and Color Grading

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

Treat exposure, tone mapping, grading, and output conversion as distinct stages. Tune them from measured HDR signal, not by stacking compensating color operations.

## Order

```text
HDR scene
  → luminance meter
  → adapted exposure
  → tone map
  → creative grade / 3D LUT
  → final output conversion
```

Read [references/scene-referred-color-pipeline.md](references/scene-referred-color-pipeline.md)
for the exact 64x36 meter, encoded readback, adaptation constants, 32-cube LUT,
and signal-ownership ambiguities.

## Failure conditions

- tone mapping occurs in both materials and post;
- exposure is used to repair physically inconsistent light ratios;
- meter weighting and scene framing are not inspected;
- adaptation speed is the same toward light and dark;
- LUT input/output spaces are undocumented;
- sRGB encoding happens twice;
- a display-domain LUT is moved before tone mapping without being rebuilt.

## Routing boundary

Use `$threejs-bloom` for HDR glow contribution and
`$threejs-image-pipeline` when this color path must share ownership with AO,
atmosphere, or effect-local render targets.
