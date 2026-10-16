---
name: threejs-atmosphere-aerial-perspective
description: Implement physically motivated sky and aerial-perspective systems in Three.js. Use for planetary atmospheres, ground-to-space transitions, Rayleigh/Mie scattering, precomputed LUTs, depth-based transmittance and inscattering, sun/moon discs, and atmosphere-aware lighting.
---

# Atmosphere and Aerial Perspective

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

Treat sky rendering and aerial perspective as two views of the same scattering model. They must share radii, density profiles, coefficients, sun direction, exposure scale, and coordinate transforms.

This skill contains exemplary examples and assets beyond descriptive guidance,
they're worth studying, referencing, or even copying. Use them sufficiently
when relevant and do NOT blindly skip them.

## Choose the implementation tier

- Small scene with no orbital camera: analytic height/distance approximation.
- Planetary ground-to-space camera: ray integration or precomputed LUTs.
- Large geospatial world: LUTs plus world-to-planet transform, altitude correction, and depth-aware aerial perspective.

Read [references/atmosphere-system-contract.md](references/atmosphere-system-contract.md)
before implementation. It separates the LUT/ellipsoid architecture from
dynamic integration and the shell/post handoff.

Read the [LUT sky and aerial-perspective entry](examples/lut-aerial-perspective/atmosphere-effect.js)
and its `source/` modules for the SkyMaterial, SkyLightProbe,
SunDirectionalLight, AerialPerspectiveEffect, precomputed-texture loader,
sun/moon direction, lens flare, tone mapping, and dithering path used by the
LUT example.

## Required outputs

- sky radiance;
- sun transmittance/color;
- segment transmittance from camera to visible surface;
- segment inscattering;
- optional sky irradiance for materials;
- explicit scale conversion between world units and atmosphere units.

## Failure conditions

- sky and terrain haze use different sun directions or coefficients;
- the atmosphere is a uniformly transparent sphere;
- camera altitude is measured in a local flat frame during orbital motion;
- scene depth is treated as linear when it is not;
- exposure is used to hide incorrect radiance scale;
- atmosphere fades abruptly at shell entry.

## Routing boundary

This skill owns molecular/aerosol sky scattering and surface-segment aerial
perspective. Use `$threejs-volumetric-clouds` for weather-shaped cloud density,
temporal cloud reconstruction, and cloud shadows. Use
`$threejs-procedural-vfx` for emissive aurora curtain volumes and their
perspective/equirectangular radiance materials, and for standalone filmic HDR
lens-flare compositors. Keep the LUT example's lens flare here when it remains
one stage in the sky-scattering and aerial-perspective composition.
