---
name: threejs-skills
description: Use for Three.js, WebGL or WebGPU 3D work - photoreal or stylized scenes, open ocean and water, sky and sunlight, scanned textures and models, materials, shaders, lighting, animation, geometry, interaction, games and particle effects - or when a bundled threejs-* or nixie-fx-* method is named. Excludes ordinary 2D frontend work and general task orchestration.
---

# Three.js Skills

One installed skill with 57 internal methods at `skills/<method-id>/GUIDE.md`.
They are resources of this skill, not separate native skills. "Use threejs-skills"
selects methods from the request; "threejs-skills, specifically threejs-open-ocean"
or `/threejs-skills threejs-open-ocean` names one, and a named relevant method is
always loaded.

## When to use

- A 3D scene, canvas or game built with Three.js on WebGL or WebGPU, including
  making it look realistic, premium or less basic.
- A request that names a bundled method.
- Not for 2D DOM or CSS work and charts. For a failure of unknown cause, find the
  cause with the host's debugging method first, then load the method the evidence
  points to.

## Ownership

When Andino Workflow is active it owns the lifecycle, the single plan, checkpoints,
handoff and DONE. This skill supplies method selection and domain methods inside
that task. Focus owns communication; Search First owns solution and API research.
Without Andino use the host's normal task context. Paid services, credentials,
downloads, package installs, external writes and publication still need the task's
authorization. Rendering and performance claims need observed evidence.

## Select methods

1. Decide the target before any visual work. **Stylized** means code-made forms with
   procedural or painted materials. **Photoreal** means captured data: CC0 scanned
   textures and models and an HDR or physically based sky. If the request does not
   settle it, ask one question and state the consequence: code-only work tops out at
   stylized, photoreal needs captured assets. Record the answer.
2. Note the project's renderer (`WebGLRenderer` or `WebGPURenderer`). A method
   marked WebGPU needs WebGPU; on a WebGL project take the WebGL method in its row.
3. Take the bundle for the outcome from this table, then add single methods for the
   remaining needs from [the method index](references/specialists.md). Load methods
   when their stage starts, not all at once.

| Outcome | Load | Renderer |
| --- | --- | --- |
| Photoreal environment, "make it realistic", reference matching, look upgrade | `threejs-realism-director` first; it names each stage's methods | any |
| Open sea with a horizon, boats, wakes, creeks | `threejs-open-ocean` | WebGL module |
| FFT ocean cascades, coastal breakers, beach swash, wet sand | `threejs-spectral-ocean` | WebGPU/TSL |
| Harbour or canal water, reflections of quays, rain rings | `threejs-harbour-water` | WebGL |
| Pools, bounded shallow water, caustics, object ripples | `threejs-water-optics` | any |
| Underwater light shafts and caustics | `threejs-underwater-light` | WebGL |
| Sky, horizon, sun disc, environment lighting | `threejs-sky-background`; planetary scattering: `threejs-atmosphere-aerial-perspective` | any |
| Sun shafts through foliage or roofs | `threejs-sky-rays` | any |
| Volumetric clouds and cloud shadows | `threejs-volumetric-clouds` | any |
| Scanned or high-resolution PBR textures | `threejs-hires-textures` | any |
| Detailed hero models and LODs | `threejs-high-poly-models`; code-built hard surfaces: `threejs-procedural-geometry` | any |
| Wood, metal, cloth or paper that holds up close | `threejs-crafted-materials` | WebGL |
| Terrain fields, vegetation, buildings from code | `threejs-procedural-fields`, `threejs-procedural-vegetation`, `threejs-procedural-architecture` | see guide |
| Walkable painterly-real environment | `threejs-painterly-realism` | any |
| Light an interior and score the frame | `threejs-lighting-scorecard` | WebGL |
| Sharp output on HiDPI screens | `threejs-retina-resolution` | any |
| Tone mapping, exposure, bloom, AO, pass order | `threejs-exposure-color-grading`, `threejs-bloom`, `threejs-screen-space-ambient-occlusion`, `threejs-image-pipeline` | see guide |
| Shadows over large worlds | `threejs-shadow-systems` | see guide |
| A whole browser game | `threejs-game-director` | any |
| Premium graphics pass on a game | `threejs-aaa-graphics-builder` | any |
| NixieFX particle effects | `nixie-fx-authoring`, `nixie-fx-runtime` | any |
| One API topic: scene setup, shaders, lighting, materials, geometry, textures, loaders, animation, interaction, post-processing | the matching guide (`threejs-fundamentals`, `threejs-shaders`, `threejs-lighting`, `threejs-materials`, `threejs-geometry`, `threejs-textures`, `threejs-loaders`, `threejs-animation`, `threejs-interaction`, `threejs-postprocessing`) | API reference, not a look recipe |

4. Read each selected GUIDE.md in full before writing code, then open the modules,
   examples and references it names for the current stage. When a method ships a
   working module, such as `skills/threejs-open-ocean/assets/ocean.mjs`, adapt that
   module instead of re-implementing its technique.

## Selection record

Before the first code change, and again whenever the stage changes, write this
block in your notes or reply:

```text
Three.js selection
Target: stylized | photoreal (confirmed by user | stated in request | assumed: <reason>)
Renderer: WebGL | WebGPU
Stage: <current stage>
Selected: <method-id> - read skills/<method-id>/GUIDE.md; opened <module or reference paths>
Not needed: <nearby method-id> - <one-line reason>
```

List a method under Selected only after its guide was read in full and its
technique or module is being applied. Loading a guide is ACTIVE; USED needs that
application. Unselected methods are NOT_NEEDED.

## Load the right reference

- [Method index](references/specialists.md): every method with its selection
  description.
- Resolve paths relative to this installed folder and read them through the host's
  authorized file tools after invoking this skill. Never require a native
  `$threejs-...` registration. A missing or restricted resource is UNAVAILABLE: say
  so and use an honest fallback, never an alternate denied copy.

## Output contract

Return the selection record for each stage, the files changed, fixed-frame
screenshots or other observed evidence for visual claims, draw calls, triangles and
frame time on named hardware for performance claims, and what still looks wrong.
Static review does not verify rendering. Finish on a rendered frame inspected for
black, NaN or clipped pixels; edits that were never re-rendered do not count.

## Provenance

Methods come from the maintainer's collection and the upstream sources named in
each method's notices. Eleven methods are adapted from MengTo/Skills (MIT); each
carries `references/legal/mengto-skills-license.md`. See [README](README.md).
