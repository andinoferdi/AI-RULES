# AI Codebase Rescue

An evidence-first method for stabilizing fragile codebases and bounded
subsystems. Choose KEEP, REFACTOR, REMAKE, REMOVE or INVESTIGATE from
engineering evidence. Preserve contracts and establish regression protection;
AI authorship alone never justifies a rewrite.

Start with [the skill](SKILL.md). Rescue works standalone using the host task
context, and follows the existing Andino plan when Andino is active. Routine
local bugs, cosmetic cleanup and ordinary features use the normal workflow.
[Validation scenarios](references/validation-scenarios.md) describe expected
behavior for reviewers; they are not automatically loaded during a rescue.

## Install

Clone this branch into a directory named `ai-codebase-rescue` under your agent's skill root.
The commands below work in PowerShell and Bash; `$HOME` is your user home.
Use a destination that does not already contain another installation.

```sh
git clone --depth 1 --single-branch --branch ai-codebase-rescue https://github.com/andinoferdi/AI-RULES.git "$HOME/.agents/skills/ai-codebase-rescue"
```

That destination works globally for Codex and OpenCode. For another host or
project scope, replace the destination using this table, appending `/ai-codebase-rescue`.
Project paths are relative to the target project's root.

| Agent | Global skill root | Project skill root |
| --- | --- | --- |
| Codex | `~/.agents/skills` | `.agents/skills` |
| OpenCode | `~/.config/opencode/skills`; compatible `~/.agents/skills`, `~/.claude/skills` | `.opencode/skills`; compatible `.agents/skills`, `.claude/skills` |
| Claude Code | `~/.claude/skills` | `.claude/skills` |
| Antigravity 2.0 | `~/.gemini/config/skills` | `.agents/skills` |
| Antigravity IDE | `~/.gemini/config/skills` | `.agents/skills` |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills` | `.agents/skills` |

For example, Claude Code globally:

```sh
git clone --depth 1 --single-branch --branch ai-codebase-rescue https://github.com/andinoferdi/AI-RULES.git "$HOME/.claude/skills/ai-codebase-rescue"
```

Antigravity IDE also documents the legacy global path
`~/.gemini/antigravity/skills`. Prefer the location for your installed surface.
Other agents can use this directory when they support Agent Skills; use their
documented discovery path rather than assuming every agent shares these roots.
Keep one discoverable copy per skill unless an override is intentional. OpenCode
V2 uses path-derived IDs and later-source precedence; Claude has scope precedence;
Codex can show both same-name skills. Check the loaded path rather than assuming
the newest copy wins. These are different host rules; see the linked sources below.
Use ordinary directories for portable installation; Windows junction behavior
has not been verified across these hosts.

Install the **whole folder**, including `references/`. No build, package manager,
sync script, MCP service or personal host configuration is required by this skill.
For team distribution in a project, commit the package files as ordinary files or
use a deliberately managed submodule; a nested clone alone is not a complete
parent-repository distribution. Do not include credentials or personal configs.

## Use

- Codex CLI/IDE: select the skill with `$` or `/skills`, for example
  `$ai-codebase-rescue investigate repeated checkout regressions within the payment module`.
- Claude Code: `/ai-codebase-rescue investigate repeated checkout regressions within the payment module`.
- Antigravity 2.0/CLI: `/ai-codebase-rescue investigate repeated checkout regressions within the payment module`; in the IDE, check Customizations
  and mention the skill by name.
- OpenCode: ask the agent to use `ai-codebase-rescue` for the task; its native skill tool
  loads the matching ID, subject to configured permissions.

Implicit selection depends on the task, host and invocation policy. Installation
does not force activation or authorize commits, pushes, merges, publication,
deployment, live-data changes or unrelated external actions.

## Combine the two skills

Install the companion branch into a **separate sibling folder** under the same
host skill root:

```sh
git clone --depth 1 --single-branch --branch andino-workflow https://github.com/andinoferdi/AI-RULES.git "$HOME/.agents/skills/andino-workflow"
```

Use the appropriate root from the table for Claude Code or Antigravity. The result
is two packages: `andino-workflow/` and `ai-codebase-rescue/`.

Andino coordinates task state and may route eligible rescue work to Rescue.
Rescue supplies diagnosis, dispositions, remediation and verification evidence.
When Andino is active, its plan remains the single lifecycle owner. Without
Andino, Rescue uses the host's normal task context. Merely installing both does
not activate both. Neither package bundles or automatically installs the other.

Example request: "Use andino-workflow to coordinate this task and
ai-codebase-rescue to investigate repeated regressions in the checkout module."

## Update or switch branches

For a clean clone on this branch:

```sh
git -C "$HOME/.agents/skills/ai-codebase-rescue" status --short
git -C "$HOME/.agents/skills/ai-codebase-rescue" pull --ff-only
```

Resolve or preserve local edits before updating. If an older installation is a
copied/generated folder instead of a Git clone, preserve it outside every host's
skill roots, then replace it with a fresh clone. Do not blindly overwrite local
edits or leave a second discoverable backup. Old `.andino-generated.json` markers
belong to the retired sync workflow; do not mix that workflow with these clones.

Use separate clones to run both skills together. Branch switching is for a clean
development checkout: a single checkout exposes only one branch at a time, and a
single-branch clone initially fetches only the selected branch. An installed
folder must retain the name of the skill it contains.

## Verify your installation

Confirm `ai-codebase-rescue/SKILL.md` and every linked file in `references/`
exist. Check the actual loaded path and use the host's documented invocation above.
Codex detects updates automatically (restart if missing); Claude watches SKILL.md
in existing roots (restart for a newly created root). Antigravity documents discovery
at conversation start. No universal hot-refresh promise is made for OpenCode or IDEs.

Manual smoke cases, in a disposable context:

| Case | Request | Expected decision |
| --- | --- | --- |
| Positive | Investigate reproduced repeated regressions in a bounded subsystem. | Establish contracts and evidence before selecting a disposition. |
| Negative | Fix one isolated bug, or assess healthy code described only as AI-written. | Use ordinary local work; authorship alone must not trigger rescue or REMAKE. |

For selection checks, present the request without explicitly forcing the skill.
For instruction checks, explicitly invoke it and inspect its actual decisions.
Record host/version, skill commit, loaded path, input, observed actions and limits.
These are proposed checks, not cross-host PASS claims. Package validation is
STRUCTURAL VERIFIED only for the tested revision; documented host features are
DOCUMENTATION VERIFIED. LIVE HOST VERIFIED requires observed host execution;
unrun checks remain NOT VERIFIED. Historical evidence lives on main.

## Package and sources

This branch contains only `SKILL.md`, `references/` and this README. The
[WebBased branch](https://github.com/andinoferdi/AI-RULES/tree/WebBased) retains
web/chat rules and project templates. Development plans, monorepo adapter scripts
and historical evaluation reports are outside the runtime package. Edit this
branch's root files as the canonical source. The
[main quality plane](https://github.com/andinoferdi/AI-RULES/tree/main) owns
validators, tests, evaluation cases, CI and family audit evidence; none is installed
as runtime methodology.

Installation and discovery guidance checked against official documentation on 2026-09-21:
[Codex skills](https://learn.chatgpt.com/docs/build-skills),
[OpenCode V2 skills](https://opencode.ai/v2/docs/skills)
([V1 differences](https://opencode.ai/docs/skills/)),
[Claude Code skills](https://code.claude.com/docs/en/skills), and
[Antigravity skills by surface](https://antigravity.google/docs/skills?tab=ide).
These sources establish folder conventions, not identical runtime behavior.
