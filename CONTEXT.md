# AI-RULES

AI-RULES installs first-party agent skills into coding hosts such as Codex, Claude
Code, OpenCode and Antigravity.

## Language

**Skill**:
A directory with a `SKILL.md` that a host loads. Each first-party skill is
developed on its own orphan branch with the same name.
_Avoid_: Plugin, package (except for the installed directory)

**Skill branch**:
The branch that holds one skill's content, for example `council`. Its head can be
ahead of what users receive.

**Family**:
A skill that ships internal methods inside one package, such as `threejs-skills`
and the `andino-workflow` members.

**Pin**:
The commit of a skill recorded in `release_manifest.json` on `main`. CI, the tests
and `ai-rules setup` use the pin, never the branch head.
_Avoid_: Version tag, latest

**Validation ref**:
A pinned branch used only by checks, not installed. `WebBased` is the source for
the Focus reference drift check.

**Promote**:
Move a pin to a newer skill commit through a `promote/<skill>` PR whose CI passed.
Started with `python scripts/promote_skill.py <skill>`.

**Drift**:
Commits on a skill branch that are not pinned yet. Reported by
`python scripts/skill_refs.py drift`; drift never fails CI.

**Main checks**:
The model-free checks in `scripts/ci_checks.py`. CI and the promote command run
the same list.

**Latest source**:
`ai-rules setup --source latest` (the default): fetch the pins from GitHub `main`
at install time, so a merged promotion reaches users without a new installer
release.

**Bundled source**:
`ai-rules setup --source bundled`: use the pins frozen into the running
executable.
