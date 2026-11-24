---
name: threejs-retina-resolution
description: Render a 3D canvas sharply on Retina and HiDPI displays, including explicit 200 percent resolution, synchronized renderer and post-processing sizes, correct pointer coordinates, and measured quality fallbacks. Use for blurry WebGL output, 2x rendering, high-resolution previews, and display-density changes.
---

# 3D Retina Resolution

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

Treat an explicit **200% rendering** request as two drawing-buffer pixels per CSS pixel in each dimension. A 1200 × 800 CSS canvas therefore uses a 2400 × 1600 drawing buffer, or four times the pixels of 100%. Layout and camera framing stay unchanged.

## Choose the scale deliberately

- **Fixed 200%:** effective pixel ratio is `2`, independent of device pixel ratio. This is the default when the user explicitly requests 200%.
- **Automatic Retina, capped at 2×:** effective ratio is `Math.min(window.devicePixelRatio || 1, 2)`. This can render at 1× on an ordinary display; label it Auto rather than claiming it always renders at 200%.
- **Relative to native resolution:** multiply native DPR only when the user explicitly wants that meaning. Native 2× multiplied by another 2 becomes 4× per dimension, or sixteen times the CSS pixel count.

Keep an explicit quality selection distinct from automatic adaptation. Inspect the project's renderer and post-processing architecture before changing sizing.

## Synchronize the rendering pipeline

Use CSS to size the canvas and its container, then measure the container in CSS pixels. In Three.js WebGL, one consistent convention is logical sizes plus pixel ratio:

```js
function resize3D(width, height, ratio = 2) {
  if (!Number.isFinite(width) || !Number.isFinite(height) || width <= 0 || height <= 0) return;
  if (!Number.isFinite(ratio) || ratio <= 0) throw new RangeError('Invalid render ratio');
  renderer.setPixelRatio(ratio);
  renderer.setSize(width, height, false); // CSS owns displayed dimensions
  camera.aspect = width / height;        // perspective camera
  camera.updateProjectionMatrix();
  if (composer) {
    composer.setPixelRatio(ratio);
    composer.setSize(width, height);     // logical pixels; do not multiply again
  }
  const physicalWidth = renderer.domElement.width;
  const physicalHeight = renderer.domElement.height;
  resizeCustomTargets(physicalWidth, physicalHeight);
}
```

The snippet assumes an existing `renderer`, perspective `camera`, optional `composer` (or `null`), and a `resizeCustomTargets` adapter supplied by the app. For an orthographic camera, update its bounds according to the existing framing policy instead of setting `aspect`.

The adapter updates only app-owned targets and uniforms; composer-managed passes already receive sizing through the composer. Set full-resolution depth/normal targets to physical dimensions. Size lower-resolution AO, bloom, or ray targets by their deliberate scale factors. Set sampling-resolution uniforms to the dimensions of the texture actually sampled, including reciprocal resolution where the shader expects it.

The renderer and composer each maintain their own pixel ratio. Updating only the canvas can leave a lower-resolution intermediate image stretched to a Retina output. Conversely, passing already doubled dimensions into a composer that also has DPR 2 allocates 4× dimensions. See the [renderer](https://threejs.org/docs/pages/WebGLRenderer.html) and [composer](https://threejs.org/docs/pages/EffectComposer.html) sizing APIs.

## Handle layout and display changes

Observe the canvas container with `ResizeObserver`, coalesce notifications, and resize only when dimensions or effective ratio change. Skip zero-sized hidden views and retry when they become visible. Re-evaluate native DPR on browser zoom or display changes in Auto mode, including when CSS dimensions remain unchanged. Recreate a resolution media-query listener after each DPR change if using that approach.

Use `canvas.getBoundingClientRect()` for pointer normalization: `(clientX - rect.left) / rect.width`, and likewise for Y. Raycasting uses normalized coordinates derived from CSS space, not drawing-buffer pixels. Convert to physical pixels separately only for APIs such as a pixel readback.

Retina output does not automatically improve a blurry texture, coarse model, shadow map, or low-resolution reflection. Check those sources independently. Avoid CSS scaling or `image-rendering: pixelated` as a substitute for the correct drawing buffer. Higher resolution and antialiasing solve related but different artifacts.

## Budget and fallback

Measure the scene at 1× and 2× with the same camera. Track frame time, target dimensions, allocation failures, and total passes. Check GPU limits before allocating exceptionally large targets, including maximum texture/renderbuffer dimensions and viewport limits.

Reduce optional post-effect resolution or samples before compromising a requested crisp main view. Auto mode may step down after sustained poor frame time and recover with hysteresis; do not resize every few frames. A fixed 200% selection should stay fixed unless a concrete hardware/allocation failure requires a visible fallback. Report the actual effective scale rather than displaying 200% while silently rendering lower.

Pause hidden views and render static scenes on demand. Under reduced motion, keep the sharp still image; reducing animation does not require reducing resolution. Dispose replaced render targets.

## Verify

- At fixed 200%, compare canvas CSS size with `canvas.width`/`canvas.height` and `renderer.getDrawingBufferSize()`; expect approximately 2× on each axis with integer rounding.
- Confirm full-resolution composer buffers match and any reduced-size passes are intentional.
- Resize wide ↔ narrow, hide/show the view, and test browser zoom or display changes in Auto mode.
- Check thin edges and detailed materials at the same apparent size; pointer selection and UI alignment must remain correct.
- Test on a DPR 1 display and a Retina display: Fixed 200% remains 2×; Auto follows its cap.

Read [references/links.md](references/links.md) for APIs and the reference project. Seijaku has several renderer quality caps and an adaptive main path; those values are context, not evidence that its main view already renders at fixed 200%.
