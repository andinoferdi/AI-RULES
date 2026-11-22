# Boundary implementation and audit details

Open the section that matches the traced effect. Use synthetic data and a
controlled environment for probes.

## Inputs, queries, output and uploads

Use schemas with allowlisted shapes, types, ranges and lengths. Consume the
parsed result exclusively. Bind query values and allowlist dynamic identifiers.
Avoid shell interpretation by invoking a fixed executable with separate arguments.
Use contextual output escaping and vetted allowlist sanitization for necessary
raw HTML. For uploads, enforce size before buffering, inspect content when
format matters, and use server-owned names and storage paths. Test a valid
request and an injection or oversized input. Check the query, renderer or file
store for unintended effects.

## Authentication, sessions and resource access

Check authentication and per-action authorization for the specific tenant and
object on every entry point, including batch handlers, downloads and workers.
Scope the lookup or mutation by authorized tenant and resource together. Verify
same-tenant access, an authenticated cross-tenant request and an unauthenticated
request. Inspect response fields and side effects.

Use an appropriate Argon2, scrypt or bcrypt work factor for passwords. Keep
browser session cookies HttpOnly and Secure with bounded expiry, and verify
SameSite and CSRF behavior for the actual login and write flows. Check relevant
response headers, including CSP and HSTS where applicable, and allowlist CORS
origins for credentialed requests. CORS controls browser response access.
Enforce authorization and CSRF protections separately. Use a shared rate-limit
store across replicas and test limits across instances.

## Outbound requests

For user-influenced destinations, allowlist HTTPS scheme, host and port, reject
credentials and disable redirects. Resolve all A and AAAA records and reject
nonpublic or reserved destinations, including loopback, link-local and cloud
metadata addresses. DNS can change between validation and connection. Pin the
validated address or enforce the destination at the transport for exposed
fetchers. Use a fake resolver and transport to test a permitted host, mixed
public and private answers, and an attempted redirect. Assert the forbidden
destination receives no connection.

## Destructive paths

Resolve symlinks and require a strict descendant of an allowlisted root.
Verify ownership against a trusted job record or integrity-protected evidence
before the call. A marker writable by the same actor that chooses the path
can be forged. If an attacker can swap ancestors between check and use, use
an immutable hierarchy or descriptor-relative no-follow operations supported
by the platform. Refuse without falling back to a broader target. Test an owned
leaf, the root itself, a path resolving outside the root and a mismatched
owner. Use a spy to verify refused inputs never reach the mutation.

## Dependency installation and audit

Identify the workspace installation boundary. Corroborate the pinned manager
version, authoritative lockfile and CI. Resolve conflicts before changing
dependencies. Start with scripts blocked before the first install. Inspect
exact source and version, approve only required scripts through native policy,
then verify a clean frozen install. Review maintainer, release, provenance,
signature, transitive and lookalike-package risks.

Audit the committed lockfile with the native tool. Triage known advisories by
reachability through runtime, build, test or deploy, and fix availability.
Review changes and test upgrades before accepting them. Record reason and
review date for deferrals. Avoid automatic force-fixes and blanket script
approval. An audit result covers known advisories.

## Secrets, responses and personal data

Keep credentials in approved runtime secret storage, redact logs and use
placeholder examples. Check the staged changes and use a disposable sentinel
to test redaction. If a real secret reached a remote, follow authorized incident
handling and prioritize rotation before history cleanup. Allowlist response
fields and keep internal error details out of client responses.

Classify personal data and limit collection to a stated purpose. Define
retention and exercise export and deletion across primary stores, caches,
indexes and backups according to the retention policy. Verify applicable
consent, third-party processing and regional requirements with current
authority. Use synthetic records for evidence.

## LLM outputs and tools

Treat prompts, retrieved documents and model outputs as untrusted. Validate
structured output and enforce tool arguments, tenant scope and permissions in
code before execution. Keep secrets out of context, isolate tenant retrieval
and bound tokens, rate and recursion. Apply the existing authority checks to
destructive actions. Put an instruction into a synthetic retrieved document
that asks the model to read another tenant's data. Assert the tool layer denies
the call and no result reaches the model or client.

## Worked finding

Illustrative case for a tenant invoice API. **High severity, confirmed in the
fixture.** The authenticated download handler uses a route-supplied invoice ID
in an ID-only lookup. A tenant A user who knows tenant B's invoice ID can read
billing data. Scope the lookup to both the authenticated tenant and invoice ID.
In the fixture, send requests for one invoice in each tenant. Verify tenant
A's own request succeeds, the other returns the application's standard denial,
and the denied response contains no invoice data. A passing fixture establishes
only the tested path. Check alternate download routes before broader sign-off.

Provenance: independently worded adaptation of the Addy snapshot identified in the owning GUIDE.md; full MIT notice at [../references/license.md](../references/license.md). No upstream installation or hook is required.
