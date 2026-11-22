# Factual Integration and Branch Delivery Guide

Internal Andino resource. Operates under Andino Workflow governance.

## Purpose and selection

Use when deciding how to integrate verified work or carrying out an authorized delivery. Use change hygiene for commit preparation and PR drafting for the description.

## Procedure

1. Capture the candidate checkout, HEAD, branch, dirty paths and in-progress Git operations. Verify the exact committed tree you intend to deliver. If project checks fail, cannot run, or cover a different tree, record the evidence gap and stop delivery.
2. Read the user's existing choice. A scoped push request selects push only. A push plus PR request selects both. Resolve only the destinations needed for that action. Offer available choices only when the user has left the action open.
3. Execute the selected route using the [action protocol](resources/integration-menu-and-execution.md). For a local merge, locate the actual base checkout, verify it is safe to use, and run checks on the merged result. A failed check preserves both refs and blocks cleanup.
4. Verify each side effect separately. Use the [cleanup protocol](resources/workspace-cleanup-and-safety.md) only after a verified merge or confirmed discard, with recorded ownership and authority. Preserve the checkout for a push, PR, or keep decision.

## Permissions and safety

Earlier scoped authorization counts. Ask only for the unresolved action or destination. Verification grants no mutation authority. Keep existing changes intact and preserve state if a command or verification fails. Treat each commit, push, PR, merge, and cleanup as a separate action.

## Output and verification

Record candidate SHA, test command and result, action and destination, observed local or remote ref, PR URL if created, and workspace disposition. For partial delivery, name the completed action and the first remaining blocker. Record durable evidence in the active plan when one exists.

## Worked example

A user requests a commit and push to the feature branch's established remote. Change hygiene produces the scoped commit and the required checks pass on its exact tree. Push the verified candidate to that named ref and check the remote SHA. Report the commit and destination. Keep the worktree available.

## Local resources

- Handoff Ledger and Status Schema: [resources/contract.md](resources/contract.md)
- Environment and Worktree Detection: [resources/environment-and-worktree-detection.md](resources/environment-and-worktree-detection.md)
- Pre-Integration Verification: [resources/pre-integration-verification.md](resources/pre-integration-verification.md)
- Integration Menu and Execution: [resources/integration-menu-and-execution.md](resources/integration-menu-and-execution.md)
- Workspace Cleanup and Safety: [resources/workspace-cleanup-and-safety.md](resources/workspace-cleanup-and-safety.md)
- Anti-Rationalization and Failure Modes: [resources/anti-rationalization-and-failure-modes.md](resources/anti-rationalization-and-failure-modes.md)
