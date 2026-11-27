# Stage contract

Every stage of a human procedure, whether it is a script screen or a checklist section, carries
the fields below. The script requirements and shell table say how to build them; the two
`.env` snippets at the end are executed by the AI-RULES test suite
(`tests/test_human_procedure_snippets.py`), so copy them as they are.

## Stage fields

| Field | What the person sees |
| --- | --- |
| Stage N of M · outcome | One outcome per stage, in words the person uses ("Save the Inkwell API keys") |
| Before you start | Account, workspace or environment, and anything that must already be true |
| Open | The confirmed URL, printed even when the script opens it, or the exact command and where to run it |
| Do | The click path or command with the exact labels from the source ("Developers → API keys → Reveal test key → Copy") |
| Enter | Each value: name, where it comes from, secret or public, where it is written (file, CI secret, CI variable, nowhere) and what reads it |
| Before you confirm | Only for an effect that is hard to undo: what changes, who notices, how to undo it or "cannot be undone", and the word to type |
| Done when | An observation the person can make that shows no secret value: a check command's `ok`, a status line, a DNS answer, a dashboard state |
| If interrupted | What to look at first on a re-run, and which branch follows from what they see |

A stage that captures no value (a toggle, an approval, a DNS edit) still has Do, Done when and
If interrupted. A stage whose path is not confirmed says so in Do: "Not documented: find the
API token page in your Relay account; the token starts with `rl_`. Write down the clicks
afterwards."

## Screen layout for a script

```text
▸ Stage 2 of 6 · Save the Inkwell API keys
  Opening https://app.inkwell.example/settings/api-keys
  (if no browser opens, paste that address into one)
  • Public key row → Copy (starts ink_pub_)
  Paste the public key: ▌
  • Secret key row → Show → Copy (starts ink_sec_)
  Paste the secret key (hidden): ▌
  ✓ wrote INKWELL_PUBLIC_KEY, INKWELL_SECRET_KEY → .env
  Done when: python scripts/check_config.py shows both keys as ok
```

Clear the screen at each stage so only the current one shows; skip clearing when output is not
a terminal. The first screen says what the procedure will change (files, remote targets) and
how to stop (Ctrl-C) and resume. The last screen lists what was written, what was skipped and
why, and what is left for the person.

## Checklist template

```markdown
# <Outcome> (<operator, machine, shell>)

Changes: <files and remote targets>. Cannot be undone: <stages, or "none">.
Stop at any point; to resume, start at the first stage whose Done when is not true.

## Stage 1 of M · Find out what already happened (changes nothing)
Check: <each effect that may already exist, with the command or screen that shows it>
Then: <observation> → go to Stage <n>; <observation> → skip to Stage <n>; anything else → stop
and send me <non-sensitive result>.

## Stage 2 of M · <outcome>
Open: <URL or command>  Do: <exact steps>  Enter: <name → destination, secret or public>
Before you confirm: <consequence, undo>  Done when: <observation>  If interrupted: <check>

## When you are done
Send me: <the non-sensitive lines that prove each Done when>.
```

## Script requirements

Check the script against each line before handing it over.

- [ ] Written for the operator's shell: bash 3.2 on a stock Mac (no `declare -A`, `${var,,}`,
  `mapfile`, `readarray`), Windows PowerShell 5.1 when that is all the laptop has (no `&&`,
  `||`, `??`, `?:` or `-Parallel`; ASCII-only source unless saved as UTF-8 with BOM).
- [ ] The first stage changes nothing and finds out what already happened; every later stage
  that has an effect first checks whether the effect is already there.
- [ ] Each URL is opened or printed before its value is asked for, with the manual-open line.
- [ ] Secret values are read with hidden input, never echoed, never put on a command line,
  in a log, in a progress file or in the closing summary.
- [ ] `.env` writes go through the snippet below: other lines untouched, the key replaced in
  place, a symlinked file refused, the file mode kept, a new file created private.
- [ ] Every remote write (GitHub secret or variable, dashboard API) names its exact target,
  is shown before it happens and runs only after the person types `yes`.
- [ ] Every effect that is hard to undo states its consequence and undo, and runs only after
  the person types a stage-specific word (`MIGRATE`, `DELETE`).
- [ ] A stage counts as done only after its Done when was observed. Progress, if recorded,
  holds stage names and times only. A re-run never repeats a completed effect that is hard
  to undo, and an effect whose outcome is unknown is checked before anything is retried.
- [ ] End of input (Ctrl-D, closed pipe) stops the script without marking the stage done.
- [ ] The closing screen lists written values by name, remote targets set, skipped items with
  the command to finish them by hand, and the evidence to send back.

## Shell table

