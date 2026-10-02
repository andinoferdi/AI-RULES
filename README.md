# Andino Workflow

A portable problem-solving protocol for AI assistants and agents. It supports
development, troubleshooting, research, decision support, daily tasks and ordinary
conversation. It distinguishes the user's desired outcome from a proposed factual
diagnosis, gathers only decision-relevant evidence, and asks only about material
uncertainty that available context cannot resolve.

DIRECT, GROUNDED and INVESTIGATIVE describe how much reasoning and evidence the
current situation needs. Persistence is a separate choice: EPHEMERAL work needs
no plan; CHECKPOINTED work retains scope, evidence, state and a concrete next
action for continuation. LITE, STANDARD and DEEP describe that plan's density.

Start with [the skill](SKILL.md). Planning, handoff, anti-loop and routing
references are included. Specialist skills and memory/graph services are
optional; use available methods within native invocation permissions.

Andino knows a broad [capability registry](references/capability-registry.md), but
selects and loads only the minimum useful methods/instruments for the current
unresolved need. Evidence and task context guide selection, not keyword matching.
The registry covers individual Superpowers/Agent Skills, Ponytail, Claude-Mem,
UI/UX Pro Max, Taste, Cloner, Graphify, Anti-Slop and eight recommended MCP families.
It contains short contracts, not bundled third-party implementations or automatic
installation. [Coexistence](references/capability-coexistence.md) resolves competing
providers; [host invocation](references/invocation-adapter.md) separates discovered,
available, invokable, active and used capabilities. Installed does not mean used.
New evidence may change selection; stop calling a capability when its need ends.
Invocation depends on the actual host catalog, permissions and connected service.
Documentation or transport checks do not prove autonomous or cross-host use.

## Install

Clone this branch into a directory named `andino-workflow` under your agent's skill root.
The commands below work in PowerShell and Bash; `$HOME` is your user home.
Use a destination that does not already contain another installation.

```sh
git clone --depth 1 --single-branch --branch andino-workflow https://github.com/andinoferdi/AI-RULES.git "$HOME/.agents/skills/andino-workflow"
```

That destination works globally for Codex and OpenCode. For another host or
project scope, replace the destination using this table, appending `/andino-workflow`.
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
git clone --depth 1 --single-branch --branch andino-workflow https://github.com/andinoferdi/AI-RULES.git "$HOME/.claude/skills/andino-workflow"
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
  `$andino-workflow resume the existing task plan and check repository drift`.
- Claude Code: `/andino-workflow resume the existing task plan and check repository drift`.
- Antigravity 2.0/CLI: `/andino-workflow resume the existing task plan and check repository drift`; in the IDE, check Customizations
  and mention the skill by name.
- OpenCode: ask the agent to use `andino-workflow` for the task; its native skill tool
  loads the matching ID, subject to configured permissions.

Implicit selection depends on the task, host and invocation policy. Installation
does not force activation or authorize commits, pushes, merges, publication,
deployment, live-data changes or unrelated external actions.

Explicit invocation works even for a greeting or a daily question. The discipline
should remain unobtrusive: do not announce phases or interrogate the user when a
direct answer is sufficient. Implicit selection should still avoid routine
questions and trivial edits that do not benefit from coordination.

| Request | Expected behavior |
| --- | --- |
| Use Andino Workflow. Hello. | Respond naturally without tools or a plan. |
| Use Andino Workflow. How do I install PostgreSQL on Windows 11? | Give useful guidance, checking current official instructions where needed; ask about a project only if a material setup choice depends on it. |
| Registration is broken; fix the controller. | Separate symptom from diagnosis; inspect relevant implementation and runtime evidence. An unapplied migration may explain the failure without a code change. |
| Add total students to the dashboard. | Inspect existing student data and dashboard architecture before asking repository-answerable questions; clarify only unresolved product choices. |
| Compare current options for our research project. | Use relevant current authoritative sources, distinguish inference and unknowns, and preserve the project's constraints. |

Existing capabilities and meaningful cross-feature effects are checked before
adding duplicate code or dependencies. Investigation stops when the next decision
is sufficiently supported, unless consequence or contradictory evidence requires
more. A skill improves operating discipline; it cannot guarantee model capability,
root-cause correctness or successful behavior without actual evaluation.

## Combine with specialist skills

Specialists are optional, separately installed packages. Use a separate sibling
folder under the appropriate host root for each one you need:

```sh
git clone --depth 1 --single-branch --branch ai-codebase-rescue https://github.com/andinoferdi/AI-RULES.git "$HOME/.agents/skills/ai-codebase-rescue"
git clone --depth 1 --single-branch --branch skripsi-skill https://github.com/andinoferdi/AI-RULES.git "$HOME/.agents/skills/skripsi-skill"
```

Rescue supplies engineering diagnosis, dispositions and verification. Skripsi
supplies thesis/research reasoning, domain state and evidence limitations. Use only
the specialist relevant to the task; neither requires or activates the other.
When Andino is active, it owns lifecycle and completion; for CHECKPOINTED work its
plan owns checkpoints and authoritative NEXT ACTION. Specialists return results,
evidence and recommended next actions.
Both work standalone in the host's normal task context when Andino is inactive.
Installing packages alone does not activate them or grant extra authorization.

Examples: ask Andino to coordinate bounded checkout stabilization with Rescue, or
an existing research milestone with Skripsi. No sibling is bundled or auto-installed.

## Update or switch branches

For a clean clone on this branch:

```sh
git -C "$HOME/.agents/skills/andino-workflow" status --short
git -C "$HOME/.agents/skills/andino-workflow" pull --ff-only
```

Resolve or preserve local edits before updating. If an older installation is a
copied/generated folder instead of a Git clone, preserve it outside every host's
skill roots, then replace it with a fresh clone. Do not blindly overwrite local
edits or leave a second discoverable backup. Old `.andino-generated.json` markers
belong to the retired sync workflow; do not mix that workflow with these clones.

Use separate clones to run multiple skills together. Branch switching is for a clean
development checkout: a single checkout exposes only one branch at a time, and a
single-branch clone initially fetches only the selected branch. An installed
folder must retain the name of the skill it contains.

## Verify your installation

Confirm `andino-workflow/SKILL.md` and every linked file in `references/`
exist. Check the actual loaded path and use the host's documented invocation above.
Codex detects updates automatically (restart if missing); Claude watches SKILL.md
in existing roots (restart for a newly created root). Antigravity documents discovery
at conversation start. No universal hot-refresh promise is made for OpenCode or IDEs.

Manual smoke cases, in a disposable context:

| Case | Request | Expected decision |
| --- | --- | --- |
| Positive | Resume an existing non-trivial implementation plan. | Inspect repository drift, reuse the plan and continue its next action. |
| Explicit daily | Use Andino Workflow to explain PostgreSQL installation on Windows 11. | Useful direct guidance, current sources as needed, no unnecessary project interview. |
| Explicit casual | Use Andino Workflow. Hello. | Natural reply, no engineering ceremony. |
| Investigation | Registration fails; supplied runtime evidence shows an unapplied migration. | Ground the diagnosis in runtime evidence; no unnecessary controller patch. |
| Negative | Fix one known wording typo. | Make a targeted edit/check without unnecessary planning ceremony. |

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
