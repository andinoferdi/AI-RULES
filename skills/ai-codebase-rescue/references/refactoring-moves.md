# Change one concern at a time

Use when a REFACTOR, REMOVE or REMAKE disposition is being carried out. Every step
either changes structure or changes behavior, never both, and every step ends with
the code working.

## Step discipline

1. Pins and focused tests are green before the step.
2. Make one move: one structural transformation, or one behavior correction.
3. Run the pins and focused tests.
4. Green: keep the step. When commits are authorized, stage only the files of this
   concern and read `git diff --cached --stat` before committing. A file that belongs
   to another concern waits for its own step.
5. Red after a structure step: revert that step and retry with a smaller move. Do not
   debug forward on top of a broken refactoring.

A behavior step changes exactly the pins it means to change: it flips the known-bug
pins it fixes, in the same step, with the contract reason. Any other pin that turns red
is an unintended change.

Typical sequence: preparatory structure step that makes the fix easy, behavior step
that fixes it, structure step that removes what the fix made obsolete.

## Smell to move

Name the smell, then name the move. A smell without a move is a note, not a step.

| Smell | Move |
| --- | --- |
| Same rule implemented twice and the copies diverged | Pin both paths, route both callers through one owner, then delete the copy after a consumer check |
| Long function doing several things | Extract Function, named after what the block does |
| Nested conditionals | Replace with guard clauses |
| Flag argument switching behavior | Split into two functions |
| Long parameter list or data that travels together | Introduce Parameter Object |
| Shallow classes that always change together | Inline or merge into one deeper module |
| Interface with one implementation and no seam purpose | Inline the interface |
| Repeated type switches | Replace Conditional with Polymorphism, after the third occurrence |
| Magic numbers in rules | Named constant at the rule's owner |

Prefer moves that reduce what a caller must know. Splitting code into many thin
classes raises complexity even when each file gets shorter.

## Migration patterns

Choose the smallest pattern that keeps the code shippable after every step.

| Pattern | Use when | Steps | Avoid when |
| --- | --- | --- | --- |
| Extract and Simplify | One function is too complex to change safely | Pin it, extract sub-functions one at a time, simplify conditionals | The problem is ownership across modules |
| Expand-Migrate-Contract | A signature, return shape or data format must change while callers exist | Add the new form beside the old, move callers one at a time, remove the old form last | All callers are in one file you change in one step |
| Branch by Abstraction | An internal component is replaced while work continues | Introduce an interface over the old component, move callers to it, build the new implementation behind it, switch, remove the old one and any single-use interface | The component has one caller and a direct swap is protected |
| Strangler Fig | A large area with many consumers is replaced gradually | Put a routing seam in front, move one consumer or route at a time to the new code, retire the old code when nothing routes to it | The area is small enough for one protected swap |

For data, Expand-Migrate-Contract means: write both formats, move readers, stop writing
the old format, then remove it. A rollback command may not restore data that a new
format already changed.

## Blast radius is a signal

Before a move, count what it touches: files, callers, config entries and external
consumers. When one step reaches many files, or two modules that change together,
split the step or introduce a seam first. A number of files is a warning, not a
rule; the test is whether one step can still be checked and reverted on its own.

## When not to refactor

- The code works, nobody needs to change it, and it sits behind a clean interface: KEEP.
- The code is scheduled for removal: leave it, record the plan.
- No protection can be built yet: INVESTIGATE, or sprout/wrap the change and record
  the untested host as debt.
- The only argument is taste or authorship: KEEP.

Preparatory refactoring (make the change easy, then make the easy change) is justified
by the change it enables. The Rule of Three guards against abstractions built for a
single case.
