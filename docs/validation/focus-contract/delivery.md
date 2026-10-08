# Focus cleanup and delivery verification

Date: 2026-10-08. All six distribution branches inspected. Runtime branch scope is
the skill package; main owns installer, tests and evidence; WebBased owns web rules.

## Published implementation

| Branch | Commit | Message |
| --- | --- | --- |
| focus | 9eb6081aa1ae26a4bb81a38eb49e4b1f9b9c3da3 | docs: strengthen focus communication defaults |
| WebBased | bfc704e8db939bfcfc3e05eb145d9922ccc9e76a | docs: align web focus rules with stronger defaults |
| main | 422de548cb04be1b457dc159ee3d8931b940ade1 | chore: pin latest focus and preserve paired evaluation evidence |

All three commits were pushed to the matching `refs/heads/*` on
`origin` (`https://github.com/andinoferdi/AI-RULES.git`), then compared with
`git ls-remote`. The final documentation checkpoint has its own commit; this
report intentionally records the already verified implementation commits.

The remote-only branches andino-workflow (f47eac4), ai-codebase-rescue (b34f4d7),
and skripsi-skill (6f7c57c) contain valid package resources and remain unchanged.
No empty commits, force pushes, history rewrites, submodules or nested repositories
were introduced.

## Cleanup and references

- Moved the 60 inference records, snapshots, scripts and report from the Focus
  worktree into main; runtime package remains exactly three tracked files.
- Removed only build output, generated egg-info, bytecode caches and now-empty
  source directories created by this task. See [cleanup proof](cleanup-verification.json).
- Existing `.gitignore` already covers generated outputs; no ignore change or
  tracked-file removal was needed. Source, fixtures, historical proof, completed
  plans still referenced by documentation, global configuration and installer
  backups were preserved.
- Evaluation scripts now use branch refs by default and optional checkout paths.
  Removed their machine-specific paths and RTK dependency. Snapshot/transcript
  content remains historical evidence and was not rewritten.
- Main README links to the new evaluation report. evals/README.md now correctly
  describes four skills rather than three. Other README sections in WebBased
  remain identical to the evaluated baseline.
- Six-branch relative Markdown link scan passed after checking a parser false
  positive for a balanced-parenthesis filename. New main working-tree links pass.
  Credential-shaped pattern scans and staged-scope review had no findings. These
  are bounded checks, not a claim that every possible secret format was detected.

## Executed verification

| Check | Observed result |
| --- | --- |
| `python -m unittest discover -s tests` using checkout src | 132 tests PASS, 58.978 seconds |
| `python scripts/validate_skills.py --focus-ref focus` | Four packages, metadata, links and eval schemas PASS |
| `python scripts/validate_andino_capabilities.py --cases-only` | 34 schemas PASS |
| `python scripts/validate_skripsi_traceability.py` | 335 requirements, 32 capabilities, 110 initial eval owners, 75 task records PASS |
| `python docs/validation/focus-contract/verify_eval.py` | Stored 60 real inference records and structural/format checks PASS; semantic limitations retained |
| `git diff --check`, staged review, Python/JSON syntax | PASS on affected branches/files |
| `python -m pip install --no-deps --no-build-isolation .` | CLI wheel built and installed successfully |
| Latest-source global setup, five hosts, existing everything profile | Five Focus UPDATEs, 15 other target NO_OPs; all 20 VERIFIED |
| Repeat latest-source global setup | 20 NO_OPs |
| Actual installed CLI, fresh project, `--source bundled --capability focus` | Exact new Focus package installed; no workflow added |
| Implementation GitHub Actions | [Validate skills run 37763069078](https://github.com/andinoferdi/AI-RULES/actions/runs/37763069078) succeeded at main 422de54 |

The full test command was executed through a Python runner inserting `src` into
sys.path, ensuring the edited checkout implementation rather than a stale installed
package was tested. No unnecessary model rerun was performed: cleanup did not alter
the evaluated communication text.

## Installed update

The default `ai-rules setup` already uses `--source latest` and fetches configured
distribution branches. No new activation or update mechanism was added.
Main release sequence 7 now pins Focus sequence 2 to 9eb6081 for bundled installs;
the installed CLI contains the same pin.

Actual command executed:

```powershell
ai-rules setup --host codex --host claude-code --host opencode --host antigravity-cli --host antigravity-ide --profile everything --source latest --non-interactive --yes
```

Full package content and entrypoints match on all five global installations.
The existing profile and its four capabilities are preserved. See
[setup proof](setup-verification.json). Installing files does not reload an
already-running model session; use a new session or reload the host to load them.
Behavioral caveats remain in the [paired evaluation report](report.md).

No unrelated user changes were detected or discarded. Final Git SHA/status and
cleanup of the temporary managed worktrees are verified after this documentation
commit and reported in the execution response.
