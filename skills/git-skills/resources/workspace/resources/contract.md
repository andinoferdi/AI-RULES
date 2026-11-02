# Preserve user state and authorized isolation — supporting contract

## Isolation decision record

Record root, Git/common dirs, superproject, branch/detached state, worktrees, dirty user paths and allowed mutations. Avoid credential-bearing remotes in logs.

Dirty linked workspace can be correct continuation. Baseline failures need named evidence, not discarded work. Resolve symlinks before move/delete; containment and ownership are separate from authorization.

Read the current task's actual branch and location restrictions; a method cannot create or switch branches without applicable authority. Installation never runs project setup. Native tooling cannot override branch restrictions.
