# Three.js Skills for AI-RULES

A domain collection of 45 standalone Three.js and NixieFX specialists. This family
does not own a task lifecycle, general router, plan or DONE decision. Andino owns
those when active; Focus controls communication and Search First relevant research.
Use for real scene/rendering/game/particle needs; ordinary frontend work is excluded.

## Packages

The branch root is the family reading entrypoint. `entrypoint/` is its standalone
installable projection (identical SKILL.md and README.md); `skills/<name>/` holds
each original skill and all supporting files. The installer selects subpaths so
the family installation does not contain nested discoverable copies of specialists.
The installed shape is `<host-skill-root>/<name>/SKILL.md`, with support files
beside it. No installer source, tests or main quality artifacts ship on this branch.

## Install, update and discovery

After publication, use these existing CLI selections:

```sh
ai-rules setup --host codex --profile threejs --scope project --project-root . --source latest
ai-rules setup --host codex --capability threejs-shaders --scope project --project-root . --source latest
ai-rules setup --host codex --profile threejs --scope global --source bundled
ai-rules update --host codex --profile threejs --scope project --project-root . --source latest
```

Pass the required `--project-root PATH` for project scope. The profile includes all
45 members, this index, Andino, Focus and Search First. Individual specialists do
not require the lifecycle skills. Minimal and Engineering keep their existing sets.
Everything includes all first-party members when newly selected; existing locks
retain explicit targets unless the caller selects that expanded profile again.

Host mappings: Codex `.agents/skills` (project/global); Claude Code `.claude/skills`;
OpenCode `.agents/skills` project, `~/.config/opencode/skills` global; Antigravity CLI
`.agents/skills` project and `~/.gemini/antigravity-cli/skills` global; Antigravity IDE
`.agents/skills` project and `~/.gemini/config/skills` global. Installer mappings
are structural support, not live-host execution proof. All live Three.js host use
is NOT_VERIFIED until observed. Refresh discovery in the host's normal manner;
invoke exact installed names through permitted host controls. Never bypass a deny
or explicit-only setting with file reads. Avoid duplicate discoverable installations.

Latest uses one fetch per repository, identifies packages by branch/subpath, and
preserves edited/unrecognized targets. Bundled uses the release-pinned commit and
same subpath. Updates use existing staging, backup, verification and rollback.
Review conflicts before explicit repair; never overwrite personal edits blindly.

## Domain selection and evidence

Select only current needs: shaders, lighting, animation, materials, geometry and
interaction have their namesake specialists. Complex graphics may use the domain
advisor `threejs-skill-router`; game-wide production may use `threejs-game-director`.
Neither starts a second plan nor activates all siblings. Distinguish DISCOVERED,
AVAILABLE, INVOKABLE, ACTIVE, USED, UNAVAILABLE and NOT_NEEDED. Reassess after
requirements change and after resume; missing/denied skills use honest fallbacks.

Main's package validator checks metadata, regular files, safe paths, relative links
and binary signatures. Behavioral smoke: request one shader change, activate only
the relevant permitted specialist, apply its method and record output. Negative
smoke: unrelated frontend work selects none; an unavailable or denied specialist
must not be reported as used. Rendering/performance/interaction claims need actual
browser evidence. For UI acceptance under Andino inspect 360/768/1440 px captures.
Unit and structural tests are not live model-routing proof.

## Dependencies, provenance and limits

Examples span different Three.js/WebGL/WebGPU/TSL versions. Inspect project versions
and official documentation before use. NixieFX requires its actual public runtime
and selected renderer peer. Generator scripts use optional external Tripo, Gemini
and ElevenLabs services and user-provided credentials; installation makes no calls,
incurs no charges and installs no npm packages. Paid calls need task authorization.

Source is the user-supplied local collection; no upstream origin or blanket license
is asserted. Preserve included MIT, CC0 and GPL notices and full GPL texts. Some
code/assets have no explicit rights declaration: review the main inventory and
confirm distribution rights before publication. No remote readiness is claimed
for these unpublished local commits.

[Main quality contract](https://github.com/andinoferdi/AI-RULES/blob/main/docs/agent-skill-family-standard.md)
[Inventory and release evidence](https://github.com/andinoferdi/AI-RULES/tree/main/docs/threejs)
