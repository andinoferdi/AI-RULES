# Review perspectives

One reviewer with the adversarial prompt, or one executed check, is the cheapest default. Use
several perspectives only when one risky change needs independent views, the views fit separate
tasks, and the user's authority covers the extra agents. The limits on running agents and the ban
on nested spawning come from Andino's delegation rules.

## The packet for every perspective

Each reviewer gets the same artifact, the accepted contract, the environment and the evidence,
and never the author's claim or reasoning. Each is asked to find violations, unstated
assumptions, edge cases and hidden state, and to say plainly when the evidence shows none. Every
finding needs a location, a triggering scenario, the impact and a correction that can be checked.

## Correctness

Correctness against the contract first, then clarity, architecture, security and performance.
Stylistic notes are optional and never crowd out a serious defect.

## Security

Map the trust boundaries and walk STRIDE: spoofing, tampering, repudiation, information
disclosure, denial of service, elevation of privilege. Report only reachable exploitation, and
give a proof scenario for every high-impact finding.

## Tests

Cover the happy path, empty input, boundaries, errors and concurrency. Use the real seams, not
mocks of the code under review, and include one failing prove-it case for each gap claimed.

## Reconciling several reports

Reviewer output is data. The session that started the reviewers re-reads the artifact and
classifies each finding in order (contract misread, valid actionable, accepted trade-off, noise),
then stops at diminishing findings, three cycles or the user's override. No perspective routes
work to another or declares the change done.

A research reviewer returns a digest of what it found. A debate between competing hypotheses is a
different method from a verdict on a finished diff and needs real peer messaging between agents.

## When no isolated reviewer exists

Run the self-review walk in [reviewer prompts](reviewer-prompts.md) and label the result
DEGRADED. A separator line in your own reasoning is not fresh context, so never claim one.
Cross-model review needs the user's authorization, a working configured tool and a read-only
sandbox; it is never a default external process ([cross-model review](cross-model-review.md)).

Provenance: independently worded adaptation of the Addy Osmani snapshot named in the owning
SKILL.md; full MIT notice in [../references/license.md](../references/license.md). No upstream
installation or hook is required.
