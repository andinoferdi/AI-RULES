# Test one public behavior before implementing it — supporting contract

## Tests and the separate refactor gate

Use repository-native commands. Prefer small pure tests, medium boundary integration and a few critical E2E flows; these are resource choices, not fixed percentage quotas. DAMP fixtures deliberately repeat enough facts to tell each story.

A public seam may span create then retrieve, or reserve then release. Do not bypass it through an unrelated storage side channel. Doubles belong at system boundaries. Assert external call counts only when count/order is itself a contract; internal collaborator mocks couple tests to structure.

The refactor gate starts from GREEN. Compare return values, exceptions, side effects and ordering; simplify one observed problem. Apply the deletion test: what concept or indirection disappears? A deep module can hide complexity; an adapter without actual variation adds it. No new behavior belongs in this gate.

## Coverage design and boundary examples

Choose the lowest level that captures the real behavior. Inventory happy path, empty input, numeric/string boundaries, invalid input, external failure/timeout and concurrent/out-of-order calls; prioritize by data loss/security and core user flow. This is a risk map, not a rule to test every trivial function. Report current coverage, gaps, recommended case and what bug each catches.

For components, locate controls by accessible role/name and assert user-visible validation or state. For HTTP boundaries, assert status and response contract for valid, malformed and unauthorized cases. For a critical browser path, exercise the full create/complete flow and visible result. Always await asynchronous success and rejection checks; isolate mutable test data and time. Snapshot only what a reviewer will inspect. Never skip a failing test just to make CI green. Upstream JS/TS syntax is illustrative: use the repository's native framework.
