# Performance optimization skill quality

- BASE `915d5e9306c96dd5d854d312e48f3348708951c3` on `andino-workflow`.
- State VERIFIED LOCALLY. Publication and setup read-back pending.
- Decision EXTEND the existing member. Keep the evidence and permission boundaries, local resources, operational example, and discovery identity. The Addy reference offers an easier symptom-to-measurement path. Keep that path in the entry point and domain details in existing resources.
- Evidence Static walkthrough of three cases. For a slow landing page with a fast TTFB, the current entry lists several phases but does not ask for LCP subpart attribution before choosing a fix. For slow API p95, it names possible dependencies but does not ask for per-request timing and query counts before recommending a query or pool change. For a source-only review it already requires NOT MEASURED, but leaves the next diagnostic and decision format implicit. This is a document review, without independent model runs.

## Execution

1. Replace the compressed procedure in `skills/performance-optimization/SKILL.md` with Measure, Identify, Fix, Verify, and Guard. Define baseline comparability and an actionable routing table for page load, interaction, API, database and missing data. Keep the existing operational fixture and its expected outputs.
2. Add a compact evidence record to the existing output section. Require source, sample setup, hypothesis and counterevidence, before/after, correctness, verdict, and guard or next measurement. In `resources/performance-audit.md` add LCP subpart attribution. In `resources/optimization-patterns.md` add query-count versus queue-wait discrimination and safe plan capture.
3. Check the three walkthroughs against the updated entry point and resources. Run the positive and negative operational example, verify relative links, and run `git diff --check`.
4. Commit and push `andino-workflow`. Run `ai-rules setup --host codex --capability andino-workflow --scope global --source latest --yes --non-interactive --no-progress`. Compare the installed member and bundled copy with the committed skill and resources.

## Local acceptance evidence

- Frontend walkthrough: fast TTFB and late image request now lead to LCP resource load delay, discovery and priority. An early download with a late paint instead leads to render-blocking work and main-thread inspection.
- Backend walkthrough: p95 regression now leads to slow-request spans and query count by input size. Growing query count selects repeated work, while stable execution with high acquisition wait selects connection hold time and capacity.
- Source-only walkthrough: return potential impact, NOT MEASURED and the one capture needed to choose a fix. Field and synthetic conclusions remain separate.
- Extracted Python fixture passed both published examples (101 → 61 ms, keep; 101 → 99 ms, restore). All relative Markdown links in the skill and resources resolved. `git diff --check` passed.

NEXT ACTION Commit only the performance files and this plan, push, then verify latest setup read-back.
