# Andino Workflow

Andino Workflow coordinates a **31-member public core** and selectively loaded internal techniques. It owns routing, one durable checkpoint, permissions and evidence-based acceptance; selected skills retain their full methods and checks. Codex, Claude Code, OpenCode and Antigravity are peers.

Public members have native `andino-*` entrypoints. Specialized techniques live as ordinary Markdown resources: no nested native entrypoint, compatibility shim or old invocation alias. Load only the technique needed now. Selecting a resource does **not** start its parent's lifecycle, run other modes, reopen accepted decisions or create a second plan.

## What It Does

The exact active and cumulative retired sets are in [the distribution manifest](references/portfolio.json). Selection triggers and exclusions are in [the method/resource index](references/internal-method-index.md).

### Direction, design and delivery of work

| Public member | Responsibility |
| --- | --- |
| `andino-brainstorming` | Open intent and choices, why before how, decision rounds and a confirmed design; optional decision-frontier, feasibility-probe, idea-validation and async-question resources. |
| `andino-planning` | Exact implementation changes, dependencies and proof; optional behavior-readiness, dependency-slicing and recurring-process resources. |
| `andino-plan-execution` | Authorized dependency-ready execution; independently selectable task-implementation, vertical-slice and frontend-engineering resources. |
| `andino-delegation` | Decide, brief and accept any subagent work (plan lanes, investigations, research, reviews, panel seats) under one envelope approval and parent acceptance. |
| `andino-api-and-interface-design` | Consumer-first design of any interface (HTTP, GraphQL, module, props, events, agent tools); optional HTTP-contract, module-depth and import-enforcement resources. |
| `andino-architecture-survey` | Deepening candidates from the hot spots or a named area, shown as a before/after HTML report and then grilled; never edits product code during the survey. |

### Implementation and verification

| Public member | Responsibility |
| --- | --- |
| `andino-tdd` | Executable RED/GREEN behavior guards; optional typed-fixture migration preserving invalid negative cases. |
| `andino-debugging` | Reproduce, prove and fix an unknown cause through six evidence gates with a report template; quick path when the compiler names the cause. |
| `andino-verification` | Observed acceptance evidence before consequential completion claims. |
| `andino-browser-testing-with-devtools` | Reproduce, fix and replay in a real browser; release pass at 360, 768 and 1440 px by device emulation, accessibility, console split and loading metrics. |
| `andino-code-review` | Spec and Standards review with pinned scope, evidence from the reviewed bytes and the repository left as found; request and receive protocols. |
| `andino-code-simplification` | Behavior-preserving simplification of working code, in a repository or pasted, with a per-change ledger and protected regions. |
| `andino-constraint-driven-development` | Establish and preserve the quality floor. |
| `andino-doubt-driven-development` | Fresh scrutiny of consequential assumptions and invariants. |

### Production boundaries

| Public member | Responsibility |
| --- | --- |
| `andino-security-and-hardening` | External-input, authentication, data and dependency trust boundaries. |
| `andino-deprecation-and-migration` | Consumer-aware interface/schema retirement and migration. |
| `andino-observability-and-instrumentation` | Useful production evidence, monitoring and runbooks. |
| `andino-performance-optimization` | Measured bottlenecks and verified improvements. |
| `andino-ci-cd-and-automation` | CI gates and required checks, failing or flaky runs, workflow security, deploy promotion and rollback; optional commit-check setup. |
| `andino-shipping-and-launch` | Authorized release readiness, rollout and recovery planning. |
| `andino-git-skills` | Select workspace, operation-safety, change-hygiene, branch-integration or PR-draft craft. No implicit commit, push or destructive recovery. |

### Knowledge and collaboration

| Public member | Responsibility |
| --- | --- |
| `andino-agent-document-authoring` | Writing and auditing documents agents read: AGENTS.md, CLAUDE.md, skill text and descriptions, pointers. |
| `andino-skill-maker` | Executable skill/procedure authoring with baseline and candidate evaluation. |
| `andino-documentation-and-adrs` | Durable documentation and decisions; optional domain vocabulary. |
| `andino-handoff` | Portable continuation and optional context packing. |
| `andino-human-procedure` | Necessary steps requiring human-only access or authority. |
| `andino-issue-triage` | Maintainer-requested issue/PR evaluation without unauthorized tracker writes. |
| `andino-optimize-prompt` | Explicitly requested light edit of a raw task prompt that keeps its shape, every named skill and phase, and every fact; suggestions and up to three questions follow it. |
| `andino-session-diagnostics` | Session-level failures; optional prevention review after causes are known. |
| `andino-learning-workspace` | Intentional learning; optional course-exercise scaffolding. |
| `andino-article-shaping` | Shape a fixed pile into an article with its author: reader first, pile-built candidates, agreed blocks only, nothing invented; optional raw capture. |

Workflow advice is a [workflow-owned resource](references/workflow-advice/guide.md), not a mandatory router. Project conventions use the [project-setup resource](references/project-setup/guide.md), not a prerequisite for every task.

## When to Use

| Use for | Do not use for |
|---|---|
| Non-trivial work that needs the right skills chosen and sequenced | Plain questions, code explanations or small edits (do them directly) |
| Resuming earlier work from its checkpoint | Replacing a selected skill's own method or deliverable |
| Uncertain problems and bugs of unknown cause | Granting permissions the user has not given |
| Explicit requests for the workflow | Loading the whole capability collection up front |

## Quick Start

