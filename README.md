# Three.js Skills for AI-RULES

One installable family containing all 45 original Three.js/NixieFX methods and
supporting resources. Use for scene/rendering/game/particle needs, not ordinary
frontend work. Andino owns lifecycle when active; Focus controls communication.

## Installation

Requirements: Python 3.11+, Git, and an installed agent for CLI setup. Install the
CLI from `main` first, in your chosen Python environment:

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES
python -m pip install .
```

Select only **Three.js Skills** in Custom, or select **Three.js Development** for
the family plus Andino Workflow, Focus and Search First (four installed directories).

```sh
ai-rules setup --host codex --capability threejs-skills --scope project --project-root . --source latest
ai-rules setup --host codex --profile threejs --scope project --project-root . --source latest
ai-rules update --host codex --capability threejs-skills --scope project --project-root . --source latest
```

The first two commands are alternatives: install the standalone family or the
profile. Replace `codex` with `claude-code`, `opencode`, `antigravity-cli` or
`antigravity-ide` as needed. Preview with `--dry-run --non-interactive`. The family
requires no sibling skill; the profile supplies Andino and its dependencies.

Bundled distributions use the pinned family revision; latest resolves its branch.
Select `--source bundled` explicitly to use the frozen manifest without a freshness check.
Use the same host/scope when updating. Existing staging, verification, backup and
rollback apply to the entire directory. Modified or unrecognized targets need
explicit conflict review. Old separately installed specialist directories are not
automatically removed or overwritten; preserve personal edits before any cleanup.

## Layout and use

`<host-skill-root>/threejs-skills/SKILL.md` is the only native entrypoint.
`skills/<method-id>/GUIDE.md` contains each original method, with references,
scripts, examples, assets and license notices beside it. The original SKILL.md
content is preserved as GUIDE.md with integration boundaries. Nothing requires
45 separately installed skill directories or commands. All resources ship together.
See [SKILL.md](SKILL.md) and [the method index](references/specialists.md).

Say "use andino-workflow and threejs-skills" for selection from the prompt, or
"use threejs-skills, specifically threejs-shaders" to name one method. Invoke the
family through the host's native mechanism and load only the relevant authorized
guides. Do not claim that internal methods are separately registered native skills.

- Codex: `$threejs-skills create a shader effect using threejs-shaders`
- Claude Code: `/threejs-skills create a shader effect using threejs-shaders`
- OpenCode and Antigravity: ask the agent to use `threejs-skills` through its supported mechanism.

Andino retains its single plan, checkpoints, handoff and completion. Standalone
family use follows the existing host context, with no new general lifecycle.

Codex uses .agents/skills; Claude Code .claude/skills. Other hosts use the existing
AI-RULES catalog adapters. Refresh session discovery after installation. Installer
path support does not establish live cross-host behavior. Never bypass restrictions
with alternate source reads. Missing/denied methods require honest fallback.

## Verification, dependencies and provenance

After reloading the host, request a named method and check that the family loads
that guide and produces a task result. An ordinary text-only edit should need no
Three.js guide. These manual smoke cases are not a claim of observed live use.

Validate paths, metadata, relative references, binary signatures and the original
inventory in main. Verify actual host family discovery and selective guide use
separately; structural checks do not prove rendering or API compatibility. Browser,
interaction and performance claims require observed runtime evidence. Andino UI
acceptance retains 360/768/1440 px screenshots when applicable.

Inspect actual Three.js/WebGL/WebGPU/TSL and NixieFX versions before using examples.
Optional generators use Tripo, Gemini or ElevenLabs and user-provided credentials.
Installation calls none of those services and installs no npm dependencies. Paid
calls, delegation and publication require applicable task authorization.

The maintainer attests original collection authorship. Embedded MIT, CC0 and GPL
notices/full texts remain intact; no collection-wide license is invented. This is
not independent verification of every resource origin. See main's provenance record.

[Inventory and evidence](https://github.com/andinoferdi/AI-RULES/tree/main/docs/threejs)
