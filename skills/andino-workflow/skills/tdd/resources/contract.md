# Supporting contract: invariants, record fields and the refactor gate

## Invariants the gates rest on

1. Every production edit is preceded by a red run of the row it serves, or the row's test is
   proved by gate 4. A suite that is green at the end proves nothing about a test that never
   failed.
2. A red counts only when the runner executed the named test and it failed on the predicted
   assertion. Collection, import, syntax, name and fixture errors are setup failures.
3. Expected values come from an independent source: a literal, a hand-checked fixture or the
   requester's own figures. Never from the code under test, its helpers or its formula.
4. Tests act through the public seam and observe through it. A seam may span several calls
   (create then fetch, reserve then release); it never bypasses them through storage.
5. Doubles stand in for slow, external, unsafe or nondeterministic boundaries only, and mirror
   the real boundary's complete response and side effects.
6. Known failures, skipped tests and choices made for the requester are reported, never hidden.

## Record fields

| Field | Content | Source gate |
| --- | --- | --- |
| Test commands | The repository's focused and full-suite commands | Prerequisites |
| Slices | One entry per row: behavior, seam, example, red line, green change and run | 1, 2, 3 |
| Proof for tests that passed at once | The old revision or break, the failing line, the restore check | 4 |
| Refactor | What changed and the suite run after it, or none | 5 |
| Verification | Suite counts with every failure named old or new; the reporter's command for a bug | 6 |
| Not done or not verified | Open choices, checks that could not run, behavior left unprotected | all |

## The refactor gate in detail

Start only when every row is green. Name the observed problem first: duplication, an unclear
name, a long function, a needless indirection. Inspect the callers of anything you touch. Change
one thing, rerun the suite, and repeat. Compare return values, raised errors, side effects and
their order before and after. Apply the deletion test: say which concept or indirection the
change removes. A deep module may hide complexity; an adapter without real variation adds it.
New behavior belongs in a new row, never in this gate. Stop when the next change would alter a
test, the seam or the architecture, and record it as a separate request.

## Provenance

Substantive adapted material is covered by the MIT notices in
[../references/license.md](../references/license.md).
