# Rescue report

Use when writing the final report for the user or returning evidence to Andino. The
report tells the team what is now true, what changed, how it was checked and what
still needs a decision. Keep it as short as the evidence allows; every section is
required, and an empty section says so in one line.

## Skeleton

```markdown
# Rescue report: <area>

Outcome: <one or two lines: what is now true for users, what is not yet>
Mode: Assess | Stabilize | Remake. Boundary: <paths and interfaces>. Eligibility: <signal>.

## Baseline and test trust
<command, revision, result before any change; which existing tests protect the
contract and which do not, with the reason>

## Findings
| ID | Finding | Severity | Confidence | Disposition | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| RSC-001 | ... | HIGH | HIGH | REFACTOR | input -> observed vs expected; file:symbol | Fixed in step 2 |
| RSC-004 | <healthy area> | - | HIGH | KEEP | tests that exercise its contract | Assessed |

## Changes
| Step | Concern | Kind | Files | Check and result |
| --- | --- | --- | --- | --- |
| 1 | Pin current scheduling behavior | tests only | tests/... | 14 pins pass on unmodified code |

## Preserved contracts and intentional changes
<contracts kept; each intentional behavior change with its contract reason>

## Downstream impact
<for each changed contract: consumers inside and outside the repository; data or
records already written under the defect and whether they need reconciliation;
or "none found" plus how that was checked>

## Verification
| Check | Command or procedure | Result |
| --- | --- | --- |
| Full suite | python -m unittest ... | PASS (32 tests) |
| Real provider | not available | UNVERIFIED |

## Decisions for the owner
<product or policy questions the evidence cannot settle, each with the options and
the current safe behavior>

## Deferred and INVESTIGATE
<finding ID, why deferred, the next evidence action and the result that would allow
a decision>

## Next action
<one concrete step>
```

## Rules

- Findings use the contract in evidence-and-findings.md. Healthy assessed areas appear
  as KEEP rows, not as defects.
- Severity is impact; confidence is strength of proof; disposition is the decision.
  None of them is a score. Do not add health percentages or 0-100 ratings.
- Each Changes row is one concern. Kind is `tests only`, `structure` or `behavior`.
  A behavior row names the pins it flipped.
- Verification results are PASS for an executed check that met its criterion, FAIL for
  an executed check that did not, UNVERIFIED for anything not executed. Report the test
  count from the actual run.
- Downstream impact is required whenever a public contract, stored data or a status
  that other systems read changed. Records written while the defect was live (for
  example, items marked complete that never completed) are named as a reconciliation
  need even when fixing them is out of scope.
- Assess mode: leave Changes as "none (read-only)" and add a `Proposed steps` list in
  the order the Stabilize loop would run them, each with its protection and check.
- With Andino active, return the same fields to the existing plan. Andino owns the
  authoritative NEXT ACTION and completion; the report's Next action is a recommendation.
