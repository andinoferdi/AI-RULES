# CI runtime reference repair

Status: DONE
Depth: LITE
Current Phase: Verification (DONE)

## Objective and acceptance

Repair the five InternalDispatchContract failures reported by GitHub Actions without skipping or weakening runtime checks. The focused tests and the workflow's local validation commands must pass. Preserve ANDINO_RUNTIME_DIR candidate validation. Hosted CI remains unverified until a remote run.

## Current state and decisions

- Clean main checkout at 16e8aaa before this task; only remote-tracking skill branches exist.
- CONFIRMED: tests/test_andino_reliability.py reads `andino-workflow:<path>`, but validate-skills.yml fetches `origin/andino-workflow`. All five reported failures reproduce locally (20 tests, 5 failures).
- Search First: inspected workflow, neighboring validators, runtime reader and existing tests. ADOPT the established `origin/andino-workflow` reference used by the validators; no dependency or external API research is needed.
- Loaded installed Andino debugging and CI/CD guides, Search First and Focus; regression phase uses the bundled TDD guide. No delegation, publication or deployment.
- Verification environment: Windows, Python 3.12.10; origin/andino-workflow at 65df26d182b3118e3f18ee46522eac83ea1036fb.

## Verification evidence

- Focused unittest: 22 tests, PASS. The new remote-only fixture failed with the original reader and passes after changing the default ref. Candidate-directory precedence and absent-file behavior pass.
- `python scripts/validate_skills.py --webbased-ref origin/WebBased --threejs-ref origin/threejs-skills`: PASS (7 skill packages, 7 eval schemas, Three.js family and Focus reference equivalence).
- `python scripts/validate_threejs_family.py --runtime-ref origin/threejs-skills`: PASS (45 methods, 714 resources, 10 scenario schemas).
- `python scripts/validate_andino_capabilities.py --runtime-ref origin/andino-workflow`: PASS (74 schemas, 60 contracts).
- `python scripts/validate_skripsi_traceability.py`: PASS (335 requirements, 32 capabilities, 110 eval owners, 75 task records).
- Self-review: Spec PASS (same five contracts retained; remote-only checkout fixed); Standards PASS (existing ref convention reused, candidate override retained, no dependency/workflow changes). `git diff --check`: PASS. No independent reviewer or hosted CI run.
- `python -m unittest discover -s tests`: PASS, 328 tests in 187.417s, 5 skips, no failures (exit 0). The installer Minimal project fixture installed all three skills successfully in temporary isolation.
- Hosted GitHub Actions was not run; this task changes local files only and does not commit, push or deploy.

## Execution board

| Phase | Status | Evidence |
| --- | --- | --- |
| Diagnosis | DONE | Exact five failures reproduced; fetched reference and hardcoded test reference differ. |
| Regression and repair | DONE | Remote-only fixture failed before the fix; candidate-directory precedence passed. Reader now uses origin/andino-workflow. All 22 focused tests pass. |
| Verification | DONE | Full suite: 328 tests, 5 skips, no failures; all four workflow validators pass. Bounded self-review and whitespace check pass. |

## NEXT ACTION

None: local repair and verification complete. Hosted CI requires publishing these changes through the user's normal Git workflow.
