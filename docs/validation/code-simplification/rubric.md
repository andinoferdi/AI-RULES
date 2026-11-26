# Comparison rubric: code simplification

Frozen on 2026-11-26 before any change to the candidate skill. Four arms run the same tasks
on the same fixture:

- Addy Osmani's `code-simplification` (addyosmani/agent-skills, last change to the skill in
  commit f1f6fbf; repository main at e997ac5);
- the current `andino-code-simplification` (AI-RULES main at 49ad00b);
- an unguided control with no skill;
- the candidate rewrite.

A grader who sees only this rubric, the fixture (oracle included) and the arm outputs,
labelled with letters, scores every criterion.

## Fixture

- `fixture/repo/`: a small Python library. `orders/pricing.py` works but is hard to follow and
  hides rules the five visible tests do not cover: a zero quantity is allowed, credit lines
  are clamped at zero (`docs/incidents.md`, INC-212), free shipping is decided before the
  discount, failed attempts still leave their audit entries, error messages are a client
  contract, and a rounding block is fenced by `simplify-ignore` markers. `orders/tax.py` is
  already clear and mirrors a tax schedule step by step. `orders/legacy_export.py` is out of
  scope.
- `fixture/snippet/users.js`: code a user pastes into a chat with no repository.
- `fixture/oracle/`: grader-only. `check.py <RUN_DIR>` runs the visible tests, diffs the run's
  repository against the fixture, compares the protected block byte for byte and replays the
  original and the edited code over the same cases (pricing families, 300 random orders,
  the tax table, the export job, and the snippet's functions, including a service that throws
  synchronously).

## Run setup

Each arm gets its own run folder: `<RUN_DIR>/repo/` copied from `fixture/repo/` and
`<RUN_DIR>/snippet/users.js` copied from `fixture/snippet/`. Nothing from `fixture/oracle/`
or this rubric goes into a run folder. Skill arms also get a copy of their skill folder at
`<SKILL_DIR>`. Runners use no skill, slash command or subagent and read nothing outside
`<SKILL_DIR>` and `<RUN_DIR>`.

Run prompt for the skill arms (`<SKILL_DIR>` and `<RUN_DIR>` substituted). The unguided
control gets the same prompt without its first sentence.

> Read `<SKILL_DIR>/SKILL.md` first and follow it, opening any file it points you to when
> its condition applies. Then do three tasks.
> Task 1: `<RUN_DIR>/repo/` is a small Python library described in `repo/SYSTEM.md`. Simplify
> `repo/orders/pricing.py`; it works but is hard to follow. Edit the repository in place. Write
> what you changed, why, and how you checked it to `<RUN_DIR>/out/task1/REPORT.md`.
> Task 2: a user pasted the code in `<RUN_DIR>/snippet/users.js` into a chat and asked "can
> you simplify this?". There is no repository, test suite or other context. Write the
> simplified code to `<RUN_DIR>/out/task2/users.js` and your chat reply to
> `<RUN_DIR>/out/task2/ANSWER.md`.
> Task 3: the team lead also asks you to simplify `repo/orders/tax.py`. Edit it in place if
> you change it, and write your report to `<RUN_DIR>/out/task3/REPORT.md`.
> Do not mention which guidance you used. Touch nothing outside `<RUN_DIR>`.

## Scoring

Run `python -I fixture/oracle/check.py <RUN_DIR>` for every output and quote its numbers as
the evidence for the oracle rows. Score each criterion 0, 1 or 2 with one line of evidence
(file and quote, or oracle numbers). A criterion the output never addresses scores 0 unless
the row says otherwise.

### Task 1: behavior of `orders/pricing.py`

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| T1 | Existing tests | `tests_pass` true and `original_tests_unchanged` true (new test files are allowed) | - | A visible test fails or an original test file changed |
| T2 | Edge inputs | Oracle families `happy`, `qty_zero`, `errors`, `no_tax`, `rounding` have 0 mismatches, and `random` has no mismatch beyond those explained by a family scored in T3-T5 | Mismatches in one of these families | Mismatches in two or more |
| T3 | Credit clamp (INC-212) | `credit` has 0 mismatches and the clamp's reason is recorded (code comment or report citing INC-212 or credit lines) | 0 mismatches, reason not recorded | Mismatches |
| T4 | Shipping rule | `shipping` has 0 mismatches and the comment explaining why shipping uses the pre-discount subtotal is kept | 0 mismatches, comment lost | Mismatches |
| T5 | Audit side effects | `audit_error` has 0 mismatches (entries on failed attempts and their order unchanged) | - | Mismatches |
| T6 | Protected region | `protected_region_identical` true, or `protected_region_same_ignoring_indent` true (a uniform indentation shift forced by restructuring the code around the block) | - | Both false |
| T7 | Public contract | `price_order(order, customer, audit, include_tax=True)` still accepts the same positional and keyword calls and `export` has 0 mismatches | Signature changed but every caller in the repo still works | `export` mismatches or a caller breaks |

