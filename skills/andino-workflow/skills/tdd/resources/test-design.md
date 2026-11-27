# Test design: seams, expected values, doubles and boundaries

Consult this when filling a slice-list row or writing its test. Examples use Python `unittest`;
use the repository's own framework and helpers.

## Pick the seam and the level

A seam is the public boundary a caller uses: a function or class other modules call, an HTTP
endpoint, a CLI command, a UI control. Test there; the internals may change freely behind it.
Choose the lowest level that still reaches the real behavior:

- pure logic with no I/O: a small, fast test of the function;
- behavior that crosses your own boundary (a database, a file, an HTTP handler): a medium test
  through that boundary with a test database or temporary directory;
- a critical user flow: a few end-to-end tests, only for the paths that must never break.

These are resource choices, not percentage quotas. When the shape of the seam itself is still
open (what the interface should expose), settle that first; ask the user only when it is a real
choice with consequences and nobody else can decide it.

## Write expected values by hand

```python
# Tautological: the expected value repeats the code's own arithmetic.
def test_total(self):
    items = [3_000, 4_500]
    self.assertEqual(order_total(items), sum(items) * 111 // 100)

# Independent: worked out by hand from the rule (7.500 + 11% = 8.325).
def test_total_includes_vat(self):
    self.assertEqual(order_total([3_000, 4_500]), 8_325)
```

Name the break before writing the body: the wrong constant, the missing branch, the boundary off
by one, the side effect that never happens. If you cannot name one, the test checks nothing a
bug could change. A test that fails only when an intentional decision changes (a constant's
value, exact wording) is a change detector: test the behavior that depends on the decision
instead.

## Verify through the interface

```python
# Side channel: reads storage the caller never sees.
def test_register_saves_member(self):
    register("dewi@example.org")
    self.assertEqual(db.execute("select count(*) from members").fetchone()[0], 1)

# Through the seam: what a caller can observe.
def test_registered_member_can_be_found(self):
    member = register("dewi@example.org")
    self.assertEqual(find_member(member.id).email, "dewi@example.org")
```

## Doubles: real first, then fake, stub, mock

Prefer, in order: the real implementation; a fake (an in-memory version, such as a recording
mailer); a stub that returns canned data; a mock that checks calls. Replace only what is slow,
external, unsafe or nondeterministic. Before replacing a method, list its side effects and keep
the ones the test depends on real. A double returns the complete structure the real boundary
returns, not only the fields this test reads.

Design boundaries so a double is easy: pass the clock, client or gateway in (dependency
injection) instead of constructing it inside, and give an external service one function per
operation (`get_member`, `create_loan`) rather than one generic `request(path, options)`.

```python
# Tests the mock: passes whenever the code calls send, whatever it sends.
mailer.send.assert_called_once()

# Tests the outcome: the recording fake holds what was sent.
self.assertEqual(mailer.sent, [("dewi@example.org", "Welcome to the library")])
```

Assert a call count or order only when the count or order is itself the contract (exactly one
charge per order).

## Boundary inventory

For each rule, list the cases where a bug would hide, then give the ones that matter their own
slice-list rows: the exact threshold and the value just past it; a value that rounds exactly on
the half; zero, empty and missing input; the cap or limit and one past it; invalid or malformed
input; an external failure or timeout; out-of-order or concurrent calls. Rank by what a failure
would cost (lost money or data, a security hole, a broken core flow). This is a risk map, not an
instruction to test every trivial function.

## Examples kept from the earlier contract

- **A first feature slice.** At the public checkout entry point, use a cart worth 5,000 cents and
  an active fixed coupon for 700 cents, with fees and tax disabled in the fixture; expect a charge
  of 4,300 cents. The code before the feature charges 5,000 or rejects the coupon: find which and
  confirm the focused run shows that mismatch. Receipt formatting, expiry and usage limits are
  later rows.
- **Rollback through a real boundary.** Balances 100 and 20; transfer 30. In the test database,
  make the credit write fail after the debit succeeds (a constraint or a deterministic fault at
  that boundary). Confirm the fault was reached and the debit ran in that attempt, then read both
  balances from a fresh connection: expect 100 and 20. The broken version leaves 70 and 20. A
  fault before the debit leaves both unchanged even when rollback is broken, so it proves
  nothing. An injected exception is not process termination, and a mocked transaction is not a
  rollback.

## UI, HTTP, browser and asynchronous tests

- Components: find controls by accessible role and name, and assert what the user sees
  (validation text, enabled state).
- HTTP: assert the status and the response body for a valid, a malformed and an unauthorized
  request.
- Browser flows: exercise the whole create-and-complete path and check the visible result.
- Await every asynchronous success and rejection check; pin time and random seeds; give each
  test its own data and clean it up.
- Snapshot only what a reviewer will actually read.

## Readable tests

Arrange, act, assert, in that order and visibly separated. Prefer descriptive repetition (DAMP)
over shared helpers that hide what a test sets up: each test should read as a complete story.
Keep test-only helpers and cleanup in test utilities, never as methods on production classes.

## Provenance

Substantive adapted material is covered by the MIT notices in
[../references/license.md](../references/license.md).
