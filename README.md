# Andino Workflow

Andino Workflow coordinates a **31-member public core** and selectively loaded internal techniques. It owns routing, one durable checkpoint, permissions and evidence-based acceptance; selected skills retain their full methods and checks. Codex, Claude Code, OpenCode and Antigravity are peers.

## Public skills and internal resources

Public members have native `andino-*` entrypoints. Specialized techniques live as ordinary Markdown resources: no nested native entrypoint, compatibility shim or old invocation alias. Load only the technique needed now. Selecting a resource does **not** start its parent's lifecycle, run other modes, reopen accepted decisions or create a second plan.

The exact active and cumulative retired sets are in [the distribution manifest](references/portfolio.json). Selection triggers and exclusions are in [the method/resource index](references/internal-method-index.md).

### Direction, design and delivery of work

| Public member | Responsibility |
| --- | --- |
| `andino-brainstorming` | Open intent and choices; optional decision-frontier, feasibility-probe, idea-validation and async-question resources. |
| `andino-planning` | Exact implementation changes, dependencies and proof; optional behavior-readiness, dependency-slicing and recurring-process resources. |
| `andino-plan-execution` | Authorized dependency-ready execution; independently selectable task-implementation, vertical-slice and frontend-engineering resources. |
| `andino-delegation` | Bounded independent work with disjoint write scopes and parent integration. |
| `andino-api-and-interface-design` | Select module-depth, import-enforcement or HTTP-contract craft without forcing the other modes. |
| `andino-architecture-survey` | Bounded observed architectural friction, not an unsolicited whole-repository rewrite. |

### Implementation and verification

| Public member | Responsibility |
| --- | --- |
| `andino-tdd` | Executable RED/GREEN behavior guards; optional typed-fixture migration preserving invalid negative cases. |
| `andino-debugging` | Reproduction and systematic investigation of an unknown cause. |
| `andino-verification` | Observed acceptance evidence before consequential completion claims. |
| `andino-browser-testing-with-devtools` | Rendered behavior, console/network and browser evidence; UI screenshots at 360, 768 and 1440 px. |
| `andino-code-review` | Specification and standards review. |
| `andino-code-simplification` | Evidenced simplification of green code without behavioral drift. |
| `andino-constraint-driven-development` | Establish and preserve the quality floor. |
| `andino-doubt-driven-development` | Fresh scrutiny of consequential assumptions and invariants. |

### Production boundaries

| Public member | Responsibility |
| --- | --- |
| `andino-security-and-hardening` | External-input, authentication, data and dependency trust boundaries. |
| `andino-deprecation-and-migration` | Consumer-aware interface/schema retirement and migration. |
| `andino-observability-and-instrumentation` | Useful production evidence, monitoring and runbooks. |
| `andino-performance-optimization` | Measured bottlenecks and verified improvements. |
| `andino-ci-cd-and-automation` | Build/test/deployment automation; optional commit-check setup. |
| `andino-shipping-and-launch` | Authorized release readiness, rollout and recovery planning. |
| `andino-git-skills` | Select workspace, operation-safety, change-hygiene, branch-integration or PR-draft craft. No implicit commit, push or destructive recovery. |

### Knowledge and collaboration

| Public member | Responsibility |
| --- | --- |
| `andino-agent-document-authoring` | Passive repository guidance such as CLAUDE.md and AGENTS.md. |
| `andino-skill-maker` | Executable skill/procedure authoring with baseline and candidate evaluation. |
| `andino-documentation-and-adrs` | Durable documentation and decisions; optional domain vocabulary. |
| `andino-handoff` | Portable continuation and optional context packing. |
| `andino-human-procedure` | Necessary steps requiring human-only access or authority. |
| `andino-issue-triage` | Maintainer-requested issue/PR evaluation without unauthorized tracker writes. |
| `andino-optimize-prompt` | Explicitly requested rewrite of a raw task prompt into the seven-slot format, naming only capabilities installed on the host. |
| `andino-session-diagnostics` | Session-level failures; optional prevention review after causes are known. |
| `andino-learning-workspace` | Intentional learning; optional course-exercise scaffolding. |
| `andino-article-shaping` | Shape supplied writing material; optional raw capture without invented anecdotes. |

