# Worked Example: Customer Export

The user asks for a customer export. The existing job streams tenant-scoped CSV
asynchronously. Audit users cannot read customer emails.

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
