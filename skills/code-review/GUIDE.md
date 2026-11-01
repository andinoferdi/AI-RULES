# Code Review and Quality Engineering Guide

This guide provides the deep operational craft, architectural remedies, and dispute resolution hierarchy for code review under Andino Workflow governance. It accompanies `SKILL.md` and provides thorough guidance for both human engineers and autonomous AI agents.

---

## 1. The Approval Standard

**Core Tenet:** *Approve a change when it definitely improves overall code health, even if it is not perfect.*

- Perfect code does not exist; software evolution is a continuous sequence of healthy increments.
- Do not block a change simply because the author chose a valid design pattern different from what you would have written.
- If the implementation meets the specification, complies with repository coding standards, introduces no regressions, and improves codebase health, **approve it**.
- Differentiate between **blocking defects** (bugs, security flaws, broken specs, data corruption) and **non-blocking enhancements** (alternative names, minor cleanups, optional abstractions).

---

## 2. Change Sizing and Decomposition

Small, focused pull requests are faster to review, safer to test, and significantly less likely to cause deployment rollbacks.

### 2.1 Sizing Thresholds
```
~100 lines changed   → Ideal. Thoroughly reviewable in a single pass.
~300 lines changed   → Acceptable if representing a single atomic logical change.
~1000 lines changed  → Too large. High defect escape rate. Require splitting.
```

### 2.2 File Size vs Diff Size
Watch total file size in addition to diff size:
- A small diff of 20 lines added to a file that already exceeds **1,000 total lines** is an architectural warning.
- Do not pile more logic onto an overburdened God-file. Ask whether to extract sub-modules, helpers, or policy objects *before* introducing new behavior: **Decompose, then add**.

### 2.3 Splitting Strategies for Large Changes
When a feature exceeds healthy review sizing, decompose it using these four strategies:

| Strategy | Mechanism | Optimal Context |
|---|---|---|
| **Stack** | Submit baseline change, then build dependent changes on top sequentially | Sequential logical dependencies |
| **By File Group** | Group changes by architectural boundary (e.g., API schemas, DB migrations, UI) | Cross-cutting features requiring distinct domain reviews |
| **Horizontal** | Create shared models, interfaces, or stubs first; introduce consumers second | Layered architectures |
| **Vertical** | Implement a complete, end-to-end thin slice for one specific user flow | Full-stack feature developments |

*Discipline Rule:* **Separate refactoring from feature work.** A change that refactors existing abstractions while simultaneously introducing new business behavior is two distinct changes. Submit the refactoring first (verified with existing tests), then submit the new feature.

---

## 3. The 12 Fowler Smells Mapped to Named Structural Remedies

When identifying code health issues on the Standards Axis, never stop at identifying the problem. Prescribe the exact **Named Structural Remedy**:

### 3.1 Mysterious Name
- **Symptom:** Variable, function, or class names like `data`, `res`, `temp`, `doProcess()`, or single-letter loop vars outside math indices.
- **Remedy:** *Rename Symbol to Domain Intent*. Express *what* or *why*, not the implementation type (e.g., `unverifiedSubscribers` instead of `dataList`).

### 3.2 Duplicated Code
- **Symptom:** Identical or near-identical logic duplicated in two or more modules.
- **Remedy:** *Extract Canonical Helper* or *Form Template Method*. Consolidate into a single authoritative location.

### 3.3 Feature Envy
- **Symptom:** A method spends more time querying and manipulating fields of another object than its own data.
- **Remedy:** *Move Method to Data Owner*. Relocate the behavior directly into the class or module that holds the data.

### 3.4 Data Clumps
- **Symptom:** The same three or four parameters (`street`, `city`, `zipCode`, `country`) passed together across multiple function signatures.
- **Remedy:** *Introduce Parameter Object / Typed Interface*. Bundle them into a cohesive domain struct or class.

### 3.5 Primitive Obsession
- **Symptom:** Using raw primitives (`string`, `float`, `int`) for domain concepts with invariants (emails, currency, postal codes, status codes).
- **Remedy:** *Replace Primitive with Branded Type or Value Object*. Prevent mixing currencies or passing invalid strings at compile-time.

### 3.6 Repeated Switches
- **Symptom:** The same `switch (entity.type)` or `if/elif/else` chain repeated in multiple places across the codebase.
- **Remedy:** *Replace Conditional with Polymorphism* or *Strategy Dispatch Map*. Add new cases in one table rather than editing multiple switch statements.

