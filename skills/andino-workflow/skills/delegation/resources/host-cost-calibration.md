# Host cost calibration: model and effort by role, start-up cost

Internal Andino resource for `andino-delegation`. Records observed host facts; it is not a portable default.

The portable rules speak in tiers (Fast, Standard, Capable) and efforts (`low`, `medium`, `high`). This file says which tier and effort each role starts at, maps tiers to what each host actually exposes, and records what one subagent costs before it does any work. Only write a measurement after observing it on that host; leave the rest `unmeasured`. Re-measure after adding or removing MCP servers, skills or large project rules, because those listings are part of every subagent's start-up context.

## Model and effort by role

Start at the row's tier and effort, state both on every call, and move up only on the evidence named.

| Role | Start at | Move up only when |
| --- | --- | --- |
| Implementer whose plan gives the complete code, or a single-file mechanical fix | Fast / `low` | repeated real mistakes despite a complete brief |
| Implementer working from prose; investigator; researcher; task reviewer; re-reviewer of a large fix | Standard / `medium` | a concrete complexity the brief could not remove |
| Implementer or reviewer of security, concurrency, state-machine, migration, money, renderer or 3D work | Standard / `medium`; Capable / `medium` when the plan names the risk | the plan's stated risk justifies `high`, said in the envelope |
| Final whole-change reviewer | lowest adequate, usually Standard / `medium` | broad consequential risk across the change |
| Scoped re-review of a small fix | Fast or Standard / `low` | the fix touched a shared contract |
| Panel seat | the panel skill's own guidance | — |

Turn count beats token price: the cheapest tier often takes two to three times as many turns on multi-step work, and every turn re-reads the context, so it can cost more in total. Keep a mid tier as the floor for reviewers and for implementers working from prose; use the cheapest tier when the work is transcription plus tests. Never `max`, never every agent on the Capable tier, never every agent on `high`. A model or effort change for a running lane is a replacement agent and a new ask.

## Observe existing usage first; probe only with approval

1. Prefer usage from an already authorized representative subagent. Do not start an agent just because this resource was loaded. Leave absent measurements unmeasured.
2. If calibration changes a real delegation decision, propose one Fast/`low` probe, state its actual model and effort, count it against the 3-agent limit and wait for the user's yes. A probe is still a resource-consuming agent.
3. Record host, date, model, effort, reported usage and measurement method. Total usage may include output, caching and runtime overhead; do not call all of it a fixed prompt cost without telemetry separating those parts.
4. Compare the expected saved work with start-up, briefing, integration, review and likely retries. These figures are estimates, not measured savings for another host.

## Host map

| Host | Fast | Standard | Capable | Effort control | Per-agent selection | Start-up cost per agent |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Claude Code | `haiku` | `sonnet` | `opus` | `effort`: `low` / `medium` / `high` (also `xhigh`, `max`: not used for delegation) | Yes: `model` + `effort` on each Agent call | ~58k–61k tokens (measured 2026-11-03; one-word and short-answer children). 2026-11-26: ~70k–72k total reported per no-tool child answering a 1,500–2,200-word prompt (`sonnet`/`medium` and `haiku`/`low`). 2026-11-27: ~75k total per one-read council seat (`sonnet`/`medium` and `sonnet`/`low`) |
| Codex | unmeasured | unmeasured | unmeasured | unmeasured | unmeasured | unmeasured |
| OpenCode | unmeasured | unmeasured | unmeasured | unmeasured | unmeasured | unmeasured |
| Antigravity | unmeasured | unmeasured | unmeasured | unmeasured | unmeasured | unmeasured |

## Host notes

- **Claude Code**: user-level `modelSettings` can assign a default effort per model (for example a high default on the Fast tier). Always pass `effort` explicitly so an agent never inherits it; `CLAUDE_CODE_EFFORT_LEVEL`, when set, overrides even a per-call effort. The `Workflow` tool can start many agents in one call; every one counts against the same envelope and the 3-agent limit. Facts from the official workflows and sub-agents pages, read 2026-11-27:
  - Concurrency: workflow agents run up to 16 at once by default; `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` (1-256, v2.1.269 or later) caps them. Agent-tool subagents stop at `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` (default 20, v2.1.217 or later). Either setting is a change the owner makes; without it, hold three in the script (the pool in the workflow's `references/orchestration.md`).
  - Ultracode (`/effort ultracode`, `claude --effort ultracode`, or the keyword in a typed prompt) plans a workflow for every substantive task and switches off the large-run warning, the Agent-tool concurrency limit and the first-launch approval in auto mode. It is not approval under this skill. Writing `ultracode` in backticks mentions it without starting a workflow.
  - Models: workflow agents run on the session's model unless a stage names one.
  - Resume: same session only; a failed agent reruns together with every agent started after it; a usage-limit pause needs an open interactive session, a reset within 24 hours and fewer than three waits. The checkpoint's unit ledger is what a new session resumes from.
  - Size guideline (`workflowSizeGuideline`): small fewer than 5, medium fewer than 10, large fewer than 50 agents; advice, not a cap.
- **Any host without per-agent selection**: say in the envelope that agents inherit the session's model and effort, and prefer inline work when that default is the Capable tier.

## Worked cost check

A 30-task plan with a fresh implementer and a reviewer per task starts ~60 agents. At ~58k tokens each that is ~3.5M tokens before any task work. The same plan run as ~7 lane workers, ~8 reviewers for risky tasks and 1 final reviewer starts ~16 agents, ~0.9M tokens. These figures are start-up only; measure real totals before claiming savings.
