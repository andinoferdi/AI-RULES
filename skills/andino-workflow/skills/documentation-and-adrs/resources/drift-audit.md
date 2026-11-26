# Drift audit

Use this when a document may no longer match the code it describes. Commit order tells you
where to look; reading each claim against the code decides. Report "can't tell" when history
cannot order the two, and never upgrade it to "current".

## 1. Pair each document with its code

Take the code paths from the document itself (the files, modules or endpoints it names). When
it describes several files, use all of them: the newest commit across the set counts.

## 2. History verdict from commit order

Run from the repository root. Both versions print one of four verdicts.

Bash or Git Bash:

```bash
doc="docs/modules/export.md"
code="src/export.py"            # several paths: code="src/export.py src/formats.py"
d=$(git log -1 --format=%H -- "$doc")
c=$(git log -1 --format=%H -- $code)
if [ -z "$d" ] || [ -z "$c" ]; then echo "can't tell"
elif [ "$c" = "$d" ]; then echo "changed together"
elif git merge-base --is-ancestor "$d" "$c"; then echo "code changed after the document"
elif git merge-base --is-ancestor "$c" "$d"; then echo "document changed after the code"
else echo "can't tell"; fi
```

PowerShell:

```powershell
$doc = 'docs/modules/export.md'
$code = @('src/export.py')       # several paths: @('src/export.py', 'src/formats.py')
$d = git log -1 --format=%H -- $doc
$c = git log -1 --format=%H -- $code
if (-not $d -or -not $c) { "can't tell" }
elseif ($c -eq $d) { 'changed together' }
else {
    git merge-base --is-ancestor $d $c
    if ($LASTEXITCODE -eq 0) { 'code changed after the document' }
    else {
        git merge-base --is-ancestor $c $d
        if ($LASTEXITCODE -eq 0) { 'document changed after the code' } else { "can't tell" }
    }
}
```

Check `git rev-parse --is-shallow-repository` first: `true` means missing history, so every
verdict is "can't tell" until the history is fetched.

| History verdict | What it means | What it does not mean |
| --- | --- | --- |
| changed together | One commit last touched both. | That the commit updated the document correctly. |
| code changed after the document | The code moved since the document was last edited. | That the document is wrong: a refactor or rename can leave every claim true. |
| document changed after the code | Someone edited the document after the last code change. | That the document is right: the edit may have touched another section. |
| can't tell | Neither commit is an ancestor of the other (parallel branches joined by a merge, a rebase), a path has no commit, or the clone is shallow. | Anything about accuracy. Never report it as current. |

## 3. Content verdict

List every factual claim in the document: numbers with units, defaults, limits, names, error
codes, conditions, order of steps. For each, find the code line or test that settles it.

- **Accurate**: every claim matches the code.
- **Wrong**: at least one claim contradicts the code. Quote the claim and the line.
- **Unverifiable**: a claim depends on something outside the repository (a service, a deployed
  setting). Say what would settle it.

The content verdict decides the action. History only sets the order in which you look: start
with "code changed after the document", then "can't tell", then the rest. Every document in
scope still gets a content check.

## 4. Report table

```markdown
| Document | History verdict | Content verdict | Evidence | Action |
| --- | --- | --- | --- | --- |
| docs/modules/export.md | code changed after the document (a1b2c3d) | wrong: "CSV only" vs `FORMATS = ("csv", "xlsx")` in src/export.py | git log; src/export.py:4 | fixed, change-log entry added |
| docs/modules/auth.md | can't tell (merge of parallel branches) | accurate | src/auth.py:3 | none |
```

## 5. Fixing and logging

Correct only the claims marked wrong. When the document keeps a change log, append one entry at
the end of the existing list, dated today, saying what changed and why:

```markdown
- 2026-11-26: Export formats corrected to CSV and XLSX; `FORMATS` gained "xlsx" in a1b2c3d.
```

Leave every earlier entry byte-identical, typos included. An accurate document gets no edit and
no entry.

## 6. Keeping documents from drifting again

When the user asks for prevention, pick the lightest mechanism the project will keep running:

- A pairing list (for example `docs/doc-map.txt`, one `doc: code paths` line each) that reviewers
  and the audit above read.
- A pull-request checklist line: "Changed behaviour has its document updated, or the PR says why
  not."
- A CI check that fails when a paired code path changed in the branch and its document did not,
  with an explicit override (a label or a line in the PR body). Start from
  `git diff --name-only origin/main...HEAD` and the pairing list. Setting this up changes CI and
  needs the same authority as any CI change.