Workflow advice is a [workflow-owned resource](references/workflow-advice/guide.md), not a mandatory router. Project conventions use the [project-setup resource](references/project-setup/guide.md), not a prerequisite for every task.

## Invocation

Use the host's actual invocation mechanism, for example `/andino-workflow`, `/andino-tdd` or Codex's `$andino-debugging`. Availability and permissions must be checked on the current host; installed is not active or used.

Examples of narrow resource requests:

- “Fix modal focus and loading states using the frontend-engineering resource.” Load `skills/plan-execution/resources/frontend-engineering/guide.md` from the installed workflow root; do not start the executor's full lifecycle.
- “Check import boundaries for this accepted TypeScript layout.” Select API/interface's import-enforcement resource, not HTTP design.
- “Advise which workflow fits, without executing it.” Read the workflow-advice resource and stop at advice.
- “Integrate this branch.” Select Git branch-integration; reuse current authorization, verify before/after, and preserve the branch on failure. A completed merge cannot be undone with `merge --abort`.

A nested member resolves shared resources from its containing workflow package; a standalone `andino-*` member resolves them from the sibling `andino-workflow` package. Relative local resource links remain within each member. Do not substitute an unrelated unprefixed provider or bypass denied loading.

## Installation and migration

The AI-RULES CLI lives on the repository's `main` branch:

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES
python -m pip install .
ai-rules setup --capability andino-workflow --host <host>
```

The consolidated bundle declares **installer protocol 1** in `references/portfolio.json`. Use a CLI release that implements that protocol. Older binaries and older frozen bundles do not acquire retirement behavior merely because this branch changed. Local uncommitted source verification is not release publication; the CLI's frozen bundle pins must be coordinated after corresponding revisions exist.

Fresh setup must install the coordinator, the exact active public members and required Focus/Search First packages. Managed upgrades must retire only artifacts whose ownership and unchanged contents are proven. A matching `andino-` prefix is not proof. Modified/unrecognized files and user commands are preserved as conflicts; do not manually force-remove them. Family replacement is a recoverable coordinated transaction, not instantaneous atomic visibility across every directory.

A manual coordinator clone alone does not expose all standalone members or safely retire prior installations. Prefer the protocol-aware setup for migration. Backups/staging belong outside host discovery roots. Refresh native discovery in a **new host session** after migration: deleting an entrypoint cannot remove instructions already loaded into a running conversation.

## Sibling ownership

- **Focus** supplies communication and optional lightweight explanation repair (`references/explanation-repair.md`). It does not start a lesson, research task or file edit merely to clarify an answer.
- **Search First** supplies research-before-coding, source-backed answers (`references/sourced-answer/guide.md`) and version contracts (`references/version-contract/guide.md`): resolved dependency version → matching primary source → change → parity test.
- **Council** supplies independent decision scrutiny when requested or justified.
- **AI Codebase Rescue**, **Skripsi**, and **Three.js Skills** retain their separate eligible domain responsibilities.
- Explicit Taste/Impeccable choices remain authoritative: Taste generates a direction; Impeccable critiques/refines it when selected by the accepted UI policy.

Sibling resources require actual permitted sibling loading; a name in this README is not activation. No retired public ID silently redirects to an internal resource.

## Verification and references

```sh
python -I scripts/verify_portfolio.py
```

This independent structural oracle checks exact public/retired sets, resource existence, live routes and local links in nested/flat layouts. It does **not** prove real setup, native discovery or model behavior. Installer/public-flow tests and fresh-context consumer checks are separate obligations.

- [Runtime coordination contract](SKILL.md)
- [Method and selective-resource index](references/internal-method-index.md)
- [Dispatch](references/method-dispatch.md) and [routing](references/routing.md)
- [Portable checkpoint template](references/execution-plan-template.md)
- [Provenance and notices](references/legal/provenance.md)
