# Evaluation contract

Read at gates 4, 6 and 7: what the evaluation record holds, how to label self-review, how to
write the runbook, and what to check before a skill ships.

## Evaluation record

Keep one record per skill change, next to the scenarios or in the task's existing evidence. One
row per scenario and arm:

| Scenario | Arm | Status | Evidence | Result |
| --- | --- | --- | --- | --- |
| S2 generator missing | no skill | OBSERVED (incident 3) | "I'll regenerate after the demo" | FAIL |
| S2 generator missing | candidate | SELF-REVIEW | Rule line 1 and excuse row 2 stop the edit; step 3 reports the blocker | PASS (self-review) |
| S2 generator missing | candidate | NOT RUN | Runbook below | — |

Arms are: no skill; the current skill, for a revision; the candidate. Statuses:

- **RUN**: a fresh agent ran the scenario; the evidence quotes its transcript or output.
- **OBSERVED**: the evidence quotes a real incident or sample (remedial baselines).
- **SELF-REVIEW**: you applied the PASS and FAIL lines to what the skill leads to. Name the skill
  line that decides the result. Never present it as independent.
- **NOT RUN**: nothing was executed; say why (no fresh agent available, not authorised).

A record with only SELF-REVIEW and NOT RUN rows leaves agent behaviour not verified, and the
report says so in its "Not verified" line.

For a revision, apply the criteria to the same input for the current skill and the candidate:
write the output each version leads to (for an output-shape skill, the actual output for one
real sample), and score both against the same PASS and FAIL lines. A comparison where only the
candidate was scored is not a comparison.

## Runbook

The runbook lets someone with a fresh agent repeat the evaluation without asking you:

```markdown
## Runbook: <skill name>
Scenarios: <path>
Arms: no skill | current skill (<path or commit>) | candidate (<path or commit>)
For each scenario and arm:
1. Start a fresh agent with the same tools and repository state as the scenario's Setup line.
2. Install only that arm's skill (none for the control).
3. Send the scenario's Prompt verbatim.
4. Record the actions taken and any reason the agent gave, quoted.
5. Score against the PASS and FAIL lines; read every match yourself.
Done when: every scenario has a RUN row for every arm.
First to run: <the scenario most likely to fail, and why>
```

## Machine-readable record (optional)

When a project keeps evaluation data as JSON, use these fields. The values below are an
illustration, not a result:

```json
{
  "skill": "proto-regeneration",
  "mode": "remedial",
  "scenarios_path": "evals/proto-regeneration.md",
  "arms": ["no-skill", "candidate"],
  "results": [
    {"scenario": "S2", "arm": "no-skill", "status": "OBSERVED", "evidence": "incident 3", "result": "FAIL"},
    {"scenario": "S2", "arm": "candidate", "status": "SELF-REVIEW", "evidence": "rule line 1", "result": "PASS"}
  ],
  "agent_behaviour": "NOT_VERIFIED",
  "runbook": "evals/proto-regeneration.md#runbook"
}
```

## Packaging checks (gate 7)

- The frontmatter `name` matches the folder and the repository's naming rule; the description
  starts with the trigger and stays inside the host's limit (1024 characters for portable
  skills; less if the repository says so).
- Every relative link resolves from the folder the skill is installed to, not only from the
  source tree. Bundled scripts are invoked through their interpreter (`python scripts/x.py`),
  never by bare path, since some packagers drop executable bits.
- No symlinks, credentials, personal configuration or empty placeholder files in the skill.
- The discovery probes from gate 1 are recorded: the request that must load the skill and the
  nearby one that must not, each as probed (with what happened) or NOT RUN (with the prompt).

In the AI-RULES repository (`andino-workflow` members):

- Member skills live at `skills/andino-workflow/skills/<id>/` with `SKILL.md`, a `GUIDE.md` that
  equals the `SKILL.md` body, and Markdown under `resources/`, `references/`, `templates/` or
  `examples/` only.
- Run `ai-rules setup` from the clone: it prints `Skill source: local folder ...` and installs
  uncommitted edits, which is how to try a change before the PR.
- Update counts, inventories, allow-lists and evals the change affects in the same commit, then
  run `python scripts/ci_checks.py --group skills`.

## Deployment checklist, per skill

Finish this for one skill before starting the next:

- [ ] routing table complete, routed items moved to their homes;
- [ ] scenarios saved, each with PASS and FAIL lines;
- [ ] baseline recorded (RUN, OBSERVED or NOT RUN with reason);
- [ ] skill written; every skill row maps to a line; working behaviour kept;
- [ ] evaluation record complete; runbook written when any row is SELF-REVIEW or NOT RUN;
- [ ] packaging checks pass;
- [ ] report written with the "Not verified" line filled in honestly.

Committing, pushing and opening a PR follow the user's authority, not this checklist.
