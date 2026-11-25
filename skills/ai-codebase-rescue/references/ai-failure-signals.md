# Signals common in rushed or agent-made patches

Use during scoped evidence gathering, after the target is chosen, and again on your own
diff before reporting. These are inspection leads. A signal becomes a finding only with
its evidence check. Provenance never proves a defect, and the same checks apply to code
written by people.

## Signal table

| Signal | Evidence check | Typical disposition |
| --- | --- | --- |
| Phantom import or API: a module, function, method or argument that does not exist in the installed code or dependency version | Resolve the import and the symbol in the repository or the installed package; run the path that uses it | REFACTOR to a real API, or an explicit unsupported error with the owner decision recorded. Never invent the missing symbol to make the import pass |
| Phantom package: a dependency that is not in the manifest or lockfile, often behind a silent import fallback | Read the manifest and lockfile; look up the registry only when network use is authorized; names close to popular packages are a typosquatting risk | REMOVE the phantom branch. Never install it to make the code work |
| Swallowed error or fake success: a broad catch that returns success, a default value or an empty result | Inject a failure in a fixture and observe what the caller and the stored state report | REFACTOR so failure is observable to the caller; keep "does not crash" only if the contract requires it |
| Silent fallback path that hides a broken primary path | Disable the fallback in a test and see whether the primary path works | REFACTOR or REMOVE, with the fallback's real purpose recorded |
| Duplicated rule that diverged: two near-identical functions or constants used by different callers | Diff the copies; run both with the same contrasting inputs | REFACTOR to one owner; pin both paths first |
| Test double, stub or sample data reachable from production code | Trace imports of mocks, fakes and fixture files from production entrypoints | REFACTOR or REMOVE |
| Placeholder logic: TODO returns, hard-coded results, commented-out checks | Read the path; check whether a caller depends on the placeholder | INVESTIGATE or REFACTOR |
| Over-abstraction: many shallow classes, single-implementation interfaces, wrappers that add nothing | Count what a caller must know; check whether the layers ever vary | REFACTOR by merging, or KEEP when the seam is used |
| Silently deleted or overwritten logic | Compare the current function with its history; search history for removed literals | REFACTOR to restore the verified rule, with the contract cited |
| Out-of-scope edits bundled with a fix | Read the diff of the suspect commit for unrelated files | INVESTIGATE; separate or revert only with owner authority |
| Tests that assert the mock or enshrine the bug | Check what each assertion would catch if the code broke | Replace with a contract assertion, recording the reason |
| Hard-coded secrets, URLs or environment values | Search the target for credentials and environment-specific literals; redact in evidence | Security reference; contain and report |
| Config, plugin or registry drift: code used only through configuration | Search config files, plugin lists and string references before calling code dead | KEEP or INVESTIGATE; REMOVE only with obsolescence proof |

## Scoped sweep

Sweep the target files and the files your change touches, not the whole repository.

```sh
# Imports used by the target, to resolve one by one
grep -rnE "^\s*(from|import) " <target_paths>
grep -rnE "require\(|from ['\"]" <target_paths>

# Broad catches and what they return
grep -rnE "except( +(Exception|BaseException)( +as +[A-Za-z_]+)?)? *:|catch *\(" <target_paths>

# Logic that disappeared: history of one function, and commits that removed a literal
git log -L :<function_name>:<file> --oneline | head -60
git log -p -S'<removed literal>' -- <file>

# Code reachable only through configuration
grep -rn "<module_or_class_name>" --include='*.json' --include='*.toml' --include='*.yaml' --include='*.cfg' --include='*.ini' .
```

Python check that every import in a file resolves, without installing anything:

```sh
python -c "import importlib, sys; [importlib.import_module(m) for m in sys.argv[1:]]" pkg.module_a pkg.module_b
```

An import that only fails on a rare branch (inside a function, behind a condition)
needs that branch executed in a test; a module-level import check does not reach it.

## Record the sweep

For each signal checked, record the evidence and the result, including signals checked
and not found ("no broad catches in pricing/"). An unchecked signal stays unknown; do not
describe the target as clean beyond the checks you ran.
