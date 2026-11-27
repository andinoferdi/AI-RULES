# Boundary controls and the tests that prove them

Open the section that matches the effect you traced in gate 1. Each section gives the control
and the abuse cases gate 2 turns into tests. Use synthetic data and a controlled environment
for every probe.

## Testing that a control holds

A control is proven when the protected effect does not run for the abuse case, not when the
handler returns an error. Replace the effect with a recording fake at the seam the code already
has (an injected function, a module attribute the tests patch, a fake client) and drive the
case through the normal entry point. Assert three things: the denied call returns the project's
standard refusal, the fake recorded nothing, and the legitimate call still reaches the fake with
the expected arguments. Run the abuse test before the guard exists and keep its failing output.

```python
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import jobs  # proposed module under test: jobs.cleanup(job) deletes job["workdir"]


class CleanupBoundaryTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        patcher = mock.patch.object(jobs, "WORK_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_owned_leaf_is_deleted(self):
        leaf = self.root / "job-7"
        leaf.mkdir()
        with mock.patch.object(jobs.shutil, "rmtree") as rmtree:
            jobs.cleanup({"id": "job-7", "workdir": str(leaf)})
        rmtree.assert_called_once_with(leaf.resolve())

    def test_path_outside_root_never_reaches_rmtree(self):
        for target in (self.root, self.root / ".." / "etc", Path("/")):
            with self.subTest(target=target), mock.patch.object(jobs.shutil, "rmtree") as rmtree:
                with self.assertRaises(jobs.Refused):
                    jobs.cleanup({"id": "job-7", "workdir": str(target)})
                rmtree.assert_not_called()
```

The same shape covers the other effects: a recording sender for outbound requests, a fake
queue for jobs, a spy on the query or repository method, a temporary directory checked for
files written outside it. Credentials the test needs come from the fixture the project loads,
or are created in the test; never paste a repository credential into it.

## Inputs, queries, output and uploads

Use schemas with allowlisted shapes, types, ranges and lengths. Consume the parsed result
exclusively. Bind query values and allowlist dynamic identifiers. Avoid shell interpretation
by invoking a fixed executable with separate arguments. Use contextual output escaping and
vetted allowlist sanitization for necessary raw HTML. For uploads, enforce size before
buffering, inspect content when format matters, and use server-owned names and storage paths;
keep the client's file name only as display data.

Abuse cases: a query metacharacter payload, an oversized body, a value outside the allowed
range (negative, zero, huge), a file name with `../`, an absolute path or a separator, a
script tag in rendered text. Assert the query, renderer or file store shows no unintended
effect.

## Authentication, sessions and resource access

Check authentication and per-action authorization for the specific tenant and object on every
entry point, including batch handlers, downloads and workers. Scope the lookup or mutation by
authorized tenant and resource together. Derive the tenant from the session, never from a
client-supplied field. Role rules come from the project's own docs; when a new action has no
documented role, decide it, write the decision in the reply and test it.

Abuse cases: same-tenant access by the right role (allowed), the same action by a lower role,
an authenticated cross-tenant request, an unauthenticated request. Inspect response fields
and side effects, not only the status.

Use an appropriate Argon2, scrypt or bcrypt work factor for passwords. Keep browser session
cookies HttpOnly and Secure with bounded expiry, and verify SameSite and CSRF behavior for the
actual login and write flows. Check relevant response headers, including CSP and HSTS where
applicable, and allowlist CORS origins for credentialed requests. CORS controls browser
response access. Enforce authorization and CSRF protections separately. Use a shared
rate-limit store across replicas and test limits across instances.

## Outbound requests

For user-influenced destinations, allowlist the HTTPS scheme, host and port where the product
allows it, reject credentials in the URL and disable redirects (or re-validate every hop).
Resolve all A and AAAA records and reject the request when any answer is nonpublic or reserved:
loopback, private, link-local and cloud metadata (`169.254.169.254`, `fd00:ec2::254`),
unspecified, multicast, unique-local, and IPv4-mapped IPv6 forms of these. Parse addresses with
the language's IP library (`ipaddress.ip_address(...).is_global` in Python), never by string
prefix. DNS can change between validation and connection: pin the validated address or enforce
the destination at the transport or egress proxy for exposed fetchers, and name the remaining
gap in the reply when you cannot. Bound timeouts and the bytes read, and return a generic error
instead of exception text, since the response body travels back to the caller.

