# AI-RULES

AI-RULES installs first-party agent skills into coding hosts such as Codex, Claude
Code, OpenCode and Antigravity.

## Language

**Skill**:
A directory with a `SKILL.md` that a host loads. Every first-party skill lives in
`skills/<id>/` on `main`.
_Avoid_: Plugin, package (except for the installed directory)

**Family**:
A skill that ships internal methods inside one package, such as `threejs-skills`
and the `andino-workflow` members.

**Native member**:
An `andino-workflow` member that setup installs as its own skill
(`andino-<name>`) next to the workflow, with its own command.

**Local source**:
`ai-rules setup --source local`, or the default when run inside a clone: install
the clone's `skills/` folder as it is on disk, uncommitted edits included.

**GitHub source**:
`ai-rules setup --source latest`, or the default outside a clone: install
`main:skills/<id>` from GitHub at install time.
_Avoid_: Pin, promote (retired with the branch-per-skill layout)

**Bundled source**:
`ai-rules setup --source bundled`: the skills packaged inside a release
executable (in a clone without packaged skills, the clone's `skills/` folder).

**Validation ref**:
A pinned commit of another branch used only by checks, never installed.
`WebBased` is the source for the Focus communication reference check.

**Skill checks / installer checks**:
The two groups of `scripts/ci_checks.py`. Skill checks read real skill content;
installer checks use fixture data.
