# Context Pointer Engineering and Leading Words Catalog

Internal method ID: `andino-agent-document-authoring` resource: `context-pointer-and-leading-words.md`.

---

## 1. Mechanics of Context Pointers

A **context pointer** is a reference held in the agent's active context window that names an out-of-context resource and encodes the exact condition for reading it.

Examples of context pointers:
- The `description` field in a skill's YAML frontmatter.
- A bullet point in `CLAUDE.md` or `AGENTS.md` pointing to an operational runbook.
- A conditional reference link in a step-by-step procedure.

### The Pointer Paradox
The wording of the pointer—**never the quality of the target file**—decides whether the agent reaches the material. If a critical procedure is hidden behind a weakly worded pointer, the agent will never read it. A must-have target behind a weak pointer is a variance defect: sharpen the wording first; inline the material only if sharpening repeatedly fails.

### The Two Jobs of a Context Pointer
1. **Identify the resource:** Name the specific artifact, path, or tool clearly.
2. **Encode the branch condition:** State the exact, falsifiable trigger that warrants reading it.

### The Three Golden Rules of Pointer Drafting

1. **Front-load the leading word:**
   Place the primary conceptual trigger at the very beginning of the pointer line. The model scans tokens sequentially; front-loaded triggers anchor routing attention before context load decays.
   - *Weak:* "For details on how to handle database migration errors during production rollout, consult `db-migration.md`."
   - *Sharp:* "`db-migration.md`: Database schema rollbacks and migration deadlock recovery."

2. **One trigger per distinct branch:**
   Synonyms that describe the same branch inflate context load without increasing routing reliability.
   - *Bloated:* "Read `auth.md` when configuring login, authentication, signin, user sessions, or SSO."
   - *Pruned:* "`auth.md`: Authentication providers and user session lifecycle."

3. **Cut identity the body already carries:**
   Do not explain in the pointer what the target file explains in its first paragraph. The pointer exists solely to decide *whether* to open the file.

---

## 2. Leading Words: Recruiting Pretrained Priors

A **leading word** is a compact concept already living in the model's pretraining that the agent thinks with while executing instructions (*tracer bullet*, *tight loop*, *red-green*, *SSOT*, *sediment*).

### Why Pretrained Words Win
Repeated as a token—never as an explanatory paragraph—a leading word accumulates a distributed definition and anchors a complex behavioral pattern in minimal tokens. 

- **Coining your own jargon** (e.g., *"The Quad-Phase Synchronous Boundary Matrix"*) forces you to spend dozens of tokens defining it. You pay in definition tokens what a pretrained word delivers for free.
- **Pretrained tokens** immediately activate established latent representations, guiding execution paths with zero cognitive friction.

### High-Leverage Leading Words Catalog

| Verbose / Descriptive Anti-Pattern | Sharp Leading Word | Pretrained Model Association Recruited |
| :--- | :--- | :--- |
| "Fast, deterministic, low-overhead loop" | **tight** | Uninterrupted, iterative, rapid execution with minimal distraction. |
| "A test failure that you trust and verify before writing code" | **red** (as in red-green) | Strict TDD disciple; assertion fails exclusively due to missing implementation. |
| "The single authoritative place where this configuration is defined" | **SSOT** | Single Source of Truth; zero duplicate state; single-file updates. |
| "A minimal end-to-end slice cutting through all architectural layers" | **tracer** | Thin vertical slice proving integration before broad horizontal expansion. |
| "Accumulated historical guidelines that are no longer actively relevant" | **sediment** | Outdated procedural layers; targets for ruthless pruning. |
| "Strict minimum non-negotiable requirements that cannot be relaxed" | **floor invariant** | Absolute lower bound; non-debatable constraint enforcement. |
| "Raw machine-parseable command output without terminal formatting" | **porcelain** | Script-safe, deterministic CLI output (`git status --porcelain`). |
| "Persistent, unyielding, and exhaustive verification" | **relentless** | Refusal to stop before every single assertion and edge case is checked. |

---

## 3. Defeating the Negation Trap

### The Mechanics of Negation Failure
In LLM attention architectures, steering by prohibition drags the forbidden behavior directly into the active attention window:

$$\text{Attention}(\text{"DO NOT deploy without tests"}) \rightarrow \text{Salience}(\text{deploy}) \uparrow, \text{Salience}(\text{without tests}) \uparrow$$

Like the human mind instructed *"don't think of a pink elephant"*, the model's probability distribution concentrates on the strongly-activated semantic concept *pink elephant*. The word "not" is a weak syntactic modifier that high-temperature sampling or long context easily overruns. Consequently, negative bans often read to the model as an implicit suggestion to perform the forbidden action.

### The Positive Target Steering Protocol
Convert every prohibition into an affirmative, positive target action:

| Negation Anti-Pattern (Elephant in Context) | Positive Target Steering (Sharp & Enforceable) |
| :--- | :--- |
| "DO NOT write long, complex, nested helper functions." | "Author flat, single-purpose functions under 25 lines." |
| "Never commit unverified code to the main branch." | "Verify all test suites exit code 0 before initiating git commit." |
| "Do not hallucinate external libraries." | "Use only dependencies explicitly declared in `package.json`." |
| "Avoid using vague step completion messages." | "Terminate each step with an observable binary predicate (e.g. `test -f dist/bundle.js`)." |

### When Prohibitions Are Legitimate
A prohibition earns its place **only** as a hard safety boundary that cannot be phrased positively (e.g., *"Never delete production databases or modify user credentials"*). Even then, you must immediately pair the negative guardrail with the approved positive alternative:

> *"Do not drop production database tables. To prune test data, execute `npm run db:clean:test` targeting the local sandbox environment."*
