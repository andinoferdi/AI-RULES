# Andino Workflow

An adaptive problem-solving protocol for AI agents. It matches the depth of investigation to the task, separates your goal from a suspected cause, and asks only about decisions the available context cannot settle. It covers development, troubleshooting, research, decisions, daily tasks, and conversation.

Resume work from a portable checkpoint, investigate an uncertain problem, or use
a focused engineering method without installing a separate workflow for each phase.
Andino keeps one lifecycle, permission boundary and acceptance gate.

## When to use

- You name it explicitly, for any task, including a simple question.
- A problem is uncertain or spans several steps.
- You resume a task with a saved plan. It checks for repository drift first.
- A bug has an unknown cause.
- You need thesis progress or next steps, with `skripsi-skill` when it is installed.
- You need UI/UX design or evaluation.

## Limits

Routine conversation and trivial mechanical edits outside mapped needs do not trigger it automatically. Name it explicitly if you want it anyway.

## Requires

`focus` and `search-first`. Setup installs both as required dependencies. A manual clone does not, so use `ai-rules setup --capability andino-workflow --host <host>` to get the full set.

## Install

Requirements: Python 3.11+, Git, and an installed agent for CLI setup.

With the AI-RULES CLI (recommended):

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES
python -m pip install .
ai-rules setup --capability andino-workflow --host <host>
```

Pass `--host` with `codex`, `claude-code`, `opencode`, `antigravity-cli` or `antigravity-ide`. Without it, setup targets Codex. For a project install, add `--scope project --project-root <path>`. Run the same command again to update.

Manual, for this skill only:

```sh
git clone --depth 1 --single-branch --branch andino-workflow https://github.com/andinoferdi/AI-RULES.git "$HOME/.agents/skills/andino-workflow"
```

Install the whole folder, including `skills/`, local resources, references and legal
notices, not only `SKILL.md`. The folder must keep the name `andino-workflow`. For another host, change the destination to the folder in this table:

| Host | Global folder |
| --- | --- |
| Codex | `~/.agents/skills/andino-workflow` |
| OpenCode | `~/.config/opencode/skills/andino-workflow` |
| Claude Code | `~/.claude/skills/andino-workflow` |
| Antigravity IDE and 2.0 | `~/.gemini/config/skills/andino-workflow` |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills/andino-workflow` |

For project scope, use `.agents/skills/andino-workflow` (Codex, OpenCode, Antigravity) or `.claude/skills/andino-workflow` (Claude Code) in the project root. Keep one copy per skill, and reload the host session after installing.

## Use

- Codex: `$andino-workflow <task>`
- Claude Code: `/andino-workflow <task>`
- OpenCode: ask the agent to use `andino-workflow`, or use the command that setup registers.
- Antigravity: ask the agent to use `andino-workflow`. In the IDE, check Customizations.

Example: `$andino-workflow resume the existing task plan and check repository drift`

Activating a skill grants no extra permission.

## Bundled methods and provenance

One native entrypoint contains 59 internal methods adapted from Addy
Osmani Agent Skills, Matt Pocock Skills and Superpowers. The
[method index](references/internal-method-index.md) covers requirements, planning,
implementation, diagnosis, tests, reviews, architecture, productivity and delivery.
These local `GUIDE.md` resources under `skills/` load only when needed. The upstream
repositories and plugins are not runtime dependencies.

Examples: `$andino-workflow use the tdd method for this behavior change`, or
`use andino-workflow, specifically domain-modeling`. Original names such as
`test-driven-development`, `grill-me` and `writing-plans` are internal aliases,
not extra native skills to install. Reading a guide proves loading; relevant
action and results prove use. Keep the [snapshot provenance and legal notices](references/legal/provenance.md);
upstream updates require manual review and regressions.

Use `brainstorming` to explore possible directions before choosing an outcome.
For explicit advice about which workflow fits a problem, use `workflow-advisor`
(alias `ask-matt`). Advice does not execute the recommended workflow. Accepted
specifications proceed to implementation without repeating ideation. `teach`
supports a lesson in chat; persistent learning files require a learning need
across sessions or an explicit request.

## Notes

- `focus` is the default communication style for every invocation, including direct answers.
- Andino loads other installed skills only when the task needs them, for example `search-first` for research or `ai-codebase-rescue` for codebase stabilization.
- To combine it with a specialist, install `ai-codebase-rescue` or `skripsi-skill` as a separate folder under the same skill root. Andino coordinates the work, and its plan stays the only lifecycle owner. Neither package installs the other.

For actual Three.js or NixieFX work, invoke the single `threejs-skills` family
through the host contract, then load only relevant [internal methods](references/threejs-specialists.md).
Say "use andino-workflow and threejs-skills", or name "threejs-skills, specifically
threejs-shaders". The `threejs` profile installs four directories: the complete
45-method family, Andino, Focus and Search First. Installation does not activate methods.

Council decision specialist: The [council](https://github.com/andinoferdi/AI-RULES/tree/council) branch offers five advisor perspectives, anonymous peer review when agents support it, and an actionable verdict. Focus remains the language layer and Andino retains routing and execution ownership. Standalone Council is available through `ai-rules setup --capability council`.

## Verification and safe update

Use one regular directory per native skill; preserve local edits before updating.
Setup's file checks establish package delivery, not live discovery or model behavior.
Installing the package runs no bundled examples, upstream hooks, package manager or
background server. CLI setup may fetch its configured runtime branch. Methods
requiring a browser, tracker, optional CLI or external service verify
actual availability and permissions first; offline examples do not prove live service use.

Manual smoke for each supported host: start/reload an isolated project session,
invoke Andino through that host's mechanism, request an explicit relevant method,
observe its GUIDE.md read and a concrete task artifact/result. Then ask a simple fact
and confirm irrelevant guides/plans/agents are not loaded. Test a missing/denied
resource and confirm honest UNAVAILABLE without another-copy bypass. For an unknown
bug observe diagnosis before repair; for TDD observe correct-reason RED, GREEN and a
separate optional refactor gate. Do not infer another host's behavior from one run.

The [main quality plane](https://github.com/andinoferdi/AI-RULES/tree/main/docs/validation/andino-unified)
owns source/asset matrices, procedural checks, installer tests, live records and
publication status. Deterministic examples, structural compatibility and actual live
host use are reported separately; unavailable checks remain NOT VERIFIED.
