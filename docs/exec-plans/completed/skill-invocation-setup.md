# Skill invocation setup

Status: DONE
Depth: LITE
Current Phase: complete
Date: 2026-10-02

## Objective and outcome

A new user can run setup once, select agents and a profile, and invoke the
installed first-party skills in a fresh agent session without installing skills
beforehand. Setup registers OpenCode commands and Antigravity IDE workflows,
repairs missing registrations, preserves existing valid commands, and blocks
invalid existing files. Codex, Claude Code and Antigravity CLI retain native
skill discovery. Setup prints each selected host's invocation names.

## Decisions and evidence

- Skill directories remain the canonical instructions. Commands/workflows read
  the installed SKILL.md and resolve its supporting files relative to that directory.
- Antigravity IDE compatibility covers modern config/workflows and the installed
  older IDE's antigravity/global_workflows directory. No third-party bootstrap is installed.
- Full repository suite: 123 tests pass, including interactive setup from an empty
  home outside the repository for all five hosts and all three skills.
- [Clean-install evidence](../../validation/installer/clean-install-discovery.json):
  built wheel plus actual source branches produces 15 INSTALL actions and verified
  locks; a second setup produces 15 NO_OP actions. Fresh Claude Code/OpenCode
  discovery recognizes all three commands; Codex recognizes all three enabled
  skills from a separate fresh project installation.
- Codex Windows global discovery still reads OS-profile roots despite overridden
  HOME/USERPROFILE. Isolated global runtime discovery is not claimed. Antigravity
  checks cover artifacts; live UI autocomplete remains NOT_RUN. No model turn was sent.

## Final repository cleanup

Generated src/ai_rules.egg-info metadata is removed from Git while retained locally;
the existing ignore rule already covers it. Completed checkpoint archived here,
session-specific publication notes removed from evidence, and generated Python
caches removed after verification. The capability-integration checkpoint and
reviewed validation records remain because live acceptance and tooling still use them.
Package, evaluation-schema, requirement-traceability and saved-record checks pass.
Local documentation links and whitespace checks pass; no new credential patterns found.
The user authorized inclusion of the installer changes, cleanup, commit and normal
push to main's existing origin/main upstream.

## NEXT ACTION

None for implementation/cleanup. Commit and upstream state provide publication
evidence; Antigravity live autocomplete remains a documented follow-up verification.
