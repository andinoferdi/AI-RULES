---
name: threejs-interactive-topography
description: Create thin elevation contours for a historical map and a raised relief view with interactive years, localized hover highlights and a press-triggered seismic particle wave. Use for timeline atlases and topographic section backgrounds.
---

# Interactive topography

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

Saltmere uses contours in two ways. The history map locates years along a route. Field Access shows the landform in relief and sends a disturbance across the background on press. Build both from one reproducible height field. Switch views in the [runnable atlas](examples/index.html).

## Draw the land once

- Define a height function over map coordinates. Combine a few broad ridges, inlets and valleys before adding fine displacement. Sample a regular grid and cache it. When working with measured elevations, preserve the units and state the actual interval. Use illustrative labels for generated terrain.
- For a vector or Canvas implementation, intersect each triangle of the grid with equal elevation levels. Linearly interpolate each crossing along its edge. Triangulating every cell consistently avoids ambiguous four-edge saddle cases. Batch segments by elevation and keep the lines continuous across adjacent faces.
- For a GPU implementation, compute `level = elevation/interval`, `d = abs(fract(level + 0.5) - 0.5)`. Use screen-space derivatives such as `fwidth(level)` to antialias the stroke. Start near 0.5–0.7 CSS pixels for minor contours and 0.9–1.1 for every fifth index contour. Calibrate at both 1× and 2× pixel density.

## History

Use a plan view. Keep routes, stations and year labels distinguishable from the minor contours. Drive the selected station, label emphasis and any descriptive copy from one index. Within a soft pointer radius, brighten existing lines or raise the field slightly, easing the effect back on exit. Provide keyboard-operable year buttons. Keep data labels aligned when the camera, aspect ratio or selection changes.

## Field Access

Project the same grid into a raised relief. Shade slopes with a low raking light and draw isolines from the same heights used for the mesh. Keep a quieter contour field visible across the surrounding section. If a callout sits over the map, let its links and controls receive normal input.

On a primary press, capture the origin in normalized section coordinates. Set the maximum radius to the distance to the farthest corner. Over roughly 1.5 seconds advance a wavefront past that corner. Each seeded background grain uses its distance from the origin to determine arrival time. Give it a short outward impulse at the crest and a smaller recoil immediately behind it. Fade the wake, clear the overlay, and settle at the original positions. A new press can restart the wave at its own origin. Cache the static map so a pulse only redraws the moving layer.

## Review

Test a press near a corner, selection by keyboard, an empty hover, resizing, and a second press during the wave. In reduced motion keep the map and year selection available with the pulse disabled. Contrast the lines at mobile and desktop sizes. [Original map and relief](https://threeui.com/saltmere)
