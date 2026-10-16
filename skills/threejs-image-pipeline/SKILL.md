---
name: threejs-image-pipeline
description: Build a deliberate final-image pipeline for advanced Three.js scenes. Use for depth, normal, albedo, and history ownership; GTAO or bent normals; bloom; eye adaptation; tone mapping; 3D LUT grading; effect-local render targets; and pass diagnostics.
---

# Image Pipeline

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

Use this skill only when composing several image-space systems or defining shared buffers. For one effect, load its atomic skill instead.

Load:

- `$threejs-screen-space-ambient-occlusion` for GTAO, bent normals, denoising, or AO application;
- `$threejs-bloom` for HDR extraction and bloom;
- `$threejs-exposure-color-grading` for metering, adaptation, tone mapping, LUTs, and output conversion.

The pipeline must expose its signals and ordering. Do not install a pile of effects and tune the final frame blindly.

## Signal order

```text
scene HDR color + depth + normals + albedo where required
  → lighting-related screen effects
  → atmosphere/transparency composition
  → bloom
  → exposure
  → tone mapping
  → grading
  → lens/presentation effects
  → output conversion
```

Read [references/production-image-pipeline.md](references/production-image-pipeline.md)
for four production pass graphs, their buffer/resolution contracts, and the
ownership boundaries between whole-scene and effect-local graphs.

## Rules

- Tone-map once.
- Keep HDR bloom before tone mapping.
- Meter exposure from a small luminance target, not the final 8-bit screen.
- Separate direct and indirect light before applying bent-normal ambient tint when possible.
- Upsample low-resolution effects with depth/normal-aware weights.
- Build pass toggles and effect-only views before tuning.
- UI rendered in the same target needs an explicit protection strategy.
- Do not load all atomic post skills by default. Route only the effects actually requested.

## Routing boundary

Use this skill when multiple image-space systems must share buffers, ordering,
or output ownership. For one isolated effect, use its atomic skill without
loading this coordinator.