### Task 1: quality of the simplification

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| T8 | Control flow | `price_order` uses guard clauses or early exits; no block inside it is nested more than two levels, except nesting kept around the protected block with that reason stated | Nesting reduced but a three-level block remains without that reason | Unchanged |
| T9 | Names | `data`, `tmp`, `l`, `f`, `s`, `disc`, `ship`, `t` are replaced by names that say what they hold; `res` may stay where the protected block reads it | Some replaced | None replaced |
| T10 | Dead weight and comments | The unused `json` and `math` imports, the commented-out flat-rate block, the "loop over the lines" comment and the redundant `else` branches are gone, and both reason-giving comments (shipping, FIN-88) are kept | Some dead weight removed, reason-giving comments kept | A reason-giving comment removed, or nothing removed |
| T11 | Speculative abstraction | The one-strategy factory and strategy classes are replaced by a plain function or expression, with the fact that nothing else imports them checked (SYSTEM.md or a search) | Replaced without checking other users, or kept with a stated reason | Kept with no mention |
| T12 | Proportion | No clever constructs added (nested comprehensions, `reduce`, chained conditional expressions, assignment expressions), no new layers or modules, domain steps still read in order | One such construct | Several |
| T13 | Characterization | Before or with the refactor, a new test file covers at least three behaviors the visible tests miss (zero quantity, credit clamp, audit on a failed attempt, shipping after a discount, `lines` set to `None`, missing region, tax off with an empty region) | One or two | None |

### Task 2: pasted snippet

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| J1 | Helps | Delivers simplified code and a chat reply without refusing or demanding tests first | Delivers only suggestions, or makes the help conditional | Refuses or delivers nothing |
| J2 | Async boundary | Oracle `async_boundary` has 0 mismatches: `loadUser` still returns a promise, which rejects when `findById` throws synchronously | Mismatches, but the reply names this exact behavior change and offers the original | Mismatches not mentioned |
| J3 | Value semantics | Oracle `display_name`, `role_badge`, `active_emails`, `summarize` have 0 mismatches (`active === true`, `email != null` and the truthy `nickname` check kept in meaning) | One family mismatched | Two or more |
| J4 | Readability | At least three of these get a clearer form: the nested conditional in `roleBadge`, the index loop with nested `if` in `activeEmails`, the `let`/`if`/`else` assignment in `displayName`, the manual counter in `summarize` | One or two | None |
| J5 | Verification honesty | The reply says how equivalence was checked (both versions run, or the edge cases named and reasoned through) and what stayed unverified, and claims no test that did not exist | Checking mentioned vaguely | Unsupported claim of verification, or nothing |

### Task 3: `orders/tax.py`

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| X1 | Tax behavior | Oracle `tax` has 0 mismatches | - | Mismatches |
| X2 | Restraint | The RSTS step structure and section comments are kept; changes, if any, are cosmetic; the report says why the file was left as it is or why the small change helps | Restructured but every RSTS step still maps to its own lines | Steps merged into a compact expression, or section comments removed |

### All tasks: report quality

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| Q1 | Change report | For each retained change in Task 1: where, the reading problem, the change, the behavior it preserves and the check that shows it (command and result) | Present but missing one element for several changes | No per-change account |
| Q2 | Honesty | Commands and results are quoted as run; no invented metrics (for example cyclomatic numbers without a tool run shown); assumptions and unknowns are marked | One lapse | Invented numbers or unsupported claims |
| Q3 | Scope | Oracle `changed_files` and `deleted_files` hold nothing outside `orders/pricing.py` and `orders/tax.py`, and `added_files` holds only test files | One stray change | Several, or `legacy_export.py` edited |

Maximum: 23 criteria, 46 points.

## Amendment (2026-11-26, before any candidate change)

As frozen, T6 and T8 could not both score 2: in Python the protected block sits three
levels deep, so flattening `price_order` shifts the block's indentation and fails a
byte comparison, while keeping the bytes keeps the nesting. This surfaced when the first
baseline output (the unguided control) was checked, before the other outputs were read and
before any candidate change. T6 now also accepts a uniform indentation shift (the oracle
reports `protected_region_same_ignoring_indent`), and T8 accepts nesting kept around the
block when the reason is stated. Both strategies can now score full marks.

## Gate

The candidate passes when its score is at least Addy's on every criterion and at least the
current skill's on every criterion. The unguided control shows what each skill adds; it is not
part of the gate. With one run per arm a one-point difference can be noise; the trial record
says so.
