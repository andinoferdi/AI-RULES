---
name: threejs-water-optics
description: Build production analytic and bounded water in Three.js. Use for photoreal shallow water with gravity-capillary FFT waves, dispersive caustics and diffraction glare, shared multi-wave displacement and normals, bounded RGBA heightfield pool simulation, local drops, object-driven ripples, differential-area caustics, ray-traced pool/water/sphere volume optics, derivative-filtered normal bands, analytic sky reflection, side-aware Fresnel, heuristic screen refraction, Beer-Lambert absorption, and crest foam.
---

# Water Optics

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

Treat water as geometry motion, surface orientation, and a participating optical layer. A blue transparent material is not a water system.

This skill contains exemplary examples and assets beyond descriptive guidance,
they're worth studying, referencing, or even copying. Use them sufficiently
when relevant and do NOT blindly skip them.

For large seas with spectral cascades, coastal breakers or camera-medium
crossings, use `$threejs-spectral-ocean`. This skill also owns the air-side
`photoreal-water` shallow-water compositor.

## Analytic surface build order

1. Define wave bands and evaluate displacement.
2. Derive the normal analytically from the same waves.
3. Choose displaced geometry or explicitly normal-only water.
4. Establish scene-color ownership for heuristic refraction.
5. Declare whether absorption uses true depth or a fallback path-length estimate.
6. Blend analytic reflection/refraction through side-aware Fresnel.
7. Derive foam and glints from the shared wave response.
8. Filter unresolved normal bands from derivatives.

Read [references/water-surface-system.md](references/water-surface-system.md)
for the authored displacement/normal contract, optical hierarchy, side-aware
refraction, absorption fallback, and diagnostic channels.

Read the
[interactive pool volume implementation](examples/interactive-pool-volume/water-volume-system.js)
for bounded RGBA height/velocity/normal simulation, local drops, moving-sphere
displacement suitable for draggable objects, differential-area caustics, and
in-shader pool/water/sphere ray tracing against the pool bounds and sphere.

Read the [photoreal water implementation](examples/photoreal-water/photoreal-water.js)
for gravity-capillary FFT waves, touch ripples, RGB caustics, refracted pebble-bed
radiance and aperture diffraction glare. Read
[references/photoreal-water.md](references/photoreal-water.md) for its pass,
coordinate, filtering, integration and diagnostic contracts.

## Failure conditions

- normal texture motion does not agree with displaced crests;
- heuristic refraction can sample foreground objects but the limitation is undisclosed;
- fallback path length is presented as reconstructed scene thickness;
- bounded pool caustics are a decorative projection detached from simulated
  height normals;
- micro-waves alias into sparkling noise;
- foam is a scrolling texture unrelated to the shared crest metric;
- Fresnel is replaced by constant opacity;
- reflection, refraction, and transparency are all added without energy control.

## Routing boundary

Use `$threejs-spectral-ocean` for large spectral cascades, Jacobian breaking,
persistent ocean foam and camera-medium crossings. The `photoreal-water`
example uses an FFT patch for shallow-water optics viewed from air; it does
not implement underwater viewing. The analytic screen-refraction recipe also
assumes an air-side camera above a bounded volume. Use
`$threejs-precipitation-surfaces` for rain-driven puddle wetness, ripple masks,
and weather-coupled splashes on ground surfaces. This skill owns authored
analytic waves, bounded heightfield simulation, ray-traced pool-volume optics,
and bounded-water optics.
