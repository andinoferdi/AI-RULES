# Explain what happened in an agent session — supporting contract

## Case

Problem statement (session, range, expected, actual, observable; bundle or issue wanted).
Sources: absolute paths, role (main or subagent), lines, bytes, longest line, first prompt and
first timestamp with the time-zone conversion, rejected candidates with reasons, still running
or not. Environment items labelled historical evidence, current observation, unverified
snapshot or unknown; a current install never proves a historical version. Record meanings with
a supporting line each; unresolved information listed.

## Statuses and findings

Each examined dimension has one status and the range examined:

- `OBSERVED`: findings follow, each with observation, `path:line`, a quote of at most 200
  characters with secrets replaced, turns and confidence.
- `NOT_OBSERVED_IN_SCOPE`: the authorized evidence was available, searched in the stated range,
  and showed no instance.
- `UNKNOWN`: history, fields or semantics are missing or ambiguous. Zero is valid only when a
  record establishes zero.

A conclusion carries two confidences: in what happened, and in why. A cause is `CONFIRMED` only
when cited evidence rules out the material alternatives; otherwise it stays a candidate
explanation or `UNKNOWN`. Involvement of a skill, hook, plugin or tool is `not indicated`,
`possible` or `likely`, with lines; it is never a defect diagnosis or a proposed change.

## Derived numbers

Usage totals state their semantics (per response or cumulative), count each response once, and
mark records without usage, which make the total a lower bound. Durations come from recorded
timestamps; a gap's cause is stated only when records show it. Every derived figure shows its
inputs. No prices or rates the source does not record.

## Export

Copies only; originals unchanged. Placeholders are stable across files and numbered by first
appearance; the scrub log holds placeholder, category and count, never an original value or a
replacement map. Line alignment preserved. Two separate outcomes: privacy (`CLEAN` or the
unresolved misses) and evidence support (supported, or limited with the affected findings).
No archive, upload, issue or message without the user's approval of the exact content.

## Similar sessions and issue lookup

Opt-in only. Markers come from confirmed findings; each is hit, miss or unknown per candidate,
with citations. Issue lookup searches the repository that owns the involved skill; drafting
creates a local file only.
