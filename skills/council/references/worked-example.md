# Worked example

A synthetic run that shows the shape of each stage. The scenario, excerpts and
ranking are illustrative, not results from a real council. It deliberately uses
a decision outside `evals/council.json` so trials of those cases stay independent.

## Request

> Council this: our team of four runs CI on a self-hosted Jenkins box. Builds take
> 25 minutes and the box failed twice last month. Move to GitHub Actions now, or
> fix Jenkins first? A client demo is in three weeks.

## Context and brief

Context read: the user's message only. The project has no CI notes and the user
named no files.

```text
Decision: move CI to GitHub Actions now, or stabilize Jenkins first.
Option 1: migrate now. Option 2: fix Jenkins, migrate after the demo.
Option 3: keep Jenkins.
Facts: team of four [reported]; builds take 25 minutes [reported]; two outages
last month [reported]; client demo in three weeks [reported].
Unknown: cause of the outages; Actions cost at this build volume; whether any
pipeline step depends on the Jenkins host.
Criteria: demo risk, build time, maintenance load, cost, reversibility.
```

## Run plan announcement

> Council plan: 5 advisors (mid-tier model, medium effort) in waves of 3 and 2,
> then 3 reviewers (mid-tier model, low effort) in one wave. I chair. 8 sub-agents
> in total. Proceed?

## Advisor excerpts

- **Contrarian:** prefers Option 2. "Migrating during the three weeks before a demo
  turns a known flaky system into an unknown one [assumption]. The outage cause is
  [unknown]; if it is a disk issue, a one-day fix removes most of the risk."
- **Executor:** prefers Option 2 with a time box. "Spend one day finding the outage
  cause. Port one pipeline to Actions in parallel as a test, without switching."
- **Expansionist:** prefers Option 1. "Hosted runners remove the box entirely, and
  parallel jobs could cut the 25 minutes [assumption, depends on test split]."

## Review excerpt

One of the three reviews. After all reviews arrived, the chair revealed that
Response C was the Executor and Response A the Expansionist.

> 1. Response C is strongest: it ties the choice to demo risk and proposes a
>    reversible test.
> 2. Response A assumes Actions will be faster, but the brief has no evidence on
>    where the 25 minutes go.
> 3. No response asks who on the team of four owns CI today.
> FINAL RANKING: C, E, B, A, D

## Verdict

```markdown
## Council Verdict: CI before the demo
**Recommendation:** Fix Jenkins first and port one pipeline to Actions as a side
test. The demo in three weeks makes a full switch the riskier move, and the
outage cause is still unknown.

### Where the council agrees
- The outage cause is the deciding unknown; four of five advisors named it.

### Where the council clashes
- Expansionist wants to migrate now for speed. The speed gain is an assumption
  until someone measures where the 25 minutes go.

### Blind spots from review
- Nobody knows who owns CI on the team, so a migration has no clear owner.

### What would change the verdict
- If the outages come from the host itself and cannot be fixed in a day, migrate
  now and accept the demo risk.

### First action
Spend one day finding the cause of last month's two outages.

_Run: 5 advisors and 3 reviewers (mid-tier model; medium and low effort), main agent as chair; ranking tally C first in 3 of 3 reviews; context read: user message only._
```
