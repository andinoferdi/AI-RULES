# Host Cost Calibration — Tiers, Effort Controls and Start-Up Cost

Internal Andino resource for `andino-delegation`. Records observed host facts; it is not a portable default.

The portable rules speak in tiers (Fast, Standard, Capable) and efforts (`low`, `medium`, `high`). This file maps them to what each host actually exposes and records what one child costs before it does any work. Only write a value here after observing it on that host; leave the rest `unmeasured`. Re-measure after adding or removing MCP servers, skills or large project rules, because those listings are part of every child's start-up context.

## 1. Probe (one child, once per host)

1. Dispatch one child on the Fast tier at `low` effort with the task "Reply with the single word OK. Do not use tools."
2. Read the token usage the host reports for that child.
3. Record host, date, tier/model, effort and tokens below. That number is the fixed start-up cost every child pays.
4. Delegation pays off only when the work saved inline exceeds that cost plus briefing and review.

## 2. Host Map

| Host | Fast | Standard | Capable | Effort control | Per-child selection | Start-up cost per child |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Claude Code | `haiku` | `sonnet` | `opus` | `effort`: `low` / `medium` / `high` (also `xhigh`, `max`: not used for delegation) | Yes: `model` + `effort` on each Agent call | ~58k–61k tokens (measured 2026-11-03; one-word and short-answer children) |
| Codex | unmeasured | unmeasured | unmeasured | unmeasured | unmeasured | unmeasured |
| OpenCode | unmeasured | unmeasured | unmeasured | unmeasured | unmeasured | unmeasured |
| Antigravity | unmeasured | unmeasured | unmeasured | unmeasured | unmeasured | unmeasured |

## 3. Host Notes

- **Claude Code**: user-level `modelSettings` can assign a default effort per model (for example a high default on the Fast tier). Always pass `effort` explicitly so a child never inherits it. The `Workflow` tool can fan out many agents in one call; it falls under the same wave go-ahead and the three-child ceiling.
- **Any host without per-child selection**: state in the wave announcement that children inherit the session's model and effort, and prefer inline work when that default is the Capable tier.

## 4. Worked Cost Check

A 30-task plan with a fresh implementer and a reviewer per task starts ~60 children. At ~58k tokens each that is ~3.5M tokens before any task work. The same plan run as ~7 lane workers, ~8 reviewers for risky tasks and 1 final reviewer starts ~16 children, ~0.9M tokens. These figures are start-up only; measure real totals before claiming savings.
