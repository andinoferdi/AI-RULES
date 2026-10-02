# Publication and developer handoff update

Date: 2026-10-02. The user explicitly authorized final cleanup, commit and normal push. PM accepted implementation without a blocking runtime revision. Full live/cross-host acceptance remains open.

Published runtime: [andino-workflow commit effc3b8](https://github.com/andinoferdi/AI-RULES/commit/effc3b8d7326d121317da86aff205de7c0bb0e80). Its six changed Markdown files contain 55 contracts; the adaptive core and existing UI coexistence reference remain preserved. Content SHA256: `dc9916a964011c8c7d16c977f614616db949e0643d5b0efa0aa3b47edb7f8447`. No runtime executables or dependency installation were added.

The installer already defaults to remote branch freshness. No installer behavior rewrite was necessary. The stable frozen manifest advances only the Andino commit and its release sequence to 3; the global sequence also advances to 3. Rescue and Skripsi pins remain unchanged. Explicit `--source bundled` remains a frozen release choice.

[Remote setup proof](setup-publication-proof.json) records an actual default-source `setup` against GitHub, using a disposable Codex project and isolated state directory. Starting from the prior official runtime copy, setup installed the published SHA and exact content hash, retained a backup and a verified provenance lock. A second setup returned NO_OP. No user/global installed skill was changed.

```sh
ai-rules setup
```

Select the intended hosts/profile. Default latest mode checks configured remote branches and updates recognized clean installations. Local modifications, unrecognized copies, incompatible clones, unavailable sources and concurrent changes stop the operation with an explanation; personal content is preserved. Restart the agent session if its loader requires it. Existing older CLI versions need the one-time CLI refresh described in the root README to gain this behavior.

Current-runtime evidence: [six-case review](current-runtime-review.md), 4 scoped PASS / 2 NOT_VERIFIED. The [original 13-field handoff](capability-handoff.md) remains an explicitly historical review checkpoint; [traceability](capability-traceability.json) separately records current evidence and historical records. Full MCP routing, unavailable services and other host coverage are not claimed as PASS.

Cleanup adds a precise ignore for only the root `kirim gpt` review export directory. That previously prepared packet is absent at the final filesystem check; this cleanup neither deletes nor recreates it. Owned authoring helpers/catalogs under ignored `.ai-rules` are archived outside the repository. Portable source, tests, evaluations, raw validation records and the active checkpoint are retained. No force push, destructive Git cleanup, branch deletion or global skill replacement was used.

Whitespace review preserves the accepted runtime bytes and its evaluated hash. Git's default whitespace check flags one terminal blank separator in the registry; the scoped check with `core.whitespace=-blank-at-eof` passes. This format-only exception is recorded rather than silently claiming the default check passed.

Verification results are recorded in [publication checks](publication-checks.json). Repository publication completes the authorized delivery; the active checkpoint retains the concrete next action for remaining live acceptance.
