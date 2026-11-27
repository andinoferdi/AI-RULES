# Guard hook for destructive and publishing Git commands

A Claude Code `PreToolUse` hook that stops shell commands which push, hard-reset, clean
untracked files, force-delete branches or throw away local changes, before they run. Install it
only when the user asks for a guard, and only at the scope they name (default: this project).
It is a second line of defence: the agent still checks authority for every command.

## What it decides

| Command shape | Verdict |
| --- | --- |
| `git push` in any form, including `--force-with-lease` and `git -C <dir> push` | block |
| `git reset --hard`, `git reset --merge` | block |
| `git clean` with `-f` or `--force` in any flag group (`-fd`, `-xfd`) | block |
| `git branch -D`, `git branch --delete --force`, `-df` | block |
| `git checkout .`, `git checkout -- .`, `git restore .`, `git restore --worktree .` | block |
| `git checkout -f`, `git switch -f`, `git switch --discard-changes` | block |
| `git stash drop`, `git stash clear` | block |
| Any of the above behind `&&`, `;`, `|`, `sudo`, `env`, `VAR=value`, `bash -c "..."` or `pwsh -Command "..."` | block |
| `$(...)` or backticks in a command that mentions `git`; a command line that cannot be parsed | block |
| Hook input that is not JSON, or a Bash/PowerShell call without a string `command` | block |
| `git status`, `diff`, `log`, `commit`, `add`, `fetch`, `branch -d`, `checkout -b`, `restore --staged .`, `clean -n`, `stash list` | allow |
| Any command that does not run `git`, and any tool other than Bash and PowerShell | allow |

## Install (project scope)

1. Check the interpreter: run `python --version`, then `python3 --version` if the first fails. Use
   the name that prints a version 3.8 or later. If neither works, stop and tell the user the guard
   needs Python; do not fall back to a script that depends on `jq`.
2. Write the block below to `.claude/hooks/git_guard.py` in the project root.
3. Merge this entry into `.claude/settings.json` (create the file if it is missing). Keep every
   existing key: append to an existing `hooks.PreToolUse` list instead of replacing it, and leave
   `permissions` and other hook events as they are.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/git_guard.py\""
          }
        ]
      }
    ]
  }
}
```

   Replace `python` with the interpreter name from step 1. For the user's global scope, only when
   they ask for it, the same entry goes in `~/.claude/settings.json` with the script at
   `~/.claude/hooks/git_guard.py` and the command `python "$HOME/.claude/hooks/git_guard.py"`.
4. Verify by running it (next section). Commit the two files only when the user asks.

```python git-guard-hook
#!/usr/bin/env python3
"""Claude Code PreToolUse guard: block destructive or publishing git commands.

Exit 2 blocks the tool call and shows the reason to the agent; exit 0 lets it run. Input that
cannot be read, and a git command that cannot be classified, are blocked (fail closed).
"""
import json
import os
import re
import shlex
import sys

SHELL_TOOLS = {"Bash", "PowerShell"}
WRAPPERS = {"sudo", "env", "command", "exec", "time", "nohup", "nice"}
SHELLS = {"sh", "bash", "zsh", "dash"}
POWERSHELLS = {"pwsh", "powershell", "pwsh.exe", "powershell.exe"}
VALUE_OPTIONS = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--config-env"}
ALL_PATHS = {".", "./", ":/", ":/*", "*"}


def block(reason):
    print(f"BLOCKED by the git guard hook: {reason}. Ask the user to run this command "
          "themselves, or to approve it in words for this task.", file=sys.stderr)
    sys.exit(2)


def short_flags(args):
    return "".join(a[1:] for a in args if a.startswith("-") and not a.startswith("--"))


