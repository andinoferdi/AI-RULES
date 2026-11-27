# Claim evidence and recipes

Read this when a claim is not a single test run you just made. It says what proves each kind of
claim, what does not, how to run old code without touching the working tree, and what each record
line holds.

## What proves a claim

| Claim | Requires | Not sufficient |
| --- | --- | --- |
| Tests pass | The intended suite ran on the current state: counts shown, 0 failures, every skip, xfail and deselected test named | An earlier run, another commit's CI, "should pass", a subset presented as the suite |
| Lint or type check clean | Its own run on the current state: 0 errors | A passing test run, a partial file list |
| Build succeeds | The build command ran, exited 0 and produced the expected artifact (name, version) | Lint or tests passing, logs that look fine |
| Bug fixed | The reporter's command or symptom check run on the current code shows the expected result | The code changed, a test that never reaches the bug |
| A regression test guards a bug | The test failed on code without the fix, for the reason it guards, and passes on the current code | The test passes once; it was written alongside the fix; it uses an input the old code also handled |
| Requirements met | Each requirement checked one by one against code or a test that reaches it, both parts of compound ones | The suite is green; the report says so |
| A worker, agent or colleague finished | You read the actual diff and new files, and ran the checks on the integrated result | Their report, their quoted numbers, a commit message |
| Ready to release or merge | Every checklist item has a current result on the exact state to ship; unrunnable items are named | "Most items pass", a green log from an earlier state |
| An earlier result still holds | The state it covered (commit, files, inputs, environment) matches now and nothing it depends on changed | The same branch name, "nothing important changed" |
| Installed, published or deployed | The destination serves the intended revision: version, hash or content read back from it | The upload or deploy command exited 0 |

Structural checks (paths, schemas, headings) prove structure. Procedural examples prove the
operations they run. Neither proves how a model will behave or that a live host loaded the change.

## Status words

- **passed**: an observation on the current state supports the claim in the scope you name.
- **failed**: an observation contradicts the claim; quote the output.
- **fixed**: it failed, you changed something, and the re-check after your last edit passed.
- **not verified**: the check is missing, skipped, stale, unrunnable here or only reasoned about.
  Say why and which check would settle it.

Example: "12 unit tests passed. The end-to-end check was skipped, so the checkout flow remains
unverified."

## Reusing an earlier result

Reuse a result instead of rerunning it when all of these still hold, and say so in the record:
the same commit or file contents for everything the check reads, the same inputs and
configuration, the same environment where it matters (runtime, service versions), and no
freshness window the check depends on has passed. If any one changed or cannot be shown, rerun.
A result for another commit, tag or version is not evidence for this one, however recent.

## Old code in a disposable copy

To see a regression test fail on code without the fix, run it against a copy, never against the
user's working tree. Put the copy inside the folders the task lets you write, and delete it after.

- **Old revision of one file.** Make a scratch folder in your writable scope, write the old file
  there with `git show <old-commit>:<path> > <scratch>/<path>`, copy the test files beside it,
  run the tests from the scratch folder, then remove it.
- **Whole old revision.** `git worktree add <scratch>/old <old-commit>`, copy in the test under
  check, run it there, then `git worktree remove <scratch>/old`.
- **No history.** Write the old behaviour from the report into a scratch module only if it is
  exact; otherwise report the test as never seen failing.

Never use `git stash`, `git checkout -- <file>`, `git reset` or copying files over the working
tree for this: they risk uncommitted work that is not yours, and a failed restore leaves the
repository on the old code.

## Record fields

Each record line holds the claim, the status, the command or action, and the output line that
decides it. Add the state it ran on when it is not the current working tree (commit, copy, host).
Keep secrets out: write `<REDACTED>`. Quote only the lines that carry the signal. A claim you
settled by reading code, not by running something, says "by reading".
