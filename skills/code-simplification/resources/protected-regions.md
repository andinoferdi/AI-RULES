# Non-mutating protected-region procedure
Preserve exact bytes between simplify-ignore-start and simplify-ignore-end, including markers and line endings, in a scoped before snapshot. Hash the block, not a normalized rendering. Keep reason (performance/platform/generated/contract) alongside it.
Read source normally. The protection is an editing constraint, never a tool that swaps source to placeholders. Edit surrounding code, extract matching blocks again and compare count/order/content hashes. A changed, missing, duplicated or moved marker requires explicit review, not silently accepting “equivalent” code.
Single-line annotations protect the entire line; prefer dedicated marker lines. Unterminated/nested/nonstandard comment forms need clarification rather than partial parsing. Rename or concurrent edit invalidates a path-only baseline.
If interrupted, inspect current source and saved owned snapshot. Restore only a verified owned edit after comparing current bytes; preserve unrelated changes. Never restore a stale whole-file backup or delete recovered content. A hook's exit 2/masking payload is not an error-recovery authority.
Example: simplify outer branching while unrolled hot loop stays byte-identical; behavior and performance remain separately verified. Never install the upstream source-masking hook on Read.

Provenance: independently worded adaptation of the Addy snapshot identified in the owning GUIDE.md; full MIT notice at ../../../references/legal/addy-license.md. No upstream installation or hook is required.
