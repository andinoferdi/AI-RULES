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
| OpenCode | `~/.config/opencode/skills` (also reads `~/.agents/skills`) | `.opencode/skills` (also reads `.agents/skills`) |
| Claude Code | `~/.claude/skills` | `.claude/skills` |
| Antigravity 2.0 / IDE | `~/.gemini/config/skills` | `.agents/skills` |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills` | `.agents/skills` |

For example, Claude Code globally:

```sh
git clone --depth 1 --single-branch --branch skripsi-skill https://github.com/andinoferdi/AI-RULES.git "$HOME/.claude/skills/skripsi-skill"
```

Antigravity IDE also documents the legacy global path
`~/.gemini/antigravity/skills`. Prefer the location for your installed surface.
Other agents can use this directory when they support Agent Skills; use their
documented discovery path rather than assuming every agent shares these roots.
Keep one installation per skill visible to each host where practical. OpenCode
also reads Claude-compatible directories, so duplicate copies can shadow updates.

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
does not force activation or grant permission for external actions.

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

Confirm `skripsi-skill/SKILL.md` and its referenced files in `references/` and
`assets/` exist. Open a fresh host session (or refresh its skill list), select the
skill explicitly, and ask it to explain its scope and current-state entry without
generating ungrounded research claims. Check the loaded path if multiple copies
exist. Then use a disposable research query to test actual behavior.

Package metadata, relative links and isolated directory layouts were checked.
That is not evidence of native selection or successful task execution in all
four agents; those live checks remain environment-specific and unverified here.

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
The `main` branch owns the quality control plane: validators, test suites, evaluation
scenarios (`evals/`), requirement traceability (`docs/validation/`), and CI workflows.
Development plans, raw SRS documents, and chat transcripts are excluded from the
runtime package. Edit this branch's root files as the canonical source.

Installation guidance checked against official documentation on 2026-09-19:
[Codex skills](https://learn.chatgpt.com/docs/build-skills),
[OpenCode skills](https://opencode.ai/v2/docs/skills),
[Claude Code skills](https://code.claude.com/docs/en/skills), and
[Antigravity skills by surface](https://antigravity.google/docs/skills?tab=ide).
These sources establish folder conventions, not identical runtime behavior.
