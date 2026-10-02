# AI-RULES

This branch (`main`) is the AI-RULES installer and control plane: source code, tests, release tooling, CI, evaluation cases, and active validation evidence. It shares Git history with `WebBased` but does not distribute Web/chat rules or runtime skill packages.

## Distribution branches

| Branch | Contents |
| --- | --- |
| [`WebBased`](https://github.com/andinoferdi/AI-RULES/tree/WebBased) | Web/chat rules and project templates |
| [`andino-workflow`](https://github.com/andinoferdi/AI-RULES/tree/andino-workflow) | Adaptive problem solving, proportional investigation and optional checkpoints |
| [`ai-codebase-rescue`](https://github.com/andinoferdi/AI-RULES/tree/ai-codebase-rescue) | AI Codebase Rescue runtime skill |
| [`skripsi-skill`](https://github.com/andinoferdi/AI-RULES/tree/skripsi-skill) | Thesis and research runtime skill |

Install or use a distribution from its own branch. `main` deliberately contains no copy of those runtime packages.

The runtime skills are standalone. The [family standard](docs/agent-skill-family-standard.md)
defines their shared package and release requirements without changing their distinct methods.

## Quality checks

The [evaluation cases](evals/README.md) cover expected behavior and cases that should not trigger a skill. The validator reads the three skill branches through Git refs, so fetch those branches before running:

```sh
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
python3 scripts/validate_skripsi_traceability.py
python3 scripts/audit_skripsi_live.py
```

These commands check package structure and evaluation-case format. They do not run live agent behavior. CI runs on pushes and pull requests targeting `main`, manual dispatch, and a daily schedule. Because `main` is the repository default branch, scheduled runs use the latest commit on `main`.

For unpublished runtime commits, use
`python scripts/validate_skills.py --andino-ref andino-workflow --rescue-ref ai-codebase-rescue --skripsi-ref skripsi-skill`
and `python scripts/validate_skripsi_traceability.py --runtime-ref skripsi-skill`.
The live-audit command checks saved evidence consistency without executing a model;
run it locally in addition to CI's package, unit-test and traceability checks.

The [Skripsi contract review](docs/validation/skripsi-skill/contract-review.md), [requirement inventory](docs/validation/skripsi-skill/traceability.json), and [live-evidence review](docs/validation/skripsi-skill/live-review.json) distinguish implementation ownership from observed behavior. The [evaluation guide](evals/README.md) describes opt-in isolated execution; CI never invokes a model or incurs live evaluation usage.

The [Andino integration review](docs/validation/andino-workflow/integration-review.md)
records the adaptive workflow revision and original 28 evaluation specifications, structural
verification and remaining live validation. Reasoning depth and checkpoint persistence
are independent; explicit daily and conversational use does not require a plan.

The [capability integration handoff](docs/validation/andino-workflow/capability-handoff.md)
tracks the subsequent runtime integration layer, 32 required capability scenarios
and two supplemental routes. The [publication review](docs/validation/andino-workflow/publication-review.md)
records the published runtime, default setup upgrade proof and current validation scope.
Andino selects minimum useful methods/instruments just-in-time from
actual need and evidence. Installed, active and used are separate, provider
collisions are resolved explicitly, and invocation depends on host permissions
and connected services. This does not expand the first-party installer catalog.
Validate an edited runtime worktree with
`python scripts/validate_andino_capabilities.py --runtime /path/to/andino-worktree`.
The [evaluation guide](evals/README.md) separates structural checks, isolated
selection/loading tests, read-only service smoke tests and unverified host coverage.

## AI-RULES installer/orchestrator

AI-RULES installs and manages only Andino's first-party skills: **Andino
Workflow**, **AI Codebase Rescue**, and **Skripsi Skill**. Third-party skills,
plugins, MCP servers, runtimes, and services are never installed, configured,
updated, or health-checked by AI-RULES. Follow each upstream project's current
documentation for installation, authentication, updates, and compatibility.

Profiles are `minimal` (Andino Workflow), `engineering` (Andino Workflow + AI
Codebase Rescue), `research-skripsi` (Andino Workflow + Skripsi Skill), and
`everything` (all three). `setup`, `add`, `update` and `doctor` check the latest
configured source branches by default. A folder containing SKILL.md alone is not
evidence that a skill is current.

### Keeping skills current

Run `ai-rules setup` again and select the agents/profile you want to reconcile.
Each selected skill's configured remote branch is fetched once per invocation;
the exact commit and full installed content are checked before reporting current.
Skill updates do not require a new CLI release or edits to the packaged manifest.
This applies to all registered first-party skills and their configured branches;
it does not automatically install unrelated third-party skills or arbitrary branches.

For explicit selections:

```sh
ai-rules setup --profile everything --host codex --host claude-code --host opencode --host antigravity-cli --host antigravity-ide --yes --non-interactive
ai-rules update --profile everything --host codex --dry-run
```

Latest mode requires Git and source access, but works from outside a Git checkout.
A failed fetch, missing branch or invalid skill returns an error, never a stale
"up to date" result. Read-only previews use temporary source downloads and do not
persist installation state. Commands resolve a fixed SHA before mutation, so a
branch moving during the run does not change the approved payload.

Clean official Git installations fast-forward without replacing .git or changing
their branch/origin. Copies matching the current source or one of its latest 256
revisions can be recognized; older/unrecognized copies and local modifications are
preserved with a blocking explanation. Updates retain backups under the selected
state directory. Shared directories and symlink/junction targets are respected.
Concurrent changes detected after planning stop replacement. Restart the agent's
session as required by its skill loader after an update.

Use `--source bundled` explicitly for the CLI's frozen release manifest instead
of checking online freshness. This mode does not mean latest; a packaged executable
uses embedded bundles, while a source installation needs the pinned Git objects in
its working repository. `repair` defaults to this mode and remains an explicit
replacement/repair operation. Do not use repair as a routine updater.

Latest-mode locks record source provenance and file verification. Exact replay of
a branch-tracked locked snapshot is not implemented; restore rejects it instead
of silently installing a different revision.

Skill content updates and CLI program updates are separate. Existing installations
of the old CLI need a one-time refresh using the instructions below to gain this
behavior. The [dynamic-update checkpoint](docs/exec-plans/completed/dynamic-skill-updates.md)
records the regression evidence and implementation decisions.

### Setup

To set up AI-RULES locally:

```sh
git clone https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES
python -m pip install .
ai-rules setup 
```

### External resources — manual installation

Skills and plugin families: [Superpowers](https://github.com/obra/superpowers),
[Ponytail](https://github.com/DietrichGebert/ponytail), [Claude-Mem](https://cmem.ai/),
[UI/UX Pro Max](https://uupm.cc/), [Taste Skill](https://www.tasteskill.dev/),
[AI Website Cloner](https://github.com/JCodesMore/ai-website-cloner-template),
[Graphify](https://graphify.net/), [Anti-Slop](https://github.com/miqdadbadjuber/anti-slop), and [Agent Skills](https://github.com/addyosmani/agent-skills).

MCP servers: [Context7](https://github.com/upstash/context7),
[Playwright MCP](https://github.com/microsoft/playwright-mcp),
[Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp),
[Git MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/git),
[Draw.io MCP](https://www.npmjs.com/package/@drawio/mcp),
[StarUML MCP](https://www.npmjs.com/package/staruml-mcp-server), and specialized/on-demand
[Premiere Pro MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP) and
[Cheat Engine MCP bridge](https://github.com/miscusi-peek/cheatengine-mcp-bridge).

The installer control plane runs on `main` without changing runtime skill branch behavior. In source mode, set `PYTHONPATH=src` and run:

```sh
python -m ai_rules setup --profile minimal --host codex --dry-run --non-interactive
python -m ai_rules doctor --profile minimal --host codex --dry-run
```

For development or an environment with Python 3.11+, use source mode:

```sh
python -m pip install --editable .
python -m ai_rules setup --profile minimal --host codex --dry-run --non-interactive
```

### Refreshing a local development install

If `ai-rules setup` still shows an older prompt or does not recognize a recently
added option, the `ai-rules` executable may still point at an older installed
package. From the repository root, refresh the editable installation:

```powershell
python -m pip install --editable .
ai-rules setup --help
```

The help output should include the newly added flags. To confirm which executable
PowerShell will run, use:

```powershell
Get-Command ai-rules -All
```

This refreshes the local Python installation without installing skills or changing
any existing AI-RULES-managed targets. Then run `ai-rules setup` again normally.

Release artifacts are built per operating system with `python scripts/build_release.py`; the command emits `release-manifest.json` and `SHA256SUMS`. On a fresh machine, set `AI_RULES_RELEASE_BASE_URL` to that release directory and run `scripts/bootstrap.ps1` (Windows) or `scripts/bootstrap.sh` (macOS/Linux). The bootstrap verifies the checksum before installing the executable and delegates all setup behavior to `ai-rules setup`.

Manual host installation remains a supported fallback when a host requires its own marketplace or OAuth flow. The installer reports those paths as manual or partially verified and never stores API keys, bearer tokens, or OAuth credentials in AI-RULES state.
