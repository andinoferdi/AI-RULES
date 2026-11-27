# Performance optimization supporting contract

Supporting contract for `andino-performance-optimization`. Operates under Andino Workflow
governance. The gates live in [the skill](../SKILL.md); this file states what each must leave
behind and what each record field means.

## Invariants

1. **Numbers before edits.** Outside the quick path, no source edit aims at performance until a
   baseline exists: the command, at least three samples, the statistic, the spread, the
   conditions and the target.
2. **Attribution before the change.** The change targets a cost that a capture taken before the
   edit showed to dominate. A suspect named by the requester, a colleague or the code's look is
   confirmed or ruled out by an output of its own.
3. **One mechanism per attempt.** Each attempt changes one thing and gets its own row, kept,
   reverted or inconclusive.
4. **Same-condition remeasure.** The after-number uses the baseline's command, sample count and
   conditions. A delta inside the spread is not a gain.
5. **Correctness gates the metric.** Tests stay green, the output is compared before and after,
   and every input the result depends on (tenant, permission, locale, freshness) is preserved. A
   change that wins by dropping required work is a regression.
6. **A guard seen failing.** The regression check fails on the old code and passes on the new;
   a check whose tool cannot run here is written out and marked NOT RUN, never reported as run.
7. **Honest numbers.** Every number names its source (local benchmark, lab, field). A value for
   the changed system that nobody measured is NOT MEASURED; an expected effect is labelled as one.
8. **Proportion.** A request with no measured symptom, budget or target gets a timing and its
   share first; negligible work is left unchanged and answered in a few lines.

## Record fields

| Field | Holds | Comes from |
| --- | --- | --- |
| Goal | Metric, statistic and target in the requester's words, or the smallest worthwhile change | Prerequisites |
| Baseline | Command, sample count, statistic, value, spread, conditions (revision, input size, cache state, environment, device/network, concurrency) | Gate 1 |
| Attribution | The capture, the dominant cost and its share; each suggested cause with the output that ruled it in or out | Gate 2 |
| Change | One mechanism, expected movement, the result that would disprove it | Gate 3 |
| Attempts | One row per idea: baseline -> result, verdict (keep, revert, inconclusive), why | Gate 4 |
| Correctness | Tests run, outputs compared before and after, constraints checked | Gates 3-4 |
| Guard | The check, its failing output on old code and passing output on new; or NOT RUN with config and command | Gate 5 |
| Not measured or not verified | Production, field data, devices, load levels not exercised; the next capture to run | All gates |

## Verdicts

| Result against baseline | Verdict |
| --- | --- |
| Delta exceeds the spread, target or threshold met, tests green, output unchanged | keep |
| Delta inside the spread | revert (neutral) |
| Worse | revert |
| Better, but a test failed or the output changed | revert |
| Conditions not comparable, or the spread too wide to decide | inconclusive, with the capture that would decide it |

## Resource map

- [Measurement and diagnosis](measurement-and-diagnosis.md): symptom-to-capture tree, sampling
  and statistics, profiling, query counting, allocation snapshots, reading Lighthouse reports.
- [Optimization patterns](optimization-patterns.md): fixes with code for queries, pools,
  caching, memory, CPU, startup and front-end runtime.
- [Web performance audit](performance-audit.md): Core Web Vitals, LCP subparts, layout shift,
  responsiveness, lab versus field, scorecards and budgets.
- [Worked example](worked-example.md): one optimization through all gates, with its record.

## Provenance

Adapted material is covered by the MIT notices in [../references/license.md](../references/license.md).
