# Architectural vocabulary and card wording

Internal resource of `architecture-survey`. Read it when wording a finding, a candidate card
or a grilling question. The definitions follow Matt Pocock's `codebase-design`; the
module-depth resource of the sibling `api-and-interface-design` skill uses the same terms.

## Terms

**Module**: anything with an interface and an implementation. Scale-agnostic: a function, a
class, a package or a slice that spans tiers.

**Interface**: everything a caller must know to use the module correctly: the type
signature, and also its invariants, ordering constraints, error modes, required
configuration and performance characteristics.

**Implementation**: the code inside a module. It differs from an adapter: a small adapter
can have a large implementation (a Postgres repository), and a large adapter a small one (an
in-memory fake). Say adapter when the seam is the topic, implementation otherwise.

**Depth**: leverage at the interface, meaning the behaviour a caller or test can exercise per
unit of interface it has to learn.

**Deep**: a lot of behaviour behind a small interface.

**Shallow**: an interface nearly as complex as the implementation behind it. A pass-through
module, whose interface mirrors the one call it forwards, is the extreme case.

**Seam** (Michael Feathers): a place where behaviour can change without editing in that
place; the location where a module's interface lives. Where to put a seam is its own design
decision, separate from what goes behind it.

**Adapter**: a concrete thing that satisfies an interface at a seam. It names a role, the
slot it fills, not what is inside it.

**Leverage**: what callers get from depth: more capability per unit of interface learned.
One implementation pays back across N call sites and M tests.

**Locality**: what maintainers get from depth: change, bugs, knowledge and verification
concentrate in one place instead of spreading across callers. Fix once, fixed everywhere.

Relationships: a module has one interface; depth is measured against that interface; a seam
is where the interface lives; an adapter sits at a seam and satisfies the interface; depth
produces leverage for callers and locality for maintainers.

Rejected framings:

- Measuring depth as a ratio of implementation lines to interface lines. It rewards padding
  the implementation.
- Treating the interface as only the type signature or a class's public methods. Callers
  also depend on invariants, ordering and error modes.
- Boundary, which is overloaded with the bounded context of domain-driven design. Say seam or
  interface.

## Substitutions

These words never stand in for the terms above in the survey's own prose. Identifiers quoted
from the code keep their names: a file called `OrderService.ts` is still cited as
`OrderService.ts`.

| Do not write | Write instead | Reason |
| --- | --- | --- |
| component, service, unit (for a module) | module | They blur UI parts, deployables and test granularity into one word |
| API, signature (for an interface) | interface | Too narrow: they name the type-level surface only |
| boundary | seam | Seam says behaviour can change there; boundary does not |
| layer, wrapper (as a substitute for module) | module, or "pass-through module" for a thin one | These words excuse shallow modules instead of naming their depth |

Name modules after the domain glossary. If `GLOSSARY.md` defines Order, write "the order
intake module", not "the FooBarHandler" and not "the order service". When a candidate needs
a concept the glossary lacks, propose the term during grilling.

## Dependency categories

The category decides how the deepened module is tested across its seam.

1. **In-process**: pure computation or in-memory state, no I/O. Always deepenable: merge the
   modules and test through the new interface. No adapter is needed.
2. **Local-substitutable**: a dependency with a local test stand-in, such as an in-memory
   Postgres such as PGlite, or an in-memory filesystem. Deepenable when the stand-in exists;
   tests run against it. The seam stays internal, with no port at the module's interface.
3. **Remote but owned (ports & adapters)**: your own service across a network. Define a port
   at the seam. The deep module owns the logic; production injects an HTTP, gRPC or queue
   adapter and tests inject an in-memory adapter.
4. **True external (mock)**: a third party you do not control, such as payments, email or
   SMS. The deepened module takes it as an injected port, and tests use a mock adapter.

A candidate can span categories; name each one ("local-substitutable database, true external
email").

## Seam discipline

- One adapter means a hypothetical seam; two adapters mean a real one. A test stand-in counts
  as an adapter when the test passes it in at the seam. Module-level mocking (`jest.mock`,
  patching an import) is not an adapter: it works around the seam. Introduce a port only
  when at least two adapters are justified; a single-adapter seam is indirection.
- Internal seams and external seams: a deep module can keep internal seams, private to its
  implementation and used by its own tests, beside the external seam at its interface. Do not
  expose an internal seam through the interface because a test uses it.

## The deletion test

Imagine deleting the module. If complexity vanishes, the module was a pass-through: absorb
it into a deep module. If complexity reappears across N callers, the module earns its keep:
keep it, and say so when a reader would expect it on the candidate list.

## Testing: replace, don't layer

- Once tests at the deepened interface exist, the old tests of the shallow modules are waste;
  delete them.
- Write the new tests at the deepened module's interface. The interface is the test surface.
- Assert observable outcomes through the interface, not internal state.
- A test that has to change when the implementation changes is testing past the interface.

## Card wording

- **Problem**: one sentence saying what hurts today, with no remedy in it.
  - Fits: "Three order callers each sequence validation, tax, the database transaction and
    the confirmation email themselves."
  - Does not fit: "The order flow is messy and could use a better service layer."
- **Solution**: one sentence naming the consolidation and where the seam goes. No method
  names or signatures yet: the interface is designed after the user picks and grilling
  settles the shape.
  - Fits: "Absorb the four pass-through order modules into one order intake module that
    owns the transaction."
  - Does not fit: "Refactor the code with clean architecture patterns."
- **Wins**: 6 words or fewer each, naming the gain in glossary terms, for example
  "locality: tax rules in one module", "leverage: one interface, three callers", "tests hit
  one interface", "transaction handle stays behind the seam".
- Phrases that never earn a place: "cleaner code", "easier to maintain", "best practices",
  "more modular and flexible", and "separation of concerns" without the module and seam it
  means.

Phrasings in the right register: "The order intake module is shallow: its interface nearly
matches its implementation." "Tax rules leak across the seam." "Two adapters justify the
seam: Postgres in production, in-memory in tests."
