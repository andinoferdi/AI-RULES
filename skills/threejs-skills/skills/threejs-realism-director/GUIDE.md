---
name: threejs-realism-director
description: Direct photoreal or premium Three.js environments from target decision to scored frames. Use for "make it realistic", reference matching, look upgrades, open-sea or island scenes, scanned-asset pipelines and choosing each stage's methods.
---

# Three.js Realism Director

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

## The mechanism

Photoreal comes from captured data and one coherent light and colour pipeline,
judged on fixed frames. More shader effects on code-made forms do not get there.
Work the stages in order and write the family's selection record at each one.

## 1. Settle the target

Ask, when the request does not say: stylized (code-made forms, procedural or painted
materials) or photoreal (scanned textures and models, HDR or physical sky). Say the
consequence in one sentence: a "code-made, no imported textures or models" rule caps
the result at stylized premium, however good the shaders. Record the answer as
`Target:` in the selection record. Stop here until it is answered when the answer
changes the asset plan.

## 2. Tear down the reference

- **Live three.js page:** list what it loads (texture names, sizes and formats; mesh
  format and LOD files), its tone mapping and exposure, fog model, post passes and how
  the sky is drawn. Network requests and the bundle answer most of this.
- **Video or still:** read the palette, exposure, fog density with distance, horizon
  treatment, specular behaviour on water and foliage, and shadow softness.
- **No reference:** write the three fixed shots and the time of day instead.

Output a list of mechanisms to reproduce ("height fog into the sky's horizon colour",
"per-pixel Gerstner normals with footprint fade"), not effect names ("make it foggy").

## 3. Source captured assets

Follow [asset sourcing](references/asset-sourcing.md). Downloads and package
installs need the task's authorization; ask before fetching anything.

## 4. Build one light and colour pipeline

- Keep every colour uniform linear. Render the scene into a `HalfFloatType` target and
  tone-map once, at the end. Additive effects (glitter, shafts, bloom input) stay in
  linear HDR before that pass.
- Compare tone mappers (ACES Filmic, AgX, Neutral) on the same fixed frames at the same
  exposure, then pick one. Do not tune exposure on one shot only.
- Build the environment map (PMREM) from the scene's own sky so reflections and sky
  agree. Fog into the sky's horizon colour, not a flat fog colour.
- Light with one key (the sun) and low fill. A bright `AmbientLight` as the look fills
  every crevice and reads as CG.

## 5. Stage bundles

| Stage | Methods | Renderer |
| --- | --- | --- |
| Water | open sea `threejs-open-ocean`; harbour or canal `threejs-harbour-water`; pool or bounded `threejs-water-optics`; breakers and swash `threejs-spectral-ocean` | WebGL; WebGL; any; WebGPU |
| Sky and light | `threejs-sky-background`, `threejs-sky-rays`, `threejs-volumetric-clouds`; planetary scattering `threejs-atmosphere-aerial-perspective` | any |
| Ground and terrain | `threejs-hires-textures`, `threejs-procedural-fields` | any |
| Hero props and architecture | `threejs-high-poly-models`, `threejs-crafted-materials`, `threejs-procedural-architecture` | any |
| Vegetation | `threejs-procedural-vegetation` | see guide |
| Underwater | `threejs-underwater-light` | WebGL |
| Final image | `threejs-exposure-color-grading`, `threejs-bloom`, `threejs-screen-space-ambient-occlusion`, `threejs-retina-resolution` | see guide |
| Walkable painterly environment | `threejs-painterly-realism` | any |

When a method ships a working module, adapt that module (for example
`../threejs-open-ocean/assets/ocean.mjs`) instead of re-deriving its technique. Read
each selected guide in full before you write code for its stage.

## 6. Review on fixed frames

1. Freeze time and fix the camera, sun direction and exposure for at least three shots:
   low near the surface, mid on the subject, wide with the horizon.
2. Capture a baseline before changing anything and keep it.
3. Inspect every capture for render errors before judging the look: black or NaN pixels
   (dashed black lines, speckles, black wedges), clipped highlights wider than the sun's
   glitter path, and banding. NaN usually comes from `pow`, `sqrt`, `log` or
   `normalize` of a negative or zero value, or a division by a value that can reach
   zero: clamp the input first. Fix render errors before any further look change.
4. Change one physical cause at a time and compare at the same frames.
5. Score each shot with [the realism rubric](references/realism-rubric.md). Keep only
   changes the picture confirms; look at a 2x crop after any metric-driven change.
6. For a lit interior, use `threejs-lighting-scorecard` for the numbers.
7. Finish on a rendered, inspected frame. An edit you did not render and inspect is
   not done: render once more, or revert it before you stop.

## 7. Hold the frame budget

Set an absolute budget on named hardware (default: 16.7 ms per frame at 1440x900 on a
mid-range GPU) and measure it, before and after, on the same build. Report draw calls,
triangles and frame time. Load captured assets after the first frame, give scans a
low LOD, and instance repeated plants and rocks.

## Report

Return the selection record for each stage, rubric scores per shot before and after,
the budget numbers with the hardware named, and what still looks fake.