### Installation

Install with the **AI-RULES CLI** (included in every profile):

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES && python -m pip install .
ai-rules setup --capability andino-workflow --host <host>
```

`<host>` is one of `codex`, `claude-code`, `opencode`, `antigravity-cli` or `antigravity-ide`.

<details>
<summary>Manual installation</summary>

A manual copy installs only the coordinator. It does not expose the standalone `andino-*` members or safely retire prior installations, so prefer `ai-rules setup`. To copy the coordinator anyway:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/andinoferdi/AI-RULES.git ai-rules-src
git -C ai-rules-src sparse-checkout set skills/andino-workflow
cp -r ai-rules-src/skills/andino-workflow "<skills-dir>/andino-workflow"
```

| Host | Global skills directory | Project skills directory |
|---|---|---|
| **Codex** | `~/.agents/skills/andino-workflow` | `.agents/skills/andino-workflow` |
| **Claude Code** | `~/.claude/skills/andino-workflow` | `.claude/skills/andino-workflow` |
| **OpenCode** | `~/.config/opencode/skills/andino-workflow` | `.agents/skills/andino-workflow` |
| **Antigravity** | `~/.gemini/antigravity-cli/skills/andino-workflow` | `.agents/skills/andino-workflow` |

</details>

### Usage

Use the host's actual invocation mechanism, for example `/andino-workflow`, `/andino-tdd` or Codex's `$andino-debugging`. Availability and permissions must be checked on the current host; installed is not active or used.

Examples of narrow resource requests:

- “Fix modal focus and loading states using the frontend-engineering resource.” Load `skills/plan-execution/resources/frontend-engineering/guide.md` from the installed workflow root; do not start the executor's full lifecycle.
- “Check import boundaries for this accepted TypeScript layout.” Select API/interface's import-enforcement resource, not HTTP design.
- “Advise which workflow fits, without executing it.” Read the workflow-advice resource and stop at advice.
- “Integrate this branch.” Select Git branch-integration; reuse current authorization, verify before/after, and preserve the branch on failure. A completed merge cannot be undone with `merge --abort`.

## How It Works

### Resource resolution

A nested member resolves shared resources from its containing workflow package; a standalone `andino-*` member resolves them from the sibling `andino-workflow` package. Relative local resource links remain within each member. Do not substitute an unrelated unprefixed provider or bypass denied loading.

### Upgrades and migration

The consolidated bundle declares **installer protocol 1** in `references/portfolio.json`. Use a CLI release that implements that protocol. Older binaries and older frozen bundles do not acquire retirement behavior merely because this branch changed. Local uncommitted source verification is not release publication; the CLI's frozen bundle pins must be coordinated after corresponding revisions exist.

Fresh setup must install the coordinator, the exact active public members and required Focus/Search First packages. Managed upgrades must retire only artifacts whose ownership and unchanged contents are proven. A matching `andino-` prefix is not proof. Modified/unrecognized files and user commands are preserved as conflicts; do not manually force-remove them. Family replacement is a recoverable coordinated transaction, not instantaneous atomic visibility across every directory.

Backups/staging belong outside host discovery roots. Refresh native discovery in a **new host session** after migration: deleting an entrypoint cannot remove instructions already loaded into a running conversation.

### Verification

From an AI-RULES clone, `python scripts/ci_checks.py --group skills` runs the skill package validators and every test that reads real skill content. It checks structure and recorded behavior cases; it does **not** prove real setup, native discovery or model behavior on your host.

## Works With Other Skills

- **Focus** supplies communication and optional lightweight explanation repair (`references/explanation-repair.md`). It does not start a lesson, research task or file edit merely to clarify an answer.
- **Search First** supplies research-before-coding, source-backed answers (`references/sourced-answer/guide.md`) and version contracts (`references/version-contract/guide.md`): resolved dependency version → matching primary source → change → parity test.
- **Council** supplies independent decision scrutiny when requested or justified.
- **AI Codebase Rescue**, **Skripsi**, and **Three.js Skills** retain their separate eligible domain responsibilities.
- Explicit Taste/Impeccable choices remain authoritative: Taste generates a direction; Impeccable critiques/refines it when selected by the accepted UI policy.

Sibling resources require actual permitted sibling loading; a name in this README is not activation. No retired public ID silently redirects to an internal resource.

## Files

- [`SKILL.md`](SKILL.md) — Runtime coordination contract.
- [`references/internal-method-index.md`](references/internal-method-index.md) — Method and selective-resource index.
- [`references/method-dispatch.md`](references/method-dispatch.md) and [`references/routing.md`](references/routing.md) — Dispatch and routing.
- [`references/execution-plan-template.md`](references/execution-plan-template.md) — Portable checkpoint template.
- `skills/<member>/` — The 31 public members, each with `SKILL.md` and `GUIDE.md`.
- [`references/legal/provenance.md`](references/legal/provenance.md) — Provenance of adapted methods.
- [`references/legal/license.md`](references/legal/license.md) — MIT license notice for AI-RULES-authored content.
- [`references/legal/addy-license.md`](references/legal/addy-license.md), [`references/legal/matt-license.md`](references/legal/matt-license.md) and [`references/legal/superpowers-license.md`](references/legal/superpowers-license.md) — Third-party MIT notices.

## License

AI-RULES-authored content in this skill is released under the [MIT License](references/legal/license.md). Third-party material keeps its original license; see [references/legal/provenance.md](references/legal/provenance.md).
