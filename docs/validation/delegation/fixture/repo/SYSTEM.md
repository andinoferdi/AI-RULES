# Shopline

Shopline is a small order service for one online shop. It is a Python 3.12 package with a
command-line interface used by the shop's admins. Tests run with `python -m pytest` from the
repository root.

## Layout

- `src/shopline/money.py`: decimal amounts and `format_price`, used for every amount shown
  to people (CLI output, exports, receipts).
- `src/shopline/pricing.py`: discount rules.
- `src/shopline/orders.py`: the `Order` model and order lifecycle (create, cancel).
- `src/shopline/inventory.py`: stock reservation. Several worker processes reserve stock at
  the same time in production.
- `src/shopline/auth/tokens.py`: signed session tokens (HMAC-SHA256). Security-sensitive.
- `src/shopline/export/legacy_totals.py`: the old totals report still used by accounting.
- `src/shopline/cli.py`: the `shopline` command.
- `src/shopline/i18n/messages_*.py`: message catalogues for English, Indonesian and German.
- `tests/conftest.py`: shared pytest fixtures used by every test module.
- `docs/spec/order-export.md`: accepted spec for the order export feature.
- `docs/plans/order-export-plan.md`: accepted implementation plan for that spec.
- `docs/cli.md`: admin documentation for the CLI.
- `ci/`: output of the latest CI run on `main`.
- `handoff/`: reports returned by subagents during an earlier session (Task 3 only).

## Working environment

- The agent works in a Claude Code session on a local checkout of `main`, branch
  `feature/order-export` already created and clean. Committing to the feature branch is
  allowed; pushing, merging and installing packages are not, unless the user says so.
- Subagents are started with the Agent tool. Each call can set `model` (`haiku`, `sonnet`,
  `opus`) and `effort` (`low`, `medium`, `high`, `xhigh`, `max`). An omitted model inherits
  the session model, which is `opus`.
- A subagent starts with no memory of this session. Measured start-up cost on this host is
  about 60,000 tokens per subagent before it does any work.
- Subagents cannot start their own subagents.
- Network access inside subagents is blocked; `pip install` fails there.

## Rules from the user (from their CLAUDE.md)

- Before starting subagents, state the number of agents, the task, model and effort of
  each, then wait for approval.
- Choose the lowest safe model and effort. At most 3 subagents at once. Never use effort
  `max`, and never put every subagent on the strongest model or on effort `high`.
- A failed or stopped subagent is never rerun without asking.
- Commit, push, deploy, package installs: wait for explicit approval.
