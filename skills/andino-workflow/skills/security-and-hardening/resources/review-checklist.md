# Review checklist

Open this in review mode, gate 2. Every finding belongs to one of the eight categories below;
the questions per entry point find candidates, the dangerous-call table points at sinks, and
the rubric rates what survives gate 3.

## Eight categories

1. **Authentication and authorization.** Every route, handler and worker checks identity and
   the caller's right to this tenant and this object; no "logged in means allowed".
2. **Output encoding.** Values reaching HTML, Markdown, JSON, logs or headers are encoded for
   that sink.
3. **Outbound requests.** User-influenced URLs are checked against every resolved address,
   redirects are bounded, internal and metadata addresses are unreachable.
4. **Secrets.** No credential in code, URLs, logs, client bundles or responses.
5. **Input handling.** Queries are parameterized, paths are contained, redirect targets and
   deserialized types are allowlisted, sizes and ranges are bounded before work is done.
6. **Configuration.** Security headers, cookie flags, CORS allowlist, rate limits, debug and
   development bypasses off in production.
7. **Supply chain.** New packages, lockfile changes and install scripts reviewed; manager and
   lockfile agree.
8. **Failure modes.** Authorization and policy errors fail closed; errors reveal no stack
   trace, internal ID or personal data; broad exception handlers do not swallow security
   errors.

## Questions per entry point

- What does it do in one sentence, who is meant to call it, and what does it read, write and
  send out?
- Where is the authentication check, and can a route skip it?
- Is the tenant taken from the session or from the request? Is every lookup and mutation scoped
  by tenant and object together?
- Is every parameter typed and bounded (length, range, charset) before use? What happens with
  a negative, empty, huge or wrong-type value?
- Do file paths stay inside their base directory after resolution? Who chooses the name?
- Does any value drive a query, a shell command, a template, an outbound request or a
  deserializer?
- What does the response contain beyond what this caller may see? What does the log line
  contain?
- What happens when a dependency (auth service, database, remote host) fails or times out?
- Is the action rate-limited and audited at a sensible scope?

## Dangerous calls by language

| Sink | Python | JavaScript / TypeScript | Go | Java |
| --- | --- | --- | --- | --- |
| Query | `cursor.execute(f"...")`, `%` formatting, `text("..." + x)`, `.raw()`, `.extra()` | template strings in `query()`, `sequelize.literal`, `$where` | `db.Query(fmt.Sprintf(...))` | `Statement.execute("..." + x)`, JPQL string concat |
| Shell | `subprocess(..., shell=True)`, `os.system`, `os.popen` | `child_process.exec`, `execSync` with strings | `exec.Command("sh", "-c", x)` | `Runtime.exec(String)` |
| File path | `open(os.path.join(base, x))`, `Path(base) / x` without containment, `shutil.rmtree(x)` | `fs.*(path.join(base, x))`, `res.sendFile(x)` | `os.Open(filepath.Join(base, x))` | `new File(base, x)`, `Files.delete(x)` |
| HTML / template | `Markup(x)`, `\|safe`, `autoescape=False`, `Environment().from_string(x)` | `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `eval` | `template.HTML(x)` | unescaped JSP output, `th:utext` |
| Outbound HTTP | `requests`, `httpx`, `urllib.request.urlopen` (follows redirects) | `fetch`, `axios` with user URLs | `http.Get(x)` (follows redirects) | `HttpClient` with `followRedirects(ALWAYS)` |
| Deserialization | `pickle.loads`, `yaml.load` without `SafeLoader`, `xml.etree` without `defusedxml` | `node-serialize`, `vm.runInContext` | `gob` from untrusted input | `ObjectInputStream.readObject`, XML without XXE settings |
| Logging | `logger.info("%s", request.headers)`, logging bodies or tokens | `console.log(req.headers)` | `log.Printf("%v", r.Header)` | `log.info(request.getHeaderNames...)` |

## Severity rubric

| Severity | Meaning | Examples | Merge action |
| --- | --- | --- | --- |
| CRITICAL | An unauthenticated attacker takes over accounts, runs code, or reads or writes other tenants' data | authentication bypass, remote code execution, arbitrary file write reachable without login | Block; treat exposed credentials as compromised |
| HIGH | An authenticated attacker leaves their scope, or a live credential reaches people who should not have it | cross-tenant read, path traversal write, SSRF to internal services, tokens in a shared log, missing CSRF on a state change | Block; fix in this change or with a documented compensating control |
| MEDIUM | A gap that needs another bug to hurt, or that fails an audit | missing size check before decoding, a bypassable cap, stack traces in errors, missing rate limit | Fix in this change or file a ticket with a date |
| LOW | Hygiene with no plausible direct exploit | missing `nosniff`, a non-security hash choice, an unbound but integer-typed SQL fragment | Comment; no block |

Rate from what gate 3 established: reachability (which entry point, which role), attacker
prerequisites and impact on a named asset. When a finding sits between two levels and the
evidence does not settle it, take the higher one and say why.

## Decoys to dismiss with a reason

- A weak hash used for a cache key, ETag or deduplication, not for a password, signature or
  integrity check an attacker could forge.
- A value formatted into SQL after conversion to an integer or a fixed allowlist: no injection.
  A range it still escapes (a negative or huge value) is its own finding.
- A credential-shaped string in tests or examples that is labelled as a placeholder and matches
  no real account. Ask about credential-shaped values whose status you cannot tell.
- A route that looks unauthenticated but sits behind a middleware the router applies; confirm
  the middleware order before dismissing.

Write each dismissal in the report's Dismissed line, so the next reader sees it was examined.

Provenance: categories, entry-point questions, dangerous calls and the severity-to-merge rubric
are independently worded after Phoenix Security's `security-reviewer`
(Security-Phoenix-demo/security-skills-claude-code `40ace4a`, MIT); notices in
[../references/license.md](../references/license.md).
