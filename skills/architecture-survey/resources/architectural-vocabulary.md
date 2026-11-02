# Architectural Vocabulary and Output Shaping

Internal method ID: `architecture-survey`. Supporting resource for `skills/architecture-survey`.

This resource defines the mandatory lexical standards, output-shaping rules, and diagnostic deletion criteria for architecture surveys. Adherence to these standards prevents semantic drift (*semantic slop*) and focuses AI reasoning on structural realities rather than rhetorical prose.

---

## 1. The 10 Canonical Terms

All architecture surveys must express findings using strictly these 10 nouns and verbs:

| Term | Operational Definition | Concrete Architectural Grounding |
| :--- | :--- | :--- |
| **`module`** | A bounded unit of software providing functionality behind an interface. | A class, cohesive package, or file cluster with an explicit public boundary. |
| **`interface`** | The public surface area through which callers invoke a module. | Function signatures, exported types, and method declarations exposed to callers. |
| **`implementation`** | The internal logic, state management, and private helpers hidden behind an interface. | The code inside the module that callers cannot and must not see or rely upon. |
| **`depth`** | The ratio of internal implementation volume and leverage to interface surface area. | High implementation volume hidden behind a tiny interface = deep. |
| **`deep`** | A module with a small, high-leverage interface that conceals significant internal complexity. | 1 public method (`submitOrder`) coordinating transactions, validation, and side-effects. |
| **`shallow`** | A module whose interface is nearly as complex as its underlying implementation. | A pass-through wrapper whose signature mirrors its 1-line internal SQL or helper call. |
| **`seam`** | A join point where implementation details can be altered or substituted without editing callers. | An interface boundary allowing an in-memory test fake to replace an external dependency. |
| **`adapter`** | A concrete translation layer connecting a module across a seam to a specific technology. | A Postgres repository adapter or an HTTP transport controller. |
| **`leverage`** | The cognitive and mechanical advantage gained when 1 interface eliminates work across $N$ callers. | Absorbing 4 scattered caller-side coordination steps into 1 authoritative call site. |
| **`locality`** | The physical concentration of related invariants and business rules into a single module. | Validation and state changes occur in the same place where data lives, not in callers. |

---

## 2. Banned Substitutions Table

Do not drift into generic or corporate jargon. When an architectural concept is discussed, use the exact canonical noun:

| Banned Term | Why It Is Prohibited | Mandatory Replacement |
| :--- | :--- | :--- |
| *component* | Ambiguous; conflates UI presentation elements with structural modules. | **`module`** |
| *service* | Vague; implies an RPC microservice or bloated corporate helper class. | **`module`** |
| *unit* | Conflates testing granularity with architectural cohesion. | **`module`** |
| *API* | Overused; confuses external HTTP endpoints with in-process module interfaces. | **`interface`** |
| *signature* | Too narrow; describes typing mechanics rather than contract boundaries. | **`interface`** |
| *boundary* | Imprecise; does not specify whether substitution is possible. | **`seam`** |
| *layer* / *wrapper* | Often used to rationalize shallow pass-through classes without depth. | **`shallow module`** (if thin) or **`adapter`** (if seam-justified) |

---

## 3. Output-Shaping Invariants

Every candidate card in both the HTML report and the terminal summary card must adhere to strict structural constraints:

### A. Problem Specification (Exactly 1 Sentence)
State purely what hurts today without proposing remedies or offering excuses.
- **Correct:** *"OrderController forces every caller to manually coordinate database transactions, tax math, and notification events."*
- **Incorrect:** *"The order processing flow is currently messy and could be improved by creating a better service layer to handle things."* (Fluffy, multiple clauses, vague).

### B. Solution Specification (Exactly 1 Sentence)
State the exact structural consolidation or seam encapsulation.
- **Correct:** *"Consolidate the 4 shallow wrappers into a deep OrderIntake module behind a single transactional submit seam."*
- **Incorrect:** *"We should refactor the code and implement clean architecture patterns."* (Vague, lacks target module and seam definition).

### C. Wins Formulation ($\le 6$ Words per Bullet)
Every win must follow the formula `[Glossary Category]: [Quantified Claim]`:
- `locality: pricing logic concentrates in module`
- `leverage: 1 interface replaces 4 wrappers`
- `tests hit 1 public seam`
- `seam hides database transaction handles`
- `deletes 140 lines of boilerplate`

### D. Prohibited Fluff Phrases (Anti-Slop Filter)
The following phrases are strictly forbidden in all survey outputs:
- *"cleaner code"*
- *"easier to maintain"*
- *"industry best practices"*
- *"more modular and flexible"*
- *"separation of concerns"* (unless accompanied by exact seam and module definitions)

---

## 4. The Deletion Test for Shallowness

The core diagnostic test for identifying candidates:

$$\text{Deletion Test} = \begin{cases} 
\textbf{Concentrates Complexity:} & \text{Shallow module (Consolidate into parent/deep module)} \\ 
\textbf{Scatters Complexity:} & \text{Load-bearing seam (Preserve and encapsulate)} 
\end{cases}$$

- **The Question:** *"If this module were deleted, would complexity vanish or merely disperse back into callers?"*
- If deleting the module removes unnecessary boilerplate, pass-through getters, and parameter translation without scattering logic across multiple callers, **the module is a shallow wrapper ripe for deepening**.
- If deleting the module forces $N$ disparate callers to reinvent coordination logic independently, **the module represents a load-bearing seam**.

---

## 5. The Two-Adapter Rule for Seams

Never introduce an abstraction or interface without proven variation:
1. **One Adapter = Hypothetical Seam:** An interface with only one production implementation and no testing substitution is accidental complexity. Collapse the abstraction.
2. **Two Adapters = Justified Seam:** A seam is justified only when two distinct implementations exist (e.g., PostgreSQL in production and In-Memory repository in unit tests; or REST and CLI adapters).
