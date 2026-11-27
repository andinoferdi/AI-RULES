# Commit only what belongs to the change

Internal Andino resource under `andino-git-skills`. Loading it changes neither tools nor
permissions.

## Purpose

Turn a working tree into commits a reviewer can read, that contain the requested change and
nothing else: no secret, no scratch file, no one else's edit. Decide the version bump and the
changelog entry when the project ships to consumers.

## Trigger and non-trigger

Use when the user asks to commit, when a tree mixes the requested change with other files, or
when a release needs a version and changelog decision.

Do not use for: choosing where to work ([workspace](../workspace/guide.md)) or delivering the
commits ([branch-integration](../branch-integration/guide.md)).

## Procedure

1. **Label every path.** Run `git status --porcelain=v1 -uall`, `git diff --stat` and
   `git diff --cached --stat`. Give each path one label: part of the requested change, someone
   else's work, generated output, scratch or notes, or secret-bearing. Staged content you did not
   stage counts as someone else's until shown otherwise. Done when: every path in the status has a
   label.
2. **Keep secrets out.** Check the paths you would stage by name (`.env`, `.env.*`, `*.pem`,
   `*.key`, `id_rsa*`, `credentials*`, `*.p12`) and by content (`sk_live_`, `AKIA`,
   `-----BEGIN`, `password=`, `token=`): `git diff -- <path>` for tracked files, a search over
   untracked ones. Never stage them and never print the value; write `<REDACTED>`. When such a
   file is untracked and not ignored (`git check-ignore -q <path>` exits 1), tell the user and
   suggest the `.gitignore` line; add it only when they ask. Done when: you can list each excluded
   path with its reason and no value appears in your output.
3. **Group by change.** One logical change per commit, with its tests and the docs it needs.
   Formatting or refactoring goes in its own commit, before the behaviour change; an unrelated
   dependency upgrade in another. Around 100 changed lines is easy to review, but never split a
   change into commits that do not build or pass alone. Done when: each planned commit lists its
   paths and nothing appears in two groups.
4. **Stage by name.** `git add -- <path> <path> ...` for the group. Never `git add -A`,
   `git add .` or `git commit -a` in a tree that holds files outside the group. Compare
   `git diff --cached --name-only` with the group. Run the project's check on the staged content
   when other edits sit in the tree (they can hide or cause a failure). Done when: the staged list
   equals the group exactly.
5. **Write the message.** Subject in the imperative, under 72 characters, naming the behaviour
   ("Skip reminders for unsubscribed members", not "Update reminders.ts"). Body: why, the ticket
   or spec reference, anything a reviewer must not miss (a migration that drops data, a changed
   default), and the check you ran.

   ```text
   Skip reminder emails for unsubscribed members

   NOTIF-58. send_reminders now skips members whose opt_out_at is set.
   Migration 0012 copies the old unsubscribed flag into opt_out_at and drops
   the flag; rows written by app 3.1 lose it when the migration runs.

   Tests: npm test (128 passed)
   ```

   Commit with `git commit -F <file>` or `-m` per paragraph. Done when: `git log -1 --stat` shows
   the message and exactly the group's files.
6. **Decide the version and changelog** when the project publishes versions. MAJOR for a change
   consumers must adapt to (removed or renamed API, changed behaviour they rely on, including
   quirks), MINOR for an addition that keeps old use working, PATCH for a compatible fix. Write the
   changelog by impact (Breaking, Added, Fixed) with migration notes for each breaking entry.
   Tagging and releasing need the user's words. Done when: the bump has a one-line reason tied to
   observable behaviour.

## Output

```text
Committed: <sha> "<subject>" -> <files>
Left out: <path: reason (someone else's / scratch / secret, value not shown)>
Checks: <command> -> <result> on <staged content | whole tree>
Version: <MAJOR | MINOR | PATCH | not published>, because <reason>
Needs you: <a .gitignore line to add, a file whose owner is unclear, or nothing>
```

## Shortcuts that break a commit

| Shortcut | What happens instead |
| --- | --- |
| "`git add -A`, then unstage what doesn't belong." | One missed path ships a secret or someone's draft. Stage by name. |
| "The `.env.local` is untracked, so it's harmless." | Untracked and not ignored is one `git add .` from a leak. Warn the user. |
| "I'll stash their edits so I can commit cleanly." | Stashing someone's work is a change to it. Stage around it instead. |
| "'Update files' is fine, the diff explains it." | Reviewers and `git log` read subjects. Name the behaviour. |
| "Tests pass in my tree." | With other edits present, the commit may not be what was tested. |

## Permission boundary

Committing needs the user's words; staging and drafting do not. This guide grants no push, tag,
release, history rewrite or edit to files outside the group.

## Operational example (offline)

The grouping check flags a group that picks up someone else's path.

```python andino-operational-example
import json, os
def version(change):
    return {"breaking": "major", "additive": "minor", "compatible-fix": "patch"}[change]
def validate_groups(groups, not_ours):
    owned, errors = set(), []
    for group in groups:
        paths = set(group["paths"])
        if paths & not_ours: errors.append("user-change-selected")
        if paths & owned: errors.append("overlapping-groups")
        owned |= paths
    return errors
groups = [{"paths": ["src/api.py", "tests/test_api.py"]}, {"paths": ["docs/api.md"]}]
if os.getenv("ANDINO_NEGATIVE"): groups[0]["paths"].append("notes/user.txt")
print(json.dumps({"bump": version("breaking"),
                  "errors": validate_groups(groups, {"notes/user.txt"}),
                  "git_mutated": False}, sort_keys=True))
```

Expected output: `{"bump": "major", "errors": [], "git_mutated": false}`, and with
`ANDINO_NEGATIVE=1`: `{"bump": "major", "errors": ["user-change-selected"], "git_mutated": false}`.

## Provenance

Adapted in original wording from Addy Osmani's `git-workflow-and-versioning`
(addyosmani/agent-skills aeac41d4, MIT). Path labels, the secret check, the message example and
staging by name are Andino's. Notices: [license](../../references/license.md).
