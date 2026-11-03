# Council verdict quality

Status: delivery verified locally. Independent model comparison pending.

1. Update council/SKILL.md at 42d740a. Give advisors and reviewers evidence criteria, strengthen chair synthesis and establish a single chat output contract. Preserve five lenses, anonymity, Focus and honest fallbacks.
2. Extend main/evals/council.json for architecture, product and missing evidence. Compare the same cases against the old skill and upstream where the host permits.
3. Verify the Council diff and publish the Council branch. Update the stable Council pin and sequence on main. Run installer tests and isolated setup, then push main and verify remote refs.

## Evidence

- Council runtime aafc9a089fbfc27aa1ee745ead2f781e67218cf4 pushed to origin/council.
- Static comparison: upstream supplies reusable role prompts and a fixed verdict layout. The new Council procedure makes criteria, evidence challenges and switch conditions explicit while keeping the Andino and Focus contracts.
- Three installer integration tests passed. Isolated Codex project setup installed Council and Focus from both latest and bundled source modes. Both installed Council files match Git blob 2f91fc28ebe568f4fa3460b9c0c81ef11646bdf3.
- The three behavioral fixtures define comparison cases. No independent agents ran, so parity with upstream is unmeasured.

NEXT ACTION: use the three fixtures to compare verdicts in an authorized independent council session.
