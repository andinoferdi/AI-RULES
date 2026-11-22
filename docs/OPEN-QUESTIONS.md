# Open questions

- Stale routing-readiness assertions (found 2026-11-22, updated 2026-11-23).
  `tests/test_andino_routing_readiness.py` still reads the old local branch
  `andino-workflow`, which no longer exists, so it always skips. Pointed at
  `skills/andino-workflow` (`ANDINO_RUNTIME_DIR=skills/andino-workflow`), four
  assertions fail against the current content:
  `test_entrypoint_separates_discoverable_facts_from_user_owned_direction`,
  `test_method_index_covers_mixed_execution_and_uncertainty`,
  `test_readiness_distinguishes_what_is_open` and
  `test_research_contract_preserved_and_task_guides_precede_focus` (they still
  expect, for example, `skills/decision-interview/GUIDE.md` and the phrase
  `before Focus`). The owner decides per assertion whether the contract is still
  wanted; then the test reads `skills/andino-workflow` by default like the other
  Andino tests, or the assertion is deleted.