Abuse cases: a permitted public host (fetched), loopback, metadata address, private range,
IPv6 loopback or unique-local, a host with mixed public and private answers, a redirect to a
private address, a non-HTTP(S) scheme, credentials in the URL. Use a fake resolver and a
recording sender; assert refused destinations receive no request.

## Destructive paths

Resolve symlinks and require a strict descendant of an allowlisted root. Verify ownership
against a trusted job record or integrity-protected evidence before the call. A marker writable
by the same actor that chooses the path can be forged. If an attacker can swap ancestors
between check and use, use an immutable hierarchy or descriptor-relative no-follow operations
supported by the platform. Refuse without falling back to a broader target. Test an owned leaf,
the root itself, a path resolving outside the root and a mismatched owner, with a spy proving
refused inputs never reach the mutation (see the example above).

## Redirects, tokens and parsers

- Redirect targets after login or actions: allow relative paths or an allowlist of hosts;
  reject `//host`, schemes and encoded variants.
- Signed tokens (JWT and similar): pin the algorithm, verify signature, issuer, audience and
  expiry; reject `none`; keep keys out of the token header's control.
- Deserialization: never unpickle, `yaml.load` without a safe loader, or deserialize types
  chosen by input; accept data formats with type allowlists.
- XML: disable external entities and DTDs (`defusedxml` in Python).
- Templates: never compile a template from user input; pass input as data.

Abuse cases: an off-site redirect, a token with `alg: none` or a wrong audience, a payload
naming a dangerous type, an external entity, a template expression in user text.

## Dependency installation and audit

Identify the workspace installation boundary. Corroborate the pinned manager version,
authoritative lockfile and CI. Resolve conflicts before changing dependencies. Start with
scripts blocked before the first install. Inspect exact source and version, approve only
required scripts through native policy, then verify a clean frozen install. Review maintainer,
release, provenance, signature, transitive and lookalike-package risks.

Audit the committed lockfile with the native tool. Triage known advisories by reachability
through runtime, build, test or deploy, and fix availability. Review changes and test upgrades
before accepting them. Record reason and review date for deferrals. Avoid automatic force-fixes
and blanket script approval. An audit result covers known advisories only.

## Secrets, responses and personal data

Keep credentials in approved runtime secret storage, redact logs and use placeholder examples.
Log identifiers, never request headers, bodies or tokens wholesale; a log that support staff
can search is a disclosure channel. Check the staged changes and use a disposable sentinel to
test redaction. If a real secret reached a remote or a shared log, follow authorized incident
handling: rotate first, then clean history or the log. Allowlist response fields and keep
internal error details out of client responses.

Classify personal data and limit collection to a stated purpose. Define retention and exercise
export and deletion across primary stores, caches, indexes and backups according to the
retention policy. Verify applicable consent, third-party processing and regional requirements
with current authority. Use synthetic records for evidence.

## LLM outputs and tools

Treat prompts, retrieved documents and model outputs as untrusted. Validate structured output
and enforce tool arguments, tenant scope and permissions in code before execution. Keep secrets
out of context, isolate tenant retrieval and bound tokens, rate and recursion. Apply the
existing authority checks to destructive actions. Put an instruction into a synthetic retrieved
document that asks the model to read another tenant's data. Assert the tool layer denies the
call and no result reaches the model or client.

## Worked finding

The tenant invoice download finding that used to live here is now part of the
[worked example](worked-example.md), with a build and a review run end to end.

Provenance: independently worded adaptation of the Addy Osmani snapshot identified in the
owning GUIDE.md, with review additions described there; MIT notices at
[../references/license.md](../references/license.md). No upstream installation or hook is
required.
