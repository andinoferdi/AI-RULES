# Worked Example: Customer Export

The user asks for a customer export. The existing job streams tenant-scoped CSV
asynchronously. Audit users cannot read customer emails.

## First message: findings, then why

The request says what, but not for whom or why. The agent reads the export job and the role
definitions before writing anything, then sends:

> You'd like customers to be able to export their customer list. The app already has a background
> job that writes tenant-scoped CSV files, so the file itself is mostly built. What I can't tell
> from the code is who needs the file and what they do with it, and that decides who may request
> it and where it goes. My guess is someone in finance checking records against another system.
> What will the person who downloads it use it for?

One question, a guess with its reason, and no list of export formats. The user replies that
account owners reconcile customer records every quarter.

## Ground the next decision

> The existing export job already handles tenant-scoped CSV. Since audit users
> cannot read customer emails today, I recommend limiting the first release to
> account owners so the export follows the existing access boundary. Should
> account owners be the only users who can request it?

The user replies **“Yes.”** Record owner-only access as confirmed. The answer's
length does not make it ambiguous.

## Follow the dependency

The user wants the file for quarterly reconciliation and asks to start building.

> Account owners are confirmed. For reconciliation, I recommend letting the
> requesting owner download the file from the account rather than creating a
> shareable URL. That keeps access within the account after the job finishes.
> Does reconciliation require sending the export to someone outside the account?

A link expiry decision becomes relevant only if the user chooses sharing. The
user confirms that account access is enough and delegates the file lifetime
within the existing export retention policy. Inspect that policy before recording
the chosen lifetime. If it cannot be verified, keep file lifetime open.

## Play back the design

> Account owners request a tenant-scoped customer CSV for quarterly
> reconciliation. The existing job generates it asynchronously. The requesting
> owner downloads it inside the account, and the existing export retention policy
> governs when it is removed. An audit user and an owner of another tenant must
> both be denied access, including by direct download URL. Does this design match
> what you want to hand off for planning?

After confirmation, document the job and download authorization boundaries and
the failure behavior for an expired file. An ADR can preserve the decision to
avoid external sharing if future work might revisit it. Record domain terms only
where their meaning affects behavior, such as whether “owner” is the platform's
account role or the person who requested the file.

## The restate the user confirmed

```markdown
- Outcome: account owners download their customer list as CSV for reconciliation
- User: account owners of each tenant
- Why now: quarterly reconciliation is done by hand today
- Success: an owner gets the file from the account without asking support
- Constraint: tenant isolation and the audit role's email restriction stay as they are
- Out of scope: shareable links, scheduled exports, formats other than CSV
```

The file lifetime is the agent's call under the existing retention policy, marked as such in the
design. The external-sharing decision gets an ADR only if the user expects it to be revisited:
reversing it later would change who can see customer data, which is hard to reverse and would
surprise a reader.

## Anti-pattern

The same request answered with "Sure. CSV or Excel? Which columns? Should it be scheduled? Who
should have access? Do you want a download link by email?" asks five things at once, offers a menu
before the why is known, and asks nothing the code answers better (the job already writes CSV).
Each answer arrives without the reason behind it, so the agent still cannot make the small calls
the user never mentions.