| Need | bash 3.2 (macOS, Linux, Git Bash) | Windows PowerShell 5.1 |
| --- | --- | --- |
| Hidden input | `read -r -s -p 'Paste the secret key (hidden): ' v; echo` | `$s = Read-Host 'Paste the secret key (hidden)' -AsSecureString` then `$v = [Runtime.InteropServices.Marshal]::PtrToStringBSTR([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))` |
| Open a URL | `open "$u"` (macOS), `xdg-open "$u"` (Linux), else print it | `Start-Process $u`, and print it too |
| Clear the screen | `[ -t 1 ] && clear` | `Clear-Host` |
| Typed confirmation | `read -r -p "Type MIGRATE to run the migration: " a; [ "$a" = MIGRATE ]` | `if ((Read-Host 'Type MIGRATE to run the migration') -ne 'MIGRATE') { ... }` |
| GitHub secret | `printf '%s' "$v" \| gh secret set NAME --repo OWNER/REPO` (gh reads stdin when `--body` is absent) | `gh secret set NAME --repo OWNER/REPO` with no `--body`: gh prompts and the person pastes the value into gh itself |
| GitHub variable (public) | `gh variable set NAME --repo OWNER/REPO --body "$v"` | `gh variable set NAME --repo OWNER/REPO --body $v` |
| Syntax check | `bash -n script.sh`; `shellcheck script.sh` when installed | `[void][System.Management.Automation.Language.Parser]::ParseFile($p, [ref]$null, [ref]$e); $e` prints nothing |

GitHub Actions reads repository secrets and variables in every job, environment jobs included;
an environment's own value with the same name takes precedence. Set the repository level
unless the workflow's environment already holds values or the person asks for the environment
level, and say which one you chose.

## Snippets for `.env` writes

Both write `KEY=value` when the value contains only `A-Z a-z 0-9 _ . / : @ + = , -`, write
`KEY='value'` otherwise, and refuse a value with a single quote or a line break (the person
edits the file by hand). A later duplicate of the key is removed. Lines keep their bytes and
line endings; a missing final newline is added.

Bash: set `ENV_FILE` first; the value never reaches another program's command line.

```bash hp-env-set
env_set() {  # env_set KEY VALUE: set KEY in $ENV_FILE; every other line stays as it was
  local key=$1 value=$2 line tmp rc
  case $value in *$'\n'*|*$'\r'*) echo "refusing: $key has a line break; edit $ENV_FILE by hand" >&2; return 1 ;; esac
  if [ -L "$ENV_FILE" ]; then echo "refusing: $ENV_FILE is a symlink; edit it by hand" >&2; return 1; fi
  case $value in
    *[!A-Za-z0-9_./:@+=,-]*)
      case $value in *"'"*) echo "refusing: $key contains a single quote; edit $ENV_FILE by hand" >&2; return 1 ;; esac
      line="$key='$value'" ;;
    *) line="$key=$value" ;;
  esac
  [ -e "$ENV_FILE" ] || (umask 077 && : > "$ENV_FILE") || return 1
  tmp=$(mktemp "$ENV_FILE.XXXXXX") || return 1
  KEY="$key=" LINE="$line" awk 'BEGIN { k = ENVIRON["KEY"]; l = ENVIRON["LINE"] }
    index($0, k) == 1 { if (!done) print l; done = 1; next } { print }
    END { if (!done) print l }' "$ENV_FILE" > "$tmp" && cat "$tmp" > "$ENV_FILE"
  rc=$?; rm -f "$tmp"; return $rc
}
```

Windows PowerShell 5.1 (also runs on PowerShell 7): call `Set-EnvValue -Path .env -Key NAME
-Value $v`; it throws on a refusal, so wrap it in `try { } catch { }` and stop the stage.

```powershell hp-env-set
function Set-EnvValue([string]$Path, [string]$Key, [string]$Value) {
  # Set $Key in the dotenv file at $Path; every other line stays as it was.
  $full = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Path)
  if ($Value -match "[`r`n]") { throw "refusing: $Key has a line break; edit $Path by hand" }
  $item = Get-Item -LiteralPath $full -Force -ErrorAction SilentlyContinue
  if ($item -and $item.LinkType) { throw "refusing: $Path is a link; edit it by hand" }
  if ($Value -match "[^A-Za-z0-9_./:@+=,-]") {
    if ($Value.Contains("'")) { throw "refusing: $Key contains a single quote; edit $Path by hand" }
    $line = "$Key='$Value'"
  } else { $line = "$Key=$Value" }
  $text = ''; if ($item) { $text = [System.IO.File]::ReadAllText($full) }
  $nl = "`n"; if ($text.Contains("`r`n")) { $nl = "`r`n" }
  $lines = @(); if ($text.Length) { $lines = @($text -split "\r?\n"); if ($lines[-1] -eq '') { $lines = @($lines[0..($lines.Count - 2)]) } }
  $out = New-Object System.Collections.Generic.List[string]; $done = $false
  foreach ($l in $lines) {
    if ($l.StartsWith("$Key=")) { if (-not $done) { $out.Add($line) }; $done = $true; continue }
    $out.Add($l)
  }
  if (-not $done) { $out.Add($line) }
  [System.IO.File]::WriteAllText($full, (($out -join $nl) + $nl), (New-Object System.Text.UTF8Encoding $false))
}
```
