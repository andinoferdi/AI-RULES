# Pre-flight, frontier and write collisions

Internal Andino resource for `andino-delegation`. Use it before the first dispatch of a plan and
whenever a task finishes. Words such as frontier and lane are defined in [the rules](contract.md).

## Pre-flight table

Before the first dispatch, write a table into the plan (or the journal it links). Write each row as
you check it.

- One row per pair of tasks that share a file or an interface: the two tasks, what one produces and
  the other consumes, what you found, your ruling.
- One row per task: whether its own text agrees with itself and with the spec (the tests it names
  against the code it names, the files it creates against the files it later edits, its values
  against the spec's).

A clean scan without these rows was not run. Rule on each conflict with the spec as the authority
and record the ruling (format in [the rules](contract.md)). Ask the user only when the spec does
not settle it. Look in particular for:

- a value in the plan that differs from the spec (a timeout, a limit, a default);
- a dependency the text uses but the dependency table omits (Task 4 calls a function Task 5 adds);
- a test the plan specifies that cannot work with the signature it specifies;
- anything the plan mandates that the review would call a defect (a test that asserts nothing, a
  duplicated logic block).

Example rows:

| Pair or task | Produces / consumes | Found | Ruling |
| --- | --- | --- | --- |
| 1 and 3 | both edit `tests/conftest.py` | same file, different fixtures | never at the same time; same lane or sequential |
| 4 and 5 | 4 calls `parse_since`, which 5 adds | table lists 4 on 1, 2, 3 only | 4 also depends on 5 |
| 3 | default `expires_in=600` | spec says 900 seconds | 900 — spec is authority — a one-line constant if wrong |

For an investigation instead of a plan, the pre-flight is grouping the failures by cause: read the
failure output and the commits since the last green run, and put failures that share a cause in one
group. A shared cause is investigated once, inline or by one agent.

## Dependencies and the frontier

Reject duplicate task IDs, dependencies on tasks that do not exist, and cycles before computing
anything. A task joins the frontier when every task it depends on has parent acceptance whose
identities still match the current files. A producer that changed after acceptance is not accepted
any more, and neither is anything built on it.

```python
def compute_active_frontier(tasks: list[dict], completed_ids: set[str]) -> list[dict]:
    """Uncompleted tasks whose dependencies are all in completed_ids, in input order."""
    frontier = []
    for task in tasks:
        if task["id"] in completed_ids:
            continue
        if set(task.get("deps", [])).issubset(completed_ids):
            frontier.append(task)
    return frontier
```

Rolling frontier: when you accept a producer, start the listed agent for the task it unblocks right
away, inside the envelope and the 3-agent limit, without waiting for the rest of its wave. Never
start a consumer on a producer that has only its own worker's word.

## Write collisions

Two tasks may run at the same time only when none of these hold:

1. **Same file**: both write one path.
2. **Ancestor directory**: one owns a directory and the other a path inside it (`src/auth` and
   `src/auth/signer.py`).
3. **Shared root configuration**: `package.json`, `pyproject.toml`, `Cargo.toml`, lockfiles,
   migration ledgers and similar files have one writer at a time.
4. **Shared mutable state**: a database, a port, generated fixtures or a running service need
   isolation or one user at a time. Different file names alone do not make tasks independent.

```python
import os


def normalize_path(path: str) -> str:
    return os.path.normpath(path).replace("\\", "/").strip("/")


def has_write_collision(paths_a: list[str], paths_b: list[str]) -> bool:
    for a in map(normalize_path, paths_a):
        for b in map(normalize_path, paths_b):
            if a == b or a.startswith(b + "/") or b.startswith(a + "/"):
                return True
    return False
```

This snippet compares normalized relative paths; it is not a sandbox and grants no permission.
Check real ownership against resolved paths and the host's case rules, reject paths that escape the
worktree, and look for symlink aliases before dispatch. A consumed interface that is still changing
is a collision too: serialize the consumer.

## Lanes and waves

Group related tasks that share files or context into a lane, kept by one worker with one model.
Dependent tasks in a lane run in order and may reuse the same files. Separate lanes may run at the
same time when they pass the collision checks. Start a fresh worker for a later task only when the
lane's earlier context would mislead it, and say why; that is a new agent in the envelope.

When more lanes are ready than the limit allows, run at most 3 at once and pick the ones whose
results unblock the most work. A free slot does not authorize an agent the envelope did not list.

## Batching

Several small edits of the same shape (the same one-line fix, constant or key across files) are one
unit: do them inline or give the whole list to one agent, and review the diff as one change, file
by file against the list. Keep one task per agent for work that needs its own judgment, tests or
review.

## Anti-patterns

1. **One agent per failing test** when the failures share one schema change or broken import.
2. **Shared manifest races**: two agents each installing packages or editing `pyproject.toml`.
3. **Speculative dispatch**: starting a consumer while its producer still runs, or has passed only
   its own worker's self-review.
4. **History replay**: pasting the conversation or earlier tasks' summaries into a later dispatch.
5. **A merger or a reviewer per small task**: the parent integrates; review follows risk.
