# Diff-scoped floor guard recipe
Input is the merge-base→working-tree diff, including staged and unstaged changes, PLUS untracked files. Run from repository root so a subdirectory does not omit new files. Obtain merge base and all input lists before evaluating; any failed collection returns exit 2. Do not execute file names or interpolate diff text into a shell command. Use argument arrays; handle paths with spaces, renames and deleted files. A portable implementation should use NUL-separated path inventory and native null-device handling instead of assuming /dev/null.
Track diff file-header state only between diff header and first @@ hunk. Inside a hunk +++i is added content, not a +++ file header. Deletion retains old path when new path is null device. Collect added/removed lines and deleted paths; include untracked content as additions.
Five finding families:
1. Added suppression (@ts-ignore/ts-nocheck, eslint/biome/noqa/type-ignore, istanbul/Stryker disable, nosemgrep/gitleaks allow).
2. Added skip/todo tests; deleted test files; assertion removed from a surviving test.
3. Stub/not-implemented/empty catch or TODO standing for missing implementation.
4. Removed floor rule or loosened numeric dimension. Match stable first-column/bullet identity; pair numbers by direction min/max/unknown. New lower min or higher max is weakening; removed number/rule is weakening; unknown-direction changes require review. New thresholds tighten. Changes to dates/prose are not metric rules.
5. New exception rows require rule/path/reason/owner/expiry and accepted authority.
Return 0 clean,1 findings,2 cannot evaluate. Emit rule and file/line only, never matched secret/source text. This shallow guard catches cheap green-making moves, not all semantic cheating. Renames/direction wording require human interpretation. A maintained exception file may allow a specific rule/path; broad ignore changes themselves need review.
Contract examples: coverage >=80→>=70 fails; maximum payload <=200→<=250 fails; >=80→>=85 tightens; missing base errors; new untracked test with skip fails; deleting assert fails; unchanged known suppressions outside diff do not fail.
A quality bar maps each number to command/phase/reason. Reuse lcov from the actual run, scope expensive mutation/security to changed code, redact secret scanners. Tool absence is recorded, never silently clean. Existing deficits become a ratchet at today's measured value with an explicit tolerance and owned expiring exceptions.

Provenance: independently worded adaptation of the Addy snapshot identified in the owning GUIDE.md; full MIT notice at ../../../references/legal/addy-license.md. No upstream installation or hook is required.
