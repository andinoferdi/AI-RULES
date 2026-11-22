# Prove claims against the current result — supporting contract

## Evidence record

| Claim | Observation required |
| --- | --- |
| Tests pass | Intended tests actually ran, with counts, failures, and skips accounted for. |
| Build succeeds | The intended build completed and produced the expected result. |
| Bug fixed | A check exercises the original symptom and observes the expected behavior. |
| Worker output accepted | The reviewed changes satisfy the criteria in the integrated state. |
| Task complete | Every required criterion has current passing evidence. |
| Published or installed | The destination exposes the intended revision or file contents. |

Use **passed** for the observed scope, **failed** for a contradicted criterion,
and **not verified** for missing, stale, skipped, or inaccessible scope. For
example, “12 unit tests passed. The end-to-end check was skipped, so the
checkout flow remains unverified.”

Record claim, criterion, command/action, cwd/runtime, material timestamps, exit code, cases/assertions, safe output/log, tested hashes and exclusions.

Structural tests prove path/schema; procedural examples prove demonstrated operations; neither proves live host loading or future model compliance. Requirements need acceptance coverage beyond tests.

Controlled RED requires confirmed mutation landed and expected assertion failed. Use disposable copies, never reset/restore user work. Reuse success until affected bytes/state or material freshness condition changes.
