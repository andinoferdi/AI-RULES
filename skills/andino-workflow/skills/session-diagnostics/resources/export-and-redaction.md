# Export a scrubbed bundle and draft an issue

Used by gates 7 and 8, and only when the user asks. The bundle is the user's session data,
packaged; the user reviews every file before it leaves the machine.

## Choose the level

Ask which level, stating what each keeps, unless the request already says:

| Level | Tool-result bodies |
| --- | --- |
| skeleton | none; each body becomes `[tool result: <tool>, <bytes> bytes, exit <code>]` |
| evidence | only for the events the report cites, scrubbed; the rest become the marker above |
| full | all, scrubbed |

## Build the bundle

1. Write the bundle in the workspace (`~/.andino/session-diagnostics/<session-id>/bundle/` or
   the folder the user named). Copy; never edit the originals.
2. Keep line alignment: a JSONL transcript stays JSONL with line N of the copy holding record N
   of the original, and every line still parses. A condensed rendering instead keeps `[L<n>]`
   markers for the original line numbers. Keep commands, tool names, ids, line numbers, model
   ids, skill names and harness versions: the bundle is useless without them.
3. Include the report, the case file and the transcripts the user asked for; list what you left
   out (for example, subagent transcripts).

## Scrub

Apply every category to every file, quotes and tool-call inputs included. The same original
value gets the same placeholder in every file, numbered in order of first appearance.

| Category | Placeholder | What to catch |
| --- | --- | --- |
| Email addresses | `<EMAIL-n>` | anything shaped like an email |
| People | `<PERSON-n>` | names, surnames, handles, git author names; role words stay |
| Account and org ids | `<ORG-n>` | UUIDs and ids labelled account, org, owner, tenant, workspace, team |
| Secrets | `<SECRET-n>` | API keys, tokens, passwords, bearer strings, private keys, values of `*_KEY`, `*_TOKEN`, `*_SECRET`, `PASSWORD`, `Authorization` |
| Hosts and addresses | `<HOST-n>` | private hostnames, IP addresses, internal URLs; public package and docs domains stay |
| Home paths | `~` | any path under a home directory becomes `~/...`, dropping the account name, including escaped forms such as `C:\\Users\\name` |
| Repositories | `<REPO-n>` | repository names, slugs and remote URLs, unless the user named them public |
| Proprietary terms | `<PROPRIETARY-n>` | each term the user listed, whole word, any case |

Omit opaque encrypted payloads, keeping their record identity, and note the omission. If a
value's category is unclear, ask; do not invent a broader category.

## Audit, then check the evidence

1. **Privacy audit.** Read every bundle file again (check its size first; read large files in
   chunks) and search for each original value and each category pattern. Any miss goes back to
   the scrub; repeat until the audit is clean. A subagent may run the audit when delegation
   allows; it reports `CLEAN` or `MISSED <file>:<line> <category>` without the value.
2. **Evidence check.** For each finding the report cites, open the cited line in the bundle and
   confirm it still supports the claim. Where redaction removed the support, name the finding
   and the limitation; never keep a sensitive value to save a finding.
3. **Scrub log.** Write `scrub-log.md`: a table of placeholder, category and count, recounted
   on the final files (excluding the log). Never write an original value or a replacement map
   into it.
4. Reconcile the report, case file and bundle list after any change, and repeat the affected
   checks.

## Hand over

Show the file list, the scrub log, the privacy outcome (`CLEAN` or the unresolved misses) and
the evidence outcome (supported, or limited with the affected findings) as separate lines. Say
that scrubbing can miss things and the user must review every file. Create an archive
(`zip -r`, `tar -czf`) only after the user approved what they saw; never send or upload it.

## Issue draft

For gate 8, when involvement is `possible` or `likely`, or the user asks:

1. Find the repository that owns the involved skill, hook or plugin from its install path,
   manifest or README. Do not guess an owner.
2. Search its open and closed issues for the symptom (`gh search issues --repo <owner>/<repo>
   "<terms>"`, or the public search URL when `gh` is unavailable) and show the matches; suggest
   adding the report to the closest one.
3. If none fits, write `issue.md` in the workspace:

   ```markdown
   ## Summary (written by the user)
   <the user's own two or three sentences; leave this for them to fill>

   ## What happened
   <the verdict with `path:line` citations from the report>

   ## Environment
   <harness and version, skill name and version or commit, OS; with provenance labels>

   ## Evidence
   <the involvement label and its lines; the findings that support it; no proposed fix>

   ## Bundle
   <"available on request" or "attached by the reporter">

   _Drafted with andino-session-diagnostics from a local session report._
   ```

4. Show the exact text. Create the issue only after the user approves it and has written the
   summary. A bundle cannot be attached by the CLI; give the user its path to attach in the
   browser.

Adapted from obra/superpowers `diagnosing-superpowers` (b739a8a, MIT): redaction policy, scrub
and audit prompts, bundle README and issue template, with the superpowers tracker replaced by
the repository that owns the involved skill.
