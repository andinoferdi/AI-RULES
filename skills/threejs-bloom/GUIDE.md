---
name: threejs-bloom
description: Implement production bloom in advanced Three.js scenes. Use for HDR signal ordering, bloom-node controls, dual selective bloom with guaranteed material restoration, scene-relative emissive hierarchy, and effect-isolation diagnostics.
---

# Bloom

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

Bloom is a camera/display response to bright HDR signal. Establish scene exposure and emissive luminance before tuning blur.

## Workflow

1. Inspect pre-tone-map luminance.
2. Choose which scene values should bloom.
3. Choose a single-node or dual selective-render ownership model.
4. Calibrate threshold, radius, smooth width, and strength in HDR.
5. Restore all substituted materials transactionally for selective passes.
6. Composite before exposure/tone mapping.
7. Validate base, contribution, and final views.

Read [references/hdr-bloom-system.md](references/hdr-bloom-system.md) for the
HDR ordering, dual selective-bloom transaction, compact emissive hierarchy,
and the costs and limits of each ownership model.

Apply the material substitution/restoration ownership pattern in the
reference before adding selective bloom to a composed scene.

## Failure conditions

- bloom creates the only visible form of an effect;
- all bright materials share one arbitrary emission multiplier;
- threshold is tuned after tone mapping;
- selective bloom requires mutating scene materials every frame without restoration guarantees;
- transparent particles disappear from extraction because pass ownership is unclear;
- bloom radius changes wildly with resolution;
- highlights become gray because energy is clamped too early.

## Routing boundary

Use `$threejs-exposure-color-grading` for metering, adaptation, tone mapping,
and LUTs. Load `$threejs-image-pipeline` only when bloom must be composed with
several shared image-space systems. A per-pixel ray integrator that owns its own
reduced-resolution target and accumulation history keeps its bloom internal;
route that to `$threejs-raymarched-space-effects`.
