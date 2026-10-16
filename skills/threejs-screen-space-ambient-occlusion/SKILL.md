---
name: threejs-screen-space-ambient-occlusion
description: Implement a production GTAO path in Three.js. Use for half-resolution horizon sampling, reversed-depth reconstruction, bent-normal encoding, full-resolution bilateral reconstruction, environment-light application, contact grounding, and halo diagnosis.
---

# Screen-Space Ambient Occlusion

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

AO estimates missing ambient visibility. It must modulate indirect lighting, not repaint all scene color with a dark multiply.

## Workflow

1. Verify linear depth and view-space normals.
2. Reconstruct view position consistently.
3. Sample horizon visibility in a controlled radius.
4. Estimate AO and optional bent normal.
5. Denoise with depth/normal-aware filters.
6. Apply to indirect diffuse and environment response.

Read [references/gtao-bent-normal-pipeline.md](references/gtao-bent-normal-pipeline.md).

## Failure conditions

- direct light and emission are darkened;
- radius is specified only in pixels;
- foreground silhouettes cast thick screen-space halos;
- depth discontinuities are blurred together;
- AO remains strong at distances where its world radius is subpixel;
- bent normals are treated as ordinary geometric normals;
- the implementation claims temporal accumulation even though this path has none.

## Routing boundary

This skill owns GTAO gathering, bent normals, denoising, and AO application.
Use `$threejs-image-pipeline` only when its depth/normal buffers or pass order
must be coordinated with other image-space systems.