def reason_for(args):
    """Return why a git argument list is dangerous, or None when it may run."""
    i = 0
    while i < len(args) and args[i].startswith("-"):
        i += 2 if args[i] in VALUE_OPTIONS else 1
    if i >= len(args):
        return None
    sub, rest = args[i], args[i + 1:]
    flags = set(rest)
    if sub == "push":
        return "push publishes commits"
    if sub == "reset" and flags & {"--hard", "--merge"}:
        return "reset --hard discards work"
    if sub == "clean" and ("--force" in flags or "f" in short_flags(rest)):
        return "clean -f deletes untracked files"
    if sub == "branch" and ("D" in short_flags(rest) or (
            ("--delete" in flags or "d" in short_flags(rest))
            and ("--force" in flags or "f" in short_flags(rest)))):
        return "force-deleting a branch"
    if sub in ("checkout", "restore") and flags & ALL_PATHS:
        if not (sub == "restore" and "--staged" in flags and "--worktree" not in flags):
            return "discarding all local changes"
    if sub in ("checkout", "switch") and flags & {"-f", "--force", "--discard-changes"}:
        return "discarding local changes"
    if sub == "stash" and rest[:1] in (["drop"], ["clear"]):
        return "dropping stashed work"
    return None


def command_words(words):
    """Return ("git", args), ("nested", command) or None for one simple command."""
    i = 0
    while i < len(words) and (words[i] in WRAPPERS
                              or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", words[i])
                              or (i and words[i - 1] in WRAPPERS and words[i].startswith("-"))):
        i += 1
    if i >= len(words):
        return None
    head = os.path.basename(words[i].replace("\\", "/")).lower()
    rest = words[i + 1:]
    if head in SHELLS and "-c" in rest:
        position = rest.index("-c")
        return ("nested", rest[position + 1] if position + 1 < len(rest) else "")
    if head in POWERSHELLS:
        for position, word in enumerate(rest):
            if word.lower() in ("-command", "-c") and position + 1 < len(rest):
                return ("nested", " ".join(rest[position + 1:]))
    if head in ("git", "git.exe"):
        return ("git", rest)
    return None


def check(command, depth=0):
    if depth > 3:
        block("shell nesting is too deep to check")
    mentions_git = re.search(r"\bgit\b", command) is not None
    if mentions_git and ("$(" in command or "`" in command):
        block("command substitution around git cannot be checked")
    for segment in re.split(r"&&|\|\||[;|&\n]", command):
        try:
            words = shlex.split(segment, posix=True)
        except ValueError:
            if re.search(r"\bgit\b", segment):
                block("a command that runs git could not be parsed")
            continue
        found = command_words(words)
        if found is None:
            continue
        kind, value = found
        if kind == "nested":
            check(value, depth + 1)
            continue
        reason = reason_for(value)
        if reason:
            block(f"{reason} ({segment.strip()})")


def main():
    try:
        data = json.loads(sys.stdin.read())
    except (ValueError, UnicodeDecodeError):
        block("the hook input is not JSON")
    if not isinstance(data, dict) or not isinstance(data.get("tool_name"), str):
        block("the hook input has no tool name")
    if data["tool_name"] not in SHELL_TOOLS:
        sys.exit(0)
    tool_input = data.get("tool_input")
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str):
        block("the hook input has no command")
    check(command)
    sys.exit(0)


if __name__ == "__main__":
    main()
```

## Verify by running it

From the project root, feed it payloads and read the exit code (2 blocks, 0 allows). In Bash:

```bash
for c in "git push origin main" "git -C . push" "echo ok && git push" "git reset --hard" \
         "git clean -fd" "git branch -D old" "git checkout ." "git restore ." \
         "git status" "git commit -m save" "git branch -d done"; do
  printf '{"tool_name":"Bash","tool_input":{"command":"%s"}}' "$c" \
    | python .claude/hooks/git_guard.py 2>/dev/null; echo "$? $c"
done
echo 'not json {' | python .claude/hooks/git_guard.py 2>/dev/null; echo "$? malformed"
```

Expected: `2` for the first eight lines and for `malformed`, `0` for `git status`, `git commit`
and `git branch -d`. Put the observed table in the reply. A row that differs means the guard is
not ready: fix it before reporting it installed.

## What it cannot catch

- Git aliases (`git config alias.p push`, then `git p`) and scripts or Makefile targets that run
  git internally.
- Tools other than Bash and PowerShell, and commands a user runs outside Claude Code.
- A user or project setting that disables hooks.

Say these limits in the reply. Permission deny rules (`"deny": ["Bash(git push:*)"]`) can sit
beside the hook as a second layer; they match command prefixes only, so they are not a
replacement for it.
