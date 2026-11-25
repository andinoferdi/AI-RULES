# Pin behavior before changing it

Use when the target lacks trustworthy tests, when code resists being put under test,
or when a change must preserve behavior nobody has written down. The goal is a vise:
tests that hold the current behavior of the region you are about to change, so any
unintended movement fails at once.

## The change sequence

1. **Change points.** Read until you can point at the lines that must change.
2. **Test points.** Find where a test can observe the effect of those lines (see the
   effect sketch in triage-and-hotspots.md).
3. **Break dependencies** only as far as needed to run the code in a test, using the
   least invasive technique below. These pre-test edits preserve signatures exactly.
4. **Pin** the current behavior of every branch the change will disturb.
5. **Change**, one concern per step (see refactoring-moves.md).

Pins must pass on the unmodified code before any change. A pin that fails on
unmodified code is a wrong observation: correct the pin, never the code.

## Characterization recipe

A characterization test records what the code does now, not what anyone thinks it
should do.

1. Call the code from a test with a representative input.
2. Assert a value you know is wrong.
3. Run it and read the actual value from the failure message.
4. Replace the assertion with the observed value and name the test after what you
   learned. If you cannot yet explain the value, use a neutral name.
5. Repeat for each branch on the path you will change.

```python
def test_probe_late_fee(self):
    self.assertEqual(late_fee(days_late=0, balance=120), -1)   # absurd on purpose
# Failure: AssertionError: 5 != -1  -> a zero-day invoice already pays a 5 fee

def test_zero_days_late_charges_minimum_fee(self):
    self.assertEqual(late_fee(days_late=0, balance=120), 5)    # observed
```

Choosing inputs: one probe per branch on the change path; boundaries (zero, negative,
empty, missing keys, maximum size, time edges); anonymized real records when
available. Use coverage only as a flashlight on the region you will change. Stop when
every branch you will disturb has a pin.

## Known bugs found while pinning

Characterization regularly exposes defects. Do not fix them inside the pinning step:
callers, reports or data may depend on the current behavior, and a silent fix hides a
behavior change inside a "no behavior change" step.

1. Pin the current wrong behavior and mark it with the finding ID.
2. Record the finding in the task record (severity, confidence, disposition).
3. Fix it later as its own behavior step: flip the pin and change the code in the same
   step, with the contract reason.

```python
def test_reminder_sent_twice_across_dst_change(self):
    # KNOWN BUG RSC-003: duplicate reminder on the DST night. Flip in the fix step.
    self.assertEqual(len(sent_reminders(day="2026-03-29")), 2)
```

## Large outputs: golden masters and snapshots

When output is a report, generated file or large JSON, capture it once and compare
later runs against it.

- Review the first capture line by line; recording it is signing off on it.
- Normalize volatile values (timestamps, generated IDs, hostnames) before comparing.
- Keep several small masters, one per input class, rather than one large blob.
- Regenerating a master is a behavior change. Review the diff and keep it in the step
  that caused it. Treat snapshot update commands the same way.

## Separation and sensing

Code resists tests for two reasons. **Separation**: it cannot run in a test because it
opens connections, reads the clock or calls a singleton. **Sensing**: it runs, but the
test cannot see what it computed. Break only what blocks one of these.

## Choose the cheapest seam

A seam is a place where a test can change behavior without editing that place.

1. An existing parameter or constructor argument. Pass a fake; no production edit.
2. An import or link seam (`unittest.mock.patch`, `jest.mock`, monkeypatching).
   No production edit, but the test couples to module layout.
3. A new object seam: Parameterize Constructor or Method with a production default,
   Extract and Override Factory Method, Adapt Parameter. A small signature-preserving
   edit that stays useful.
4. Preprocessor or build flags, last resort.

Common seams:

| Hidden input | Seam |
| --- | --- |
| Wall clock (`datetime.now()`, `Date.now()`) | Inject a `now` callable or parameter with a production default; or freeze time in the test. |
| Environment and config reads | Funnel through one config object passed in; until then patch the environment and reset it. |
| Network or provider client | Fake your own gateway interface; fake at HTTP level only when the code's job is building requests. |
| DI container | Override the provider in a test module. |

## Dependency-breaking moves

| Blocker | Move |
| --- | --- |
| Constructor does real work (connections, files) | Parameterize Constructor with a production default |
| Heavy concrete collaborator | Extract Interface |
| Method reads clock, randomness or a global | Parameterize Method |
| Object created inside the method under test | Extract and Override Factory Method |
| Field value blocks testing in many methods | Extract and Override Getter |
| One dangerous call | Subclass and Override Method |
| Static method or singleton used everywhere | Introduce Instance Delegator, or a static setter reset after each test |
| Framework parameter that is hard to build | Adapt Parameter (wrap it in a narrow interface you own) |
| Very long method with tangled locals | Break Out Method Object |

## When the area cannot be pinned in time

Sprout or wrap instead of editing the untested mass:

- **Sprout**: write the new behavior as a new, fully tested function or class and call
  it from one line in the old code.
- **Wrap**: rename the old function, recreate the old name as a wrapper that adds
  behavior before or after it.

Record the untested host as debt in the task record with the next condition that will
cover it. A sprout does not make the host safe.

## Traps

- Tests that patch everything pin the call graph, not behavior; prefer one fake at a
  real boundary.
- Fakes drift from real signatures; use autospec or typed helpers so they fail loudly.
- A seam at the wrong layer (faking a query builder to test pricing) pins SQL strings;
  move up to the repository the logic actually uses.
- Editing the logic to install a seam turns the pin into a guess; pick a seam at a
  distance.
- Global seams (environment patches, static setters, module mocks) need a guaranteed
  reset, or test order starts to matter.
