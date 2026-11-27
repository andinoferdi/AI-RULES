# Patterns and notices

Load this from gate 3 or gate 5 of the deprecation guide when a consumer needs a transition path
or a written notice. Every snippet is a starting shape: adapt names and checks to the project,
and keep the evidence the guide's gates ask for.

## Adapter: old interface, new implementation

Consumers keep calling the old interface while the work moves to the replacement. The adapter
owns every behaviour difference gate 3 found, so a caller sees exactly what it saw before.

```typescript
// Old callers expect a numeric id, a boolean `done` and null for a missing task.
class LegacyTaskService implements OldTaskAPI {
  constructor(private tasks: NewTaskService) {}

  getTask(id: number): OldTask | null {
    try {
      const task = this.tasks.findById(String(id));
      return { id: Number(task.id), title: task.title, done: task.status === 'done' };
    } catch (err) {
      if (err instanceof TaskNotFound) return null; // the old contract returned null, not an error
      throw err;
    }
  }
}
```

Parity check: call the old implementation and the adapter on the same inputs (including a
missing id and every status value) and compare the results field by field. Keep the check as a
test until the old implementation is gone.

## Feature flag per cohort

```typescript
function taskService(userId: string): TaskService {
  return flags.isEnabled('new-task-service', { userId })
    ? new NewTaskService()
    : new OldTaskService();
}
```

Before widening a cohort, compare its critical behaviour and error rate with the old path, and
confirm that switching the flag back reads data the new path wrote since the switch.

## Strangler routing

Run old and new side by side and move traffic in steps; each step advances only after the
previous one passed its checks over a window that includes background and batch traffic.

```text
Phase 1  new 0 %    old 100 %   new path deployed, shadow-compared
Phase 2  new 10 %   old 90 %    canary cohort
Phase 3  new 50 %   old 50 %
Phase 4  new 100 %  old idle    usage of the old path measured, bypass routes checked
Phase 5  old removed            after the guide's gate 6 says ready
```

## Moving one consumer

1. List its touchpoints with the old thing (imports, config strings, SQL, HTTP calls).
2. Switch them to the replacement or the adapter.
3. Run the parity check on the consumer's real inputs: same outputs, or each difference
   written down and accepted by the consumer's owner.
4. Remove its references to the old thing and run its tests.
5. Mark it migrated in the consumer map with the parity result.

## Deprecation notice (external consumers)

Draft it as a file; sending it is the user's decision. The removal date respects every notice
period the consumer's agreement sets, counted from the day the notice is actually sent.

```markdown
## Deprecation notice: <old interface>

**Status:** deprecated since <date>; <advisory, no removal date | removed on <date>>
**Replacement:** <new interface>, available since <date>
**Why:** <one or two sentences: what the old one costs or blocks>

### What changes for you
Before: `<old call>` -> `<old response>`
After:  `<new call>` -> `<new response>`

Differences to handle:
- <for example: totals are a decimal string with two places instead of a whole-number integer>
- <for example: an unknown item returns HTTP 404 instead of a null total>

### How to verify
<a request they can run against a sandbox, and the response they should see>

### Timeline and support
<dates; the notice period you are honouring>; questions to <contact>.
```

## Handoff note (another internal team)

```markdown
To <owner> (<team>): <job or service> still uses <old thing> (<file:line or query>).
It runs <schedule; next run>. Before <date or condition>, change <exact change> and run <check>;
expected result: <result>. Until then we keep <old thing> working. Contact: <name>.
```

## Migration guide skeleton

1. Replace `<old import, endpoint or column>` with `<new one>`.
2. Update configuration: `<key>: <old value>` -> `<new value>`.
3. Handle the differences: <list from the notice>.
4. Run `<verification command>`; expect `<output>`.
