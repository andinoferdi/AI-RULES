# Skripsi Skill

A research and thesis workflow skill for AI agents. It guides thesis, proposal,
methodology, analysis and defense preparation from the user's actual research
state, keeping approved decisions, evidence boundaries, institutional guidance,
and the next research action explicit.

Start with [the skill](SKILL.md). Progressive routing loads detailed methodology
only when needed from `references/`, while adaptable research artifact helpers live
in `assets/`.

Skripsi Skill works standalone using normal task context, or alongside `andino-workflow`.
When Andino is active, Andino remains the lifecycle, plan, and checkpoint owner while
Skripsi Skill acts as the research specialist.

## Install

Clone this branch into a directory named `skripsi-skill` under your agent's skill root.
The commands below work in PowerShell and Bash; `$HOME` is your user home.
Use a destination that does not already contain another installation.

```sh
git clone --depth 1 --single-branch --branch skripsi-skill https://github.com/andinoferdi/AI-RULES.git "$HOME/.agents/skills/skripsi-skill"
```

That destination works globally for Codex and OpenCode. For another host or
project scope, replace the destination using this table, appending `/skripsi-skill`.
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
git clone --depth 1 --single-branch --branch skripsi-skill https://github.com/andinoferdi/AI-RULES.git "$HOME/.claude/skills/skripsi-skill"
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

Install the **whole folder**, including `references/` and `assets/`. No build,
package manager, sync script, MCP service or personal host configuration is
required by this skill. For team distribution in a research project, commit the
package files as ordinary files or use a deliberately managed submodule. Do not
include personal credentials or unverified research data.

## Use

- Codex CLI/IDE: select the skill with `$` or `/skills`, for example
  `$skripsi-skill Judul saya sudah ACC. Bantu saya menyusun outline proposal bab 1-3.`
- Claude Code: `/skripsi-skill Saya sedang merevisi BAB III berdasarkan masukan dosen pembimbing.`
- Antigravity 2.0/CLI: `/skripsi-skill Saya sudah memiliki output analisis data. Bantu saya memulai pembahasan BAB IV.`;
  in the IDE, check Customizations and mention the skill by name.
- OpenCode: ask the agent to use `skripsi-skill` for the task; its native skill tool
  loads the matching ID, subject to configured permissions.

Implicit selection depends on the task, host and invocation policy. Installation
does not force activation or authorize commits, pushes, merges, publication,
deployment, live-data changes or unrelated external actions.

## Combine with Andino Workflow

Install the companion branch into a **separate sibling folder** under the same
host skill root:

```sh
git clone --depth 1 --single-branch --branch andino-workflow https://github.com/andinoferdi/AI-RULES.git "$HOME/.agents/skills/andino-workflow"
```

Use the appropriate root from the table for Claude Code or Antigravity. The result
is two packages: `andino-workflow/` and `skripsi-skill/`.

Andino coordinates overall project lifecycle, execution plans, checkpoints, and
cross-system tasks. Skripsi Skill provides research-domain reasoning, state tracking,
methodology routing, and evidence boundaries. When Andino is active, its plan remains
the single lifecycle owner; Skripsi Skill returns research findings and recommended
actions without creating competing plans. Merely installing both does not activate
both. Neither package bundles or automatically installs the other.

Example request: "Use andino-workflow to coordinate this research milestone and
skripsi-skill to evaluate literature synthesis readiness for Chapter 2."

## Update or switch branches

For a clean clone on this branch:

```sh
git -C "$HOME/.agents/skills/skripsi-skill" status --short
git -C "$HOME/.agents/skills/skripsi-skill" pull --ff-only
```

Resolve or preserve local edits before updating. If an older installation is a
copied/generated folder instead of a Git clone, preserve it outside every host's
skill roots, then replace it with a fresh clone. Do not blindly overwrite local
edits or leave a second discoverable backup.

Use separate clones to run multiple skills together. Branch switching is for a clean
development checkout: a single checkout exposes only one branch at a time, and a
single-branch clone initially fetches only the selected branch. An installed
folder must retain the name of the skill it contains (`skripsi-skill`).

## Verify your installation

Confirm `skripsi-skill/SKILL.md` and every linked file in `references/` and `assets/`
exist. Check the actual loaded path and use the host's documented invocation above.
Codex detects updates automatically (restart if missing); Claude watches SKILL.md
in existing roots (restart for a newly created root). Antigravity documents discovery
at conversation start. No universal hot-refresh promise is made for OpenCode or IDEs.

Manual smoke cases, in a disposable context:

| Case | Request | Expected decision |
| --- | --- | --- |
| Positive | My title is approved; continue the proposal/BAB III from the supplied research context. | Preserve settled decisions and identify only evidence needed for that chapter. |
| Negative | Polish this one academic sentence without changing its meaning. | Edit the sentence without imposing a research lifecycle or inventing sources. |

For selection checks, present the request without explicitly forcing the skill.
For instruction checks, explicitly invoke it and inspect its actual decisions.
Record host/version, skill commit, loaded path, input, observed actions and limits.
These are proposed checks, not cross-host PASS claims. Package validation is
STRUCTURAL VERIFIED only for the tested revision; documented host features are
DOCUMENTATION VERIFIED. LIVE HOST VERIFIED requires observed host execution;
unrun checks remain NOT VERIFIED. Historical evidence lives on main.

## What Skripsi Skill covers

- **ResearchState & intent**: tracks actual stage (topic, proposal, analysis, revision, defense) without restarting settled work.
- **Discovery & title**: feasibility checks, title anatomy, inclusion gates, and style variants without cosmetic filler.
- **Problem, gap & questions**: distinguishes practical problems from literature gaps; verifies search provenance before negative claims.
- **Research design**: routes quantitative, qualitative, mixed methods, and R&D/DSR with clear causal and measurement boundaries.
- **Literature & systematic review**: 4-stage progressive reading, claim provenance, synthesis matrices, and PRISMA-aligned gates.
- **Quantitative planning**: construct operationalization, instrument suitability, sampling logic, and analysis pre-specification.
- **Advanced methodology & ethics**: secondary data fitness gates, theoretical mechanism grounding, and publication due diligence.
- **Results, discussion & conclusion**: finding registry, explicit RQ-to-conclusion mapping, and evidence-grounded recommendation scaffolds.
- **Defense & revision**: defense briefs, dynamic question banks, flexible reasoning cards (no rigid scripts), and examiner feedback propagation.

## Package and sources

This branch contains only `SKILL.md`, `references/`, `assets/` and this README.
The [main branch](https://github.com/andinoferdi/AI-RULES/tree/main) owns the quality control plane: validators, test suites, evaluation
scenarios (`evals/`), requirement traceability (`docs/validation/`), and CI workflows.
Development plans, raw SRS documents, and chat transcripts are excluded from the
runtime package. Edit this branch's root files as the canonical source.

Installation and discovery guidance checked against official documentation on 2026-09-21:
[Codex skills](https://learn.chatgpt.com/docs/build-skills),
[OpenCode V2 skills](https://opencode.ai/v2/docs/skills)
([V1 differences](https://opencode.ai/docs/skills/)),
[Claude Code skills](https://code.claude.com/docs/en/skills), and
[Antigravity skills by surface](https://antigravity.google/docs/skills?tab=ide).
These sources establish folder conventions, not identical runtime behavior.
