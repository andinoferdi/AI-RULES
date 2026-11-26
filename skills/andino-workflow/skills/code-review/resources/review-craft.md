# Review craft: size, structure, dead code and dependencies

Resource for `andino-code-review`. Use it during the Standards pass when you need a named
remedy, a sizing judgement, or the dependency rules.

## 1. Change size

```text
~100 lines changed   -> reviewable in one pass.
~300 lines changed   -> acceptable when it is one logical change.
~1000 lines changed  -> too large to review well; ask for a split.
```

- Watch file size as well as diff size. A small diff that pushes a file past about 1000
  total lines is an inspection signal, not a hard cap: ask whether to extract helpers,
  subcomponents or modules first. Decompose, then add.
- One change is one self-contained modification: it addresses one thing, includes its
  tests and leaves the system working. One part of a feature, not the whole feature.
- Large changes are acceptable when they are whole-file deletions or automated refactors
  where the reviewer only needs to verify intent.
- Separate refactoring from feature work. A change that refactors and adds behavior is two
  changes: the refactor first, verified by the existing tests, then the feature. Small
  cleanups such as a rename can ride along at the reviewer's discretion.

| Strategy | How | When |
| --- | --- | --- |
| Stack | Submit a small change, build the next one on it | Sequential dependencies |
| By file group | Separate changes for groups that need different reviewers | Cross-cutting concerns |
| Horizontal | Shared models, interfaces or stubs first, consumers second | Layered architecture |
| Vertical | Thin end-to-end slices of one user flow | Feature work |

## 2. Smells and structural remedies

Binding rules:

- A documented repository standard always wins. Where it endorses a pattern a smell would
  flag, the smell is suppressed and is not reported.
- Every smell is a judgement call, labelled as such ("possible Feature Envy"). A smell alone
  never blocks; it becomes a blocker only through a presumptive blocker or a concrete
  defect.
- Skip anything tooling already enforces.
- When you flag one, name the move, not just the problem. A vague "this is messy" leaves the
  author guessing. Prefer the remedy that removes moving parts over one that spreads the
  same complexity around.

| Smell | Symptom | Remedy |
| --- | --- | --- |
| Mysterious Name | A name that does not reveal what it does or holds (`data`, `res`, `temp`) | Rename to the domain intent; if no honest name comes, the design is murky |
| Duplicated Code | The same logic shape in more than one hunk or file | Extract the shared shape into one canonical helper |
| Feature Envy | A method that uses another object's data more than its own | Move the method onto the data it envies |
| Data Clumps | The same few fields or parameters travel together | Introduce a parameter object or typed interface |
| Primitive Obsession | A primitive standing in for a domain concept with invariants (money, email, status) | Give the concept its own small type or value object |
| Repeated Switches | The same `switch` or `if` cascade on the same type in several places | Polymorphism, or one dispatch map both sites share |
| Shotgun Surgery | One logical change forces scattered edits across many files | Gather what changes together into one module |
| Divergent Change | One module edited for several unrelated reasons | Split so each module changes for one reason |
| Speculative Generality | Abstractions, parameters or hooks for needs nobody has | Delete or inline until a real need appears |
| Message Chains | `a.b().c().d()` navigation the caller should not depend on | Hide the walk behind one method on the first object |
| Middle Man | A class or function that mostly delegates onward | Remove it and call the real target directly |
| Refused Bequest | A subclass that ignores or overrides most of what it inherits | Replace inheritance with composition |

Structural moves that often resolve these:

- Replace a chain of conditionals with a typed model or an explicit dispatcher.
- Collapse duplicate branches into one clearer flow.
- Separate orchestration from business logic so each reads on its own.
- Move feature-specific logic out of a shared module into the package that owns the concept.
- Reuse the canonical helper instead of a bespoke near-duplicate.
- Make a type boundary explicit so downstream branching disappears.
- Delete a pass-through wrapper that adds indirection without clarifying the API.
- Extract a helper, or split a large file into focused modules.

Examples of naming the remedy:

- Repeated if/else checks on an entity's status string: replace the conditional with a
  typed dispatcher or a lookup map.
- A method reads another object's fields five times: move the method to the data owner.
- A function takes six primitive parameters that always travel together: introduce a
  parameter object.

A refactor that relocates complexity has not reduced it. Count the concepts a reader must
hold to follow the change; if the "cleaner" version leaves that count unchanged, prefer the
restructuring that makes whole branches, modes or layers disappear.

## 3. Dead code

After a refactor or implementation change, look for orphans:

1. code no longer called (functions, interfaces, variables);
2. commented-out blocks; version control keeps the history;
3. compatibility shims whose transition window has passed.

As a reviewer, list them explicitly and request their removal before merge. As the author,
list them and ask before deleting anything you are not sure about:

```text
DEAD CODE IDENTIFIED:
- formatLegacyDate() in src/utils/date.ts, replaced by formatDate()
- LEGACY_API_URL in src/config.ts, no remaining references
-> Safe to remove these?
```

## 4. Dependencies

Before a new dependency:

1. Can the standard library or an existing utility do it?
2. What does it add to bundle size and runtime, and how many transitive packages come
   with it?
3. Is it maintained: recent releases, handled issues?
4. Does an audit report vulnerabilities?
5. Is its license compatible with the project?

Upgrading a dependency is a change like any other:

1. Read the changelog, not just the version number. A patch release can change behavior;
   a major release needs its migration notes.
2. One dependency per change, or a small related group, so a breakage names its cause and
   the revert stays clean.
3. The suite decides: green before and after. Thin coverage around the dependency is the
   real finding; add a test first.
4. Review the lockfile diff, not just the manifest; one direct bump can pull many indirect
   changes.
5. Commit the lockfile and never hand-edit it.

Supply-chain verdicts (typosquatting, compromised maintainers, audit triage) belong to
`andino-security-and-hardening`.
