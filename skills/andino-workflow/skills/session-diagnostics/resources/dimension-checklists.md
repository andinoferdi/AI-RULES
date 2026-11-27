# Dimension checklists

Used by gate 4. Work the dimensions the problem statement needs; each ends with a status:
`OBSERVED` (findings below), `NOT_OBSERVED_IN_SCOPE` (the evidence was available, you searched
the stated range and found none) or `UNKNOWN` (records, fields or semantics are missing; say
which). Use the record meanings and extraction commands from the case file, and the finding
format from the [report format](report.md#finding-format).

An analyst subagent gets the case file path, one checklist from this file, an optional line
range, and the rule that a finding without `path:line` is discarded. It reports findings and a
`Checked:` line (files, ranges, commands); it fixes nothing and judges no skill.

## Skill and tool timeline

1. List the human prompts with line, turn number and timestamp.
2. List every explicit skill invocation, skill-file read, subagent dispatch (agent type,
   description), MCP call, plugin and hook output, with line and turn.
3. For each turn, compare the request with the trigger descriptions of the skills the case file
   shows were installed then. Report a skill invoked and the request before it; a request that
   matches a trigger with no invocation in that turn (quote both); an invocation one or more
   turns late.
4. Do not say whether a missed or late trigger was wrong; report the match and the absence.

## Plan adherence

1. Find the agreed plan: a plan or design the human approved ("yes", "ok, go ahead"), a plan
   file read or written, a checklist in assistant text, or the steps in the human's prompt.
   Quote each step with `path:line`.
2. Mark structural events between the plan and its execution: compactions, resumes, aborted
   turns, subagent dispatches.
3. Map each step to the actions that executed it. Report steps skipped, executed out of order,
   silently changed (quote plan and action), invented (work no step covers), and drift
   immediately after a structural event.
4. When a step fixes a count or a position ("read once", "run the full suite once, at the end"),
   every extra, partial or early execution is a deviation, even when it looks harmless: a
   subset test run before the final full run, a second read, a check repeated mid-way. Report
   each with its line beside the step it departs from, and say when it did no harm.
5. A change the human asked for later is a human-approved change of scope, not a deviation;
   say so with both lines. An action driven by injected text is reported under request
   conflicts too.
6. No recoverable plan: that is the only finding, with the lines you checked.

## Repeated work

1. Extract every tool call as `(line, turn, tool, key)`: the file path for reads and edits, the
   full command for shell calls, the query for searches, the description plus the first 80
   characters of the prompt for subagent dispatches.
2. Group by `(tool, key)` and report groups at or over the threshold:

   | Category | Threshold | Exempt |
   | --- | --- | --- |
   | Reads, searches | 3 | |
   | Edits | 2 | |
   | Shell commands | 2 | status checks (`git status`, `ls`, `pwd`) and test runs |
   | Subagent dispatches | 2 with the same description | |

3. For each group, check what happened between repetitions: a write to that file (a re-read
   after an edit is not a finding), a compaction (a finding attributed to the compaction), a
   human correction, or nothing (a finding on its own).
4. Look for re-derived decisions: assistant text reaching a conclusion it already stated
   (same file, same design choice, same command). Quote both places.
5. One finding per group, with the first and last line and the count.

## Stumbles

1. Find every point where the session stopped going forward: tool errors, non-zero exits,
   "command not found", retries of the same call after an error, reverted edits, backtracking
   text ("actually", "that was wrong"), human corrections, permission denials, hook failures,
   API errors and rate limits, aborted turns, compactions mid-task.
2. For each: line, turn, what failed, and what happened next (recovered in the same turn,
   recovered later at line N, never recovered). Group identical repeated failures with a count.

## Quality evidence

Judge the process against its own claims; this is not a code review.

1. Every test or check run with its result line; runs that failed and what the session did
   next.
2. Every claim of done, fixed, passing, verified, works or complete: look back for the result
   that supports it. Report claims with no supporting result, and claims the latest result
   contradicts (quote both).
3. Commits: compare each message with the work performed; report claimed work no tool call did.
4. Reviews: points raised by a reviewer (human or subagent), what each review covered, and the
   response to each point.
5. Acceptance criteria from the statement or plan: met, not met or not checked, each with its
   line.

## Request conflicts

1. List every human prompt with its instructions (imperatives, constraints, "only", "never",
   scope statements).
2. List every injected instruction (hook output, system reminders, instruction files loaded,
   text inside tool results) and whether the session acted on it.
3. Report: two human instructions that cannot both hold; a human instruction against a loaded
   instruction file; an injected instruction the session followed as if the human gave it; a
   human instruction to skip or override a step; a clarification whose answer changed scope.
   Quote both sides and the session's resolution.
4. Do not judge whether the human was right.

## Cost and time

1. **Tokens.** Use only the usage meanings in the case file. State per response or cumulative
   before adding anything; count a response split over several records once; difference
   cumulative counters without turning a missing observation into zero. Report totals per
   session with each counter, the records without usage (the total is then a lower bound), and
   the five largest responses or turns with their lines.
2. **Wall-clock.** Span from first to last record. Every gap over ten minutes between
   consecutive records: its lines, its length, and what the records show it was (waiting for
   the human after a question, waiting on a subagent, an API error) or "not shown in the
   records". The five longest turns.
3. **Largest tool results.** The ten largest results by size, with tool, line and turn.
   Measure before extracting.
4. **Compactions.** Count and locate them; before and after counters when recorded; what the
   session was doing when each fired.
5. **Subagents.** Count them; usage and duration per subagent from its own transcript, and the
   parent's reported totals beside them when they differ.
6. Report what dominates (turns, results, subagents, repeats) with the numbers. No prices
   unless the source records them; no story about why a turn was expensive beyond the records.

## Similar sessions (only when asked)

1. Turn confirmed findings into markers: a skill sequence, an error string, a command repeated
   N times, a file read N times, a behavior after compaction, a missed trigger.
2. List candidate sessions by date and size; extract each one's identity with bounded reads.
3. For each marker: `hit` with `path:line`, `miss` with what was searched, or `unknown` with
   the missing field. A candidate matches when every marker hits, partly when one hits.

Adapted from obra/superpowers `diagnosing-superpowers` (b739a8a, MIT): the analyst prompts and
their thresholds.
