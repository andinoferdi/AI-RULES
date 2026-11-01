# Non-Mutating Protected-Region Procedure

This document specifies the mandatory protocol for identifying, hashing, and preserving performance-critical, platform-dependent, or compliance-bound code regions during simplification.

---

## 1. Protected Region Syntax Across Languages

Protected regions are delineated by standard comment pairs tailored to the host language syntax. Markers must occupy their own dedicated lines.

### Supported Language Formats

| Ecosystem | Start Marker | End Marker |
|---|---|---|
| **JS / TS / Java / C# / Go / Rust** | `// simplify-ignore-start` | `// simplify-ignore-end` |
| **Python / Ruby / Bash / YAML** | `# simplify-ignore-start` | `# simplify-ignore-end` |
| **C / C++ / CSS / SQL** | `/* simplify-ignore-start */` | `/* simplify-ignore-end */` |
| **HTML / XML / JSX / Markdown** | `<!-- simplify-ignore-start -->` | `<!-- simplify-ignore-end -->` |

### Single-Line Directives
For isolated statements (such as compiler directives, inline assembly, or unrolled singletons):
- `// simplify-ignore-line`
- `# simplify-ignore-line`

A single-line directive protects the entire line it resides on or immediately annotates.

---

## 2. Why Code Is Protected (Chesterton's Fence in Practice)

Never assume "ugly" or "verbose" code is accidental. Protected regions typically fence:
1. **Micro-Optimizations & Hot Paths**: Unrolled loops, bitwise manipulations, cache-line friendly layouts, and pre-allocated buffers where idiomatic functional transformations (e.g. `.map()`, list comprehensions) would incur garbage collection pressure.
2. **Platform & Hardware Quirks**: Endianness checks, browser engine edge-cases, memory-mapped I/O, or OS-specific syscall wrappers.
3. **Cryptographic Primitives**: Constant-time execution loops designed to defeat side-channel timing attacks.
4. **Legal & Licensing Constraints**: Attributed third-party routines, patent-encumbered algorithms, or regulatory compliance calculations.

---

## 3. Operational Integrity Protocol

Whenever an agent touches a file containing protected markers, it MUST adhere to the following 5-phase cryptographic invariant:

### Phase 1: Pre-Edit Snapshot & Hash Baseline
1. Scan the target file for marker pairs.
2. Extract the exact raw bytes between the start marker (including the marker line) and the end marker (including the marker line).
3. Compute the raw SHA-256 digest of the extracted bytes:
   $$\text{Baseline Hash} = \text{SHA256}(\text{RawBytes})$$
4. Record the count, order, and identifiers of all protected regions in the task memory.

### Phase 2: Bounded Editing
- You may refactor, flatten, and simplify code **surrounding** the protected block (e.g. caller parameter setup, validation guard clauses, and consumer return logic).
- You MUST NOT touch, re-indent, re-wrap, or format any byte within the protected markers.
- Never use placeholder masking tools or synthetic mock replacements on Read. Read the source code in its authentic state.

### Phase 3: Post-Edit Hash Verification
1. Extract the raw bytes of the protected region from the edited file.
2. Compute:
   $$\text{Post-Edit Hash} = \text{SHA256}(\text{EditedBytes})$$
3. Assert:
   $$\text{Baseline Hash} == \text{Post-Edit Hash}$$
4. If the hashes differ by even a single byte or newline character, the modification is immediately REJECTED.

### Phase 4: Emergency Rollback
If verification fails:
- Immediately discard the uncommitted edit.
- Restore the original file from the pre-edit snapshot.
- Do NOT attempt to "patch" the protected region back into compliance with guess-work. Re-evaluate the refactoring seam from scratch.

---

## 4. Anti-Patterns & Prohibitions

| Violation | Why It Fails | Mandated Correction |
|---|---|---|
| **Re-formatting Whitespace** | Running Prettier/Black over a protected block alters its byte hash and may break alignment assumptions. | Exclude protected regions from automatic linters/formatters or configure them to respect ignore pragmas. |
| **Inlining Protected Logic** | Moving a protected loop into a shared helper function obscures its context and risks breaking caller scope. | Keep the protected block anchored exactly where its author placed it. |
| **Partial Marker Matching** | Unterminated start markers or unmatched end markers. | Treat missing or malformed markers as a blocker; halt simplification and prompt for clarification. |
| **Renaming Passing Variables** | Renaming a variable that flows into a protected block without verifying internal references. | Preserve the identifiers consumed by the protected block exactly. |

---

## 5. Provenance

Independently authored for Andino Workflow under MIT license, adhering to the quality criteria established in `references/legal/addy-license.md`.
