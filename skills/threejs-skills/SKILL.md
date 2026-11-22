---
name: threejs-skills
description: Apply the bundled Three.js and NixieFX specialist methods for 3D scenes, shaders, lighting, animation, geometry, interactions, games and particle effects. Use for an explicit specialist name or select relevant methods from the prompt. Excludes ordinary frontend work and general task orchestration.
---

# Three.js Skills

This is one installed skill containing 45 domain methods. They are internal
resources, not separately registered native skills or installation dependencies.
The user can say "use andino-workflow and threejs-skills" for automatic selection,
or "use threejs-skills, specifically threejs-shaders" to choose a method explicitly.

## Select and apply

1. Identify the actual current need and any explicitly requested method. Honor an
   explicit relevant choice. Ordinary frontend work needs no Three.js method.
   For an unknown-cause failure use the host's debugging method first, then add
   a domain method when evidence identifies its need; do not guess shader/light.
2. For a narrow need read the corresponding local guide directly:
   shaders -> `skills/threejs-shaders/GUIDE.md`; lighting ->
   `skills/threejs-lighting/GUIDE.md`; keyframe/skeletal animation ->
   `skills/threejs-animation/GUIDE.md`; materials ->
   `skills/threejs-materials/GUIDE.md`; geometry ->
   `skills/threejs-geometry/GUIDE.md`; picking/input ->
   `skills/threejs-interaction/GUIDE.md`.
   For other needs consult [the method index](references/specialists.md) and load
   the minimum distinct guides needed now. A shader-and-light request needs those
   two methods, not all 45. Game Director is only for game-wide production;
   the optional domain advisor supports complex technical selection, not a second
   dispatcher or bootstrap chain. Do not invoke them recursively.
3. Resolve guide paths relative to this installed family directory, read each
   selected GUIDE.md through an authorized resource-reading tool and apply its
   technical method. Resolve that guide's examples/references/scripts relative to
   its own directory. Never require a native `$threejs-shaders` registration.
   If a sibling method is recommended, use the same need/permission check first.
4. Return the domain result, evidence, limitations and next recommendation. Loading
   is ACTIVE; USED also requires meaningful application, not just naming a method.
   Identify the actual guide when relevant to evidence. Unselected methods are
   NOT_NEEDED. Missing or restricted resources are UNAVAILABLE: use an honest
   native fallback without claiming their use or reading alternate denied copies.

Invoke this family through the actual host skill mechanism before loading its
resources. Permission to read bundled guides is subordinate to host/project rules;
this is not a bypass of a denied family, method or resource. Discovery, availability,
permission, activation and use remain distinct. Reassess after changed needs/resume;
release irrelevant methods rather than accumulating the whole collection.

## Ownership and limits

With Andino active it owns lifecycle, routing, one plan/checkpoint, handoff and DONE.
This family supplies domain selection and methods within that task. Focus controls
communication; Search First handles relevant solution/version research. Without
Andino use the host's existing task context. No new plan, checkpoint or delegation
is implied. Paid services, credentials, external writes and publication still need
applicable task authorization. Installation makes no API calls or npm installs.
Rendering, performance and browser interaction claims require observed evidence;
static review does not verify rendering. Read [the package guide](README.md).
