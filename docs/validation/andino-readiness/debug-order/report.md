# Debugging-guide order on `unknown-bug-id`

Date: 2026-10-20
Runtime: `andino-workflow` `17ce784` (content SHA256 `4678cf05…`), base `f99ec59` (`50c24252…`)
Evaluator: `main` with this change to `scripts/run_andino_capability_eval.py`
Host: Claude Code 2.1.300, isolated read-only (`--safe-mode`), catalog `../catalog.json`

## Cause

The contract was already in SKILL.md: load `skills/debugging/GUIDE.md` before the first
diagnostic read, and same-batch reads do not count. The failing runs never reached it in time.
Their first or second tool batch read `SKILL.md` together with `products.py`, `app.log` and
`test_products.py`, so the fixtures were read before any SKILL.md body text was in context.
The prompt names the supplied files next to "read it", and parallel reads made that cheap.

Before invocation, a host only shows a skill's frontmatter description. The isolated Claude
harness showed it for every catalog skill but not for the entry skill, which native discovery
always lists.

## Change

- Runtime (`17ce784`): the description adds "When it applies, read it and any guide it
  selects before inspecting task files, not in the same parallel batch." The body paragraph
  stays byte-identical, as `UnchangedContractsTest` requires.
- Evaluator: Claude safe-mode prompts include the entry skill's own frontmatter under
  `Runtime metadata:`, as native discovery would. Other hosts and the Search First entry are
  unchanged.
- `tests/test_andino_debugging_order.py`: structural contract. On `f99ec59` it fails the
  description check and passes the rest.

## Results (order verdict; every answer found the zero-based page slice, with no writes)

| Set | Runtime | Harness | Model | Order PASS |
| --- | --- | --- | --- | --- |
| `baseline/` | f99ec59 | old | Haiku 5.5 xhigh | 1/3 |
| `harness-only/` | f99ec59 | new | Haiku 5.5 xhigh | 2/3 |
| `after-fix/` | 17ce784 | new | Haiku 5.5 xhigh | 5/5 |
| `after-fix-opus/` | 17ce784 | new | Opus 5.5 xhigh | 2/2 |
| `../baseline`, `../after-fix` (earlier) | 634585a / f99ec59 | old | Opus 5.5 | 0/2 |

In all 7 after-fix runs, the first batch is `SKILL.md` alone, and fixtures come only after the
guide. Showing the old description alone (`harness-only/`) still failed 1 of 3 runs with the same
same-batch pattern, so the description wording carries the fix.

Limits: small samples; Claude Code only. Codex, Antigravity and OpenCode were not rerun. On
those hosts, native discovery already shows the description, but they were not checked.
