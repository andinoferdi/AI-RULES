---
name: threejs-game-director
description: Entrypoint for building, upgrading, and finishing Three.js browser games. Routes work across the sibling threejs-* skills for gameplay, graphics, UI, 3D/image/audio asset generation, debugging, and release. Use for any request to build, upgrade, polish, or ship a Three.js game as a whole, at any scope from a small arcade prototype to a premium release.
---

# Three.js Game Director

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

Coordinate the domain production outcome: a playable loop first, then the visual and interface depth the request actually asked for, then browser evidence that it works.

## Scope

The user's own words set the bar. "Make a small arcade game" is not a request for the full premium pipeline — build the good version of what was asked and stop. "Premium", "AAA", "polished", "high-fidelity", "showcase", "release-ready", or "less basic" *is* that request, and at that bar a first playable slice is not done. "Less basic" specifically means the current visual level was rejected; treat it as the premium bar.

The user's scope, art style, constraints, and prior decisions override skill defaults. A narrow edit to a premium game remains a narrow edit. Make routine implementation calls yourself and complete authorized work before seeking a decision that only affects a later step. Ask only when a missing choice materially changes the requested result; continue independent work meanwhile. Until the requested bar is met, don't end a turn with a summary that announces the next step, an offer to continue, or a list of decisions that don't block the work; take the next step instead. End the turn when the work is done, or when only the user can unblock it.

## Working style

Say in one sentence what you're about to do before your first tool call. While working, give a short update when you finish a phase, find something important, or change direction. Lead the final response with the outcome.

Keep shared interfaces, integration and verification in the existing host task. Delegate only when the user or applicable project rules explicitly authorize it.

Report what you ran and what you saw. If you couldn't run something, say that instead.

## Sibling skills

Use the actual loaded skill directory as `<director-skill-dir>`. Resolve siblings through `../<skill>/SKILL.md` there. If absent, use the runner's discovered skill path, then a matching repo `skills/` directory or the active runner's install location (`~/.agents/skills` for Codex, `~/.claude/skills` for Claude Code, legacy `~/.codex/skills` last). Resolve references relative to the selected skill; avoid mixing installed versions.

| Phase | Skill |
| --- | --- |
| Design brief, core loop, levels, entities, input, camera, physics, feel | `threejs-gameplay-systems` |
| Models, materials, shaders, VFX, lighting, render budget, scorecard | `threejs-aaa-graphics-builder` |
| HUD, menus, overlays, responsive and touch UI | `threejs-game-ui-designer` |
| Blank canvas, render/runtime bugs, mobile input, profiling | `threejs-debug-profiler` |
| Browser QA, screenshots, canvas pixels, bot playtest, production build | `threejs-qa-release` |
| Characters, vehicles, weapons, buildings, rigs, animation | `threejs-3d-generator` |
| Concepts, textures, skies, logos, icons, GUI art, image-to-3D inputs | `threejs-image-generator` |
| SFX, music, ambience, UI sounds, announcer and dialogue | `threejs-audio-generator` |

For complete games and broad upgrades, select only specialists addressing a current unresolved need and activate them through the permitted host mechanism at phase entry. Read each phase's required references at phase entry. For narrow edits, load the affected specialists and references, preserving unrelated systems. Record actual loaded resources when reporting skill use; a phase label is not a skill invocation.

## Continuity and early quality

Start broad builds with the gameplay design brief, core-loop contract, and level plan. Define art direction, camera scale, and hero/readability targets early. Launch useful asset jobs while implementing the loop, then assess a representative playable scene with the real assets before multiplying levels, waves, or enemy variants. Inspect concepts and generated model previews before their dependent generation or rigging stages.

For substantial tasks update the existing Andino execution plan or normal host task record with intent, decisions, completed work, pending provider task IDs and remaining defects. Do not create a second progress checkpoint. Preserve completed assets and reconcile pending jobs after interruption.

Use available background tool sessions or submit/status/download commands to keep independent work moving.

## The bar for premium work

Every visible surface that exists in the design is authored, not just the hero: player, obstacles and enemies, interactables, ground and world kit, HUD and menu states, lighting and materials, feel, and target-device performance. Unrefined primitives, empty arenas, box skylines, generic stat-card HUDs, and glow-or-fog-only detail are prototype placeholders unless the user explicitly chose that style. Interpret the scorecard through the genre rather than adding unrelated content.

Score the result with the 10-category scorecard in `threejs-aaa-graphics-builder/references/visual-scorecard.md`, using its anchors and the inspector's measured metrics rather than a personal rubric. Premium means no category below 2 and an average of at least 2.3.

## Asset sourcing

```bash
bash <director-skill-dir>/scripts/probe_asset_credentials.sh
```

When external generation is in scope, run it before assuming anything about keys. It sources the user's shell profile, which the agent process usually does not inherit, and prints `KEY=SET|MISSING` for all three providers. Explicitly procedural or no-external-service work does not need a credential probe.

With keys set, premium hero surfaces get generated assets: player, boss, creature, vehicle, ship, weapon, signature building. Respect an explicit procedural-only style or external-generation restriction. Procedural kits handle repeated props, decals, collision proxies, and instanced volume. Premium active gameplay includes event-driven audio.

Read `references/asset-recovery.md` when sourcing external assets or recovering a job; it classifies each failure and says when a local fallback is allowed. Continue independent work meanwhile.

## Verification ownership

The lead consolidates specialist results into one check set appropriate to the change. Full games need production build, real-input progression and retry, target-viewport captures, renderer diagnostics, and the premium scorecard when requested. Small edits need affected behavior/layout checks. Repeat checks only after relevant changes, failures, or unresolved concerns. For animated work include motion captures covering locomotion, transitions, and contact timing, not only stills.

## Getting started and checking output

```bash
python3 <threejs-gameplay-systems-skill-dir>/scripts/create_threejs_game.py ./my-game
node <threejs-qa-release-skill-dir>/scripts/inspect-threejs-canvas.mjs --manifest artifacts/evidence.json --url http://127.0.0.1:5188
python3 <director-skill-dir>/scripts/check_evidence.py ./my-game --manifest artifacts/evidence.json
```

Generated games carry their own `npm run inspect:canvas` and `npm run verify:visual`. Before capturing, read `references/evidence-manifest.md` and declare the expected viewport/state pairs for this pass. The checker verifies only that set and its run ID. Its result establishes artifact coverage, not aesthetic quality or gameplay correctness. When maintaining the pack itself, use `references/workflow-evaluations.md` for behavioral comparisons.

## Final response

Lead with what was built, whether it works, the local URL and controls, and remaining limitations. For substantial builds put the design artifacts, asset task IDs/paths, captures and motion evidence, renderer/physics metrics, tests, and scorecard in `artifacts/final-evidence.md` and link it. For narrow edits report only affected behavior and checks. Describe what ran and was observed; do not substitute a completion claim for missing evidence.