### 3.7 Shotgun Surgery
- **Symptom:** Making a single logical change requires modifying ten different files across the repository.
- **Remedy:** *Move Field / Consolidate Module*. Realign module boundaries so that related concepts reside in one place.

### 3.8 Divergent Change
- **Symptom:** One module is repeatedly modified for completely different reasons (e.g., changing database schema, changing UI rendering, and changing auth logic all touch `UserManager.ts`).
- **Remedy:** *Extract Class / Separate Orchestration from Policy*. Enforce Single Responsibility Principle.

### 3.9 Speculative Generality
- **Symptom:** Abstract interfaces, factory builders, and hooks designed for hypothetical future requirements that do not yet exist (YAGNI violation).
- **Remedy:** *Collapse Abstraction / Inline Wrapper*. Delete the unused indirection until the third genuine use-case arrives.

### 3.10 Message Chains
- **Symptom:** Long chained calls navigating deeply through object graphs: `order.getCustomer().getAddress().getCity().getTaxRate()`.
- **Remedy:** *Hide Delegate (Law of Demeter)*. Expose a direct method on the top-level entity: `order.getDestinationTaxRate()`.

### 3.11 Middle Man
- **Symptom:** A class where half the methods merely delegate directly to another object without adding value or encapsulation.
- **Remedy:** *Remove Middle Man / Inline Method*. Let callers access the underlying server directly if no translation occurs.

### 3.12 Refused Bequest
- **Symptom:** A subclass inherits methods and data from a superclass but overrides them to throw `NotSupportedException` or ignores half of them.
- **Remedy:** *Replace Inheritance with Composition*. Inject the shared behavior as a collaborator rather than inheriting unnecessary surface area.

---

## 4. Dead Code Hygiene

Unused code confuses readers, misleads AI models, and creates maintenance drag. Reviewers must inspect for orphaned artifacts:
1. **Unreachable Code:** Functions, interfaces, or variables no longer called after refactoring.
2. **Commented-Out Blocks:** Never permit `// old implementation` blocks. Version control remembers history; remove commented code.
3. **Vestigial Shims:** Temporary compatibility wrappers whose transition window has passed.
4. **Discipline:** List identified dead code explicitly in the review comments and request removal before merging.

---

## 5. Dependency Review Discipline

Every third-party package introduced into a repository represents a permanent maintenance, security, and supply-chain liability.

### 5.1 Review Questions for New Dependencies
1. **Can this be solved with the Standard Library or existing utilities?** Modern standard libraries (Node `node:fs`, Python `itertools`/`pathlib`, Go standard library) often solve the problem in 10 lines without external packages.
2. **Bundle & Runtime Impact:** What is the unpacked and gzipped weight? Does it pull in dozens of transitive dependencies?
3. **Maintenance Health:** Is the project actively maintained? When was the last commit? Are open security issues addressed?
4. **Security & Licensing:** Does `npm audit` or equivalent report vulnerabilities? Is the license compatible with the project (e.g., MIT, Apache 2.0 vs restrictive AGPL)?

### 5.2 Dependency Upgrades
- **One Dependency Per Change:** Never submit bulk `bump all deps` PRs. When an upgrade breaks runtime behavior, atomic PRs make root-cause isolation trivial.
- **Review Lockfile Diffs:** Always review `package-lock.json`, `pnpm-lock.yaml`, or `poetry.lock`. Ensure no unexpected transitive packages were injected.

---

## 6. Hierarchy of Disagreement Resolution

When author and reviewer disagree on code changes, resolve the dispute using this objective hierarchy:

```
1. Technical Facts & Empirical Data   (Overrides opinions; benchmarks, test failures, specs)
2. Documented Project Style Guides    (Absolute authority on formatting, naming, and patterns)
3. Software Engineering Principles    (Cohesion, coupling, information hiding, single responsibility)
4. Codebase Consistency               (Acceptable default if not degrading code health)
```

**Never Accept:** *"I will clean this up in a follow-up PR."*  
Historical reality shows deferred cleanups rarely happen. If an issue is important enough to flag, resolve it before merging into main. If an issue truly cannot be addressed in the current scope, require an open issue with self-assignment before merge approval.

---

## 7. Review Speed & Ergonomics

- **Cadence:** Review requests should be triaged within one business day. Slow reviews block delivery pipelines and force painful context switches.
- **Lead with What Matters:** Group and order comments by leverage. Place `[CRITICAL]` and `[REQUIRED]` blockers at the top. Never bury a critical memory leak under six formatting nits.
- **Actionability:** Pair every criticism with an explicit example or suggested replacement. A review that teaches and guides accelerates both human developers and autonomous agents.
