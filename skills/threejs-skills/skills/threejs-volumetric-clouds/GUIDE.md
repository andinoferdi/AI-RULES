---
name: threejs-volumetric-clouds
description: Implement volumetric cloud systems in Three.js. Use for weather-driven density, bounded raymarching, shape/detail erosion, vertical profiles, lighting cones, silver lining, temporal reconstruction, cloud shadows, multiple layers, and scalable quality modes.
---

# Volumetric Clouds

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

Cloud quality comes from density organization, lighting, and temporal stability—not from increasing march steps over unstructured noise.

This skill contains exemplary examples and assets beyond descriptive guidance,
they're worth studying, referencing, or even copying. Use them sufficiently
when relevant and do NOT blindly skip them.

## System order

1. Define the cloud volume and layer bounds.
2. Generate or source weather, base-shape, detail, and turbulence fields.
3. Build a density function with vertical and weather profiles.
4. Raymarch only the bounded occupied segment.
5. Integrate transmittance and lighting front-to-back.
6. Reconstruct low-resolution output temporally.
7. Project a separate low-cost cloud-shadow solution.

Read [references/weather-volume-and-reconstruction.md](references/weather-volume-and-reconstruction.md) before implementing or auditing the cloud system.

Read the [weather volume cloud entry](examples/weather-volume-clouds/cloud-effect.js)
and its `source/` modules for weather-layer ownership, spherical shell bounds,
authored shape/detail sampling, cloud shadow maps, temporal upscale,
atmospheric composition, and package-owned diagnostics.

## Required controls

- coverage, cloud type, precipitation, and anvil bias;
- base/top altitude and vertical density profile;
- shape/detail scales and erosion;
- wind for each field;
- primary step count, light step count, and empty-space policy;
- history weight and disocclusion threshold;
- cloud-shadow extent, resolution, and update rate.

## Failure conditions

- density is only `fbm(position)`;
- the raymarch traverses the full camera range;
- detail noise adds density instead of eroding shaped masses;
- temporal history is accepted across disocclusion;
- shadows use the full beauty raymarch;
- every cloud layer shares the same wind and density profile.

## Routing boundary

Use `$threejs-atmosphere-aerial-perspective` for molecular/aerosol scattering
without weather density. Use `$threejs-procedural-vfx` for emissive aurora
curtain slabs or bounded interactive voxel fire and smoke with velocity,
pressure, emitter, and collision fields. This skill owns weather-shaped cloud
volumes, reconstruction, cloud lighting, and cloud shadows.
