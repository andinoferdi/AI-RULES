# Completion criteria

Read this when writing or sharpening the condition that ends a step, or when agents keep
finishing a step too early.

## Clarity and demand

A completion criterion has two separate properties.

- **Clarity**: can the agent tell done from not done? A vague end ("understanding
  reached", "looks good") invites premature completion: attention slips from doing the
  work to being done, pulled by the steps still visible below.
- **Demand**: how much the criterion requires. "Every modified model accounted for" forces
  work that "produce a change list" does not. Demand drives legwork, the digging inside a
  step, without writing that digging as steps of its own.

| Clarity | Demand | Result |
| --- | --- | --- |
| High | High | Checkable and exhaustive: the target |
| High | Low | Shallow pass: easy to check, skips the work ("run the linter") |
| Low | High | A slog with no finish line |
| Low | Low | Premature completion ("check the code thoroughly") |

## Raising demand

| Shallow | Demanding |
| --- | --- |
| "List the modified models." | "List every modified model; done when each foreign key touching one is checked against its migration." |
| "Check that the API handles errors." | "Done when a test asserts the status code and error body for 400, 401, 403, 404 and 422." |
| "Review the changed files." | "Done when every file in `git diff --name-only` has a verdict against each rule in section 3." |

Demand also binds flat reference. "Every rule applied, each with a pass or fail verdict and
file:line evidence" puts an exhaustiveness bar on a document that has no steps.

## Forms a criterion can take

A shell predicate is one form, not the only one. Use the form that fits the work:

- Command result: the test command exits 0 with a test count above 0.
- Artifact state: `git status --porcelain` prints nothing; the named build output exists.
- Coverage of a set: every item in a named list has a verdict with evidence.
- Judgment with an exhaustiveness bar: every requirement maps to a test, or is listed as
  untested with a reason.

A shell command that does not test the judgment a step needs makes the criterion clear and
wrong.

| Work | Vague | Observable |
| --- | --- | --- |
| Tests | "Make sure the tests pass." | The test command exits 0, 0 failures, test count above 0 |
| Clean tree | "Make sure git is clean." | `git status --porcelain` prints nothing |
| Build | "Build it properly." | The named artifact exists and is not empty |
| Schema | "Check the JSON format." | The validator exits 0 against the named schema |
| Lint | "Fix style issues." | The linter exits 0 at the project's warning threshold |
| Service | "Make sure the server runs." | The health endpoint returns 200 |

## When an agent still rushes

Defend in this order and stop at the first step that works:

1. **Sharpen the bound.** Replace adjectives with an observable state. It is local and
   cheap.
2. **Raise the demand.** Require evidence for every item in scope.
3. **Split across a real context boundary.** Only when the step is irreducibly fuzzy and
   the rush has been observed: move the later steps behind a hand-off, a subagent dispatch
   or a separate phase. Splitting text inside one loaded file hides nothing, because the
   later steps stay in context.
