# Code simplification quality

Status: COMPLETE
Phase: publication

The existing skill preserves behavior and protected regions but puts its decision procedure in the companion guide. The upstream entrypoint makes the workflow easier to find. Both catalogs contain recipes whose semantic preconditions are easy to miss.

## Decisions and tasks

1. Update `skills/code-simplification/SKILL.md` and `GUIDE.md` on the workflow branch. Put the baseline, candidate selection, incremental edit, and verification sequence in the entrypoint. Retain the existing negative gates, protected-region policy, ledger and provenance. A clean target should produce a no-change result.
2. Correct the TypeScript recipes and validate against cases for effect order, inherited lookup keys, return shape and synchronous throws at a promise boundary. Keep the existing offline protected-region probe. These are deterministic checks, separate from measuring model output.
3. Commit and push the workflow branch, then advance the stable manifest on main to that commit. Run the installer path in isolated projects and compare installed entrypoints and resources to the pinned tree. Keep unrelated local changes out of the publication.

Baseline: workflow branch matches origin at `6b4ac613`. Stable manifest still pins `6ce1030e`.

## Evidence

- Published workflow revision `b5b400e266c16ec3fbd0f208db6036d53d53b5d1`. The stable pin advances to sequence 27 and includes the other workflow changes already published on that branch.
- Default Codex setup installed the published skill and matched the selected files byte for byte. The bundled distribution test passed on five hosts for all seven files at both installation paths.
- The offline probe exercised seven inputs and detected the protected-byte mutation. JavaScript probes checked inherited keys, sparse traversal, object shape, read order and synchronous throws at the async boundary.
- The broad validator reported an unexpected runtime file in the separate `search-first` package. Comparative model output was not measured.

NEXT ACTION: None. Default setup consumes the published branch and the bundled source uses the new stable pin.
