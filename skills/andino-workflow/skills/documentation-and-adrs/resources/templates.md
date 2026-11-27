# Templates

Defaults for when the repository has no convention of its own. When it has one (a template file,
earlier records, a changelog style), follow that instead and use these only to check that nothing
the reader needs is missing.

## Decision record (ADR)

Store as `docs/decisions/NNNN-short-title.md`, numbering on from the highest existing or reserved
number.

```markdown
# ADR-0007: Store invoice PDFs in object storage

## Status
Proposed. Decided by: <name>, on or before <date>.
(Later: Accepted <date> by <name> | Superseded by ADR-00NN | Deprecated <date>)

## Date
2026-11-26

## Context
What forces the decision now, with evidence and its limits.
- Incident or requirement, with its reference.
- Measurement: value, number of runs, environment, data size.
- Constraints from earlier records (link them).

## Decision
The option chosen, in one or two sentences. Name the record it replaces, if any.

## Options considered
Judge every option on the same criteria (for example: survives a host rebuild, monthly cost,
fits ADR-0002).

### Option A (chosen)
- Meets: ...
- Costs: ...

### Option B
- Meets: ...
- Fails: ... Passed over because ...

## Consequences
- Obligations: what operators or developers must now do.
- Costs and risks accepted.
- Open questions, each with who answers it.

## Revisit when
A metric with a threshold or a named event, for example "storage cost above 50 EUR a month" or
"invoices must be kept longer than the bucket's retention allows".
```

Lifecycle: proposed, then accepted, then superseded or deprecated. Never delete a record. When a
new record is accepted, set the old one's status to "Superseded by ADR-00NN" and keep its text.

Write an ADR when a choice is expensive to reverse or would surprise a newcomer: a framework or
major dependency, a data model, an authentication strategy, an API style, hosting or build
tooling.

## API reference entry

```markdown
## POST /exports/{id}/retry

Requeues a failed export. Requeueing an export that is not failed changes nothing.

Request body (optional JSON):

| Field | Type | Default | Limits | Notes |
| --- | --- | --- | --- | --- |
| `priority` | string | `normal` | `normal` or `high` | `high` needs the `exports:admin` scope. |

| Status | Body | When | Caller action |
| --- | --- | --- | --- |
| 202 | `{"state": "queued"}` | The export was failed and is queued again. | Poll `GET /exports/{id}`. |
| 404 | error `not_found` | No export with this id. | Check the id. |
| 409 | error `not_failed` | The export is queued, running or done. | Do not retry; read its state. |

Side effects: one queue entry per accepted request; a rejected request changes nothing.
Retry: safe to repeat after a timeout; a second request for the same export gets 409 `not_failed`.
Changed in 2.3: `priority` added (before 2.3 every retry ran at normal priority).
```

Typed code: put the contract on the declaration.

```typescript
/**
 * Requeues a failed export.
 * @param id - Export id.
 * @returns The new state, always "queued".
 * @throws {NotFoundError} No export with this id.
 * @throws {ConflictError} The export is not failed; nothing changes.
 */
export async function retryExport(id: string): Promise<{ state: "queued" }>;
```

OpenAPI: list every response the handler can return.

```yaml
/exports/{id}/retry:
  post:
    responses:
      "202": { description: Export queued again }
      "404": { description: No export with this id }
      "409": { description: Export is not failed; nothing changed }
```

## README

```markdown
# Project name

One paragraph: what it does and for whom.

## Quick start
Prerequisites: <runtime and version>, <services>, <config file>.
1. `<install command>`
2. `<config step>`
3. `<run command>`; expect <what the reader sees>.

## Commands
| Command | What it does |
| --- | --- |
| `<test command>` | Run the tests |

## Architecture
Two or three sentences, then links to the decision records.

## Contributing
Where conventions, review rules and the PR process live.
```

## Changelog entry

Keep a Changelog style, under the unreleased heading:

```markdown
## [Unreleased]
### Changed
- **Breaking:** `GET /exports` returns 50 items per page (was 100). Clients that read only the
  first page must follow the `next` link.
- Exports retried with `priority: high` now need the `exports:admin` scope.
```

Write for the consumer: what changed, who is affected, what they must do. Released sections are
never edited.

## Change log inside a document

Append at the end of the existing list, dated today:

```markdown
- 2026-11-26: Retry limit corrected to 3; `MAX_RETRIES` changed in a1b2c3d.
```

## Comments

```python
# Restates the code: delete it.
# increment the counter
counter += 1

# States a reason the code cannot show: keep it.
# The window opens on the first request after the previous window expires, not on a clock
# boundary, so a client can spend the full limit just before and just after a reset (2x burst).
if now - window_start > WINDOW_SECONDS:
    counter, window_start = 0, now

# A hazard, with its source.
# Amounts are integer cents (ADR-0012). The card fee rounds down: `* 3 // 100`, never `* 0.03`.
fee_cents = total_cents * 3 // 100

# A tracked TODO keeps its reference.
# TODO(#142): accept XLSX once the parser upgrade lands.
```

Commented-out code is deleted; version control keeps it. An untracked TODO is done now or deleted
and reported as follow-up.
