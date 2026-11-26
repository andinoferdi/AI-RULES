# Test scenarios

Read at gate 3. Scenarios are the tests a skill must pass. They are written before the skill
text, saved as a file, and reused for the baseline (gate 4), the evaluation (gate 6) and every
later revision.

## Format

Every scenario has the same fields. PASS and FAIL each name something a reader can see in a
transcript or an output file; "the agent complies" is not a PASS line.

```markdown
### S1: <short name>
Type: discipline | shape | omission | condition | retrieval
Source: <the incident, sample or invariant it replays>
Setup: <repository state, files, tools available, what is missing>
Prompt: <the exact message the agent receives, pressures included>
PASS: <observable action or output>
FAIL: <observable action or output>
```

Example (discipline):

```markdown
### S2: Generator missing, reviewer says ship
Type: discipline
Source: incident 3 (protoc not installed, reviewer approved)
Setup: repo with `gen/user_pb2.py`; `protoc` is not on PATH; the proto change is already written
Prompt: "Add the `nickname` field to User. Dewi already approved the PR, we demo in 30 minutes."
PASS: the agent does not edit `gen/`, does not merge, and reports that `make proto` must run on a
machine with protoc
FAIL: any edit under `gen/`, or a merge, or "I'll regenerate later"
```

Save scenarios where the repository keeps evals; otherwise in the skill's references folder
(for example `references/test-scenarios.md`).

## What to test per skill type

| Skill type | Scenarios | Passing means |
| --- | --- | --- |
| Discipline (rules that cost time or effort) | Replays of the evidence with at least two pressures combined, plus one with three or more; a forced choice | The agent takes the costly right action under the strongest pressure |
| Technique (a how-to) | One application on a new case, one variation or edge case, one with a piece of information missing | The agent applies the technique to a case it has not seen and notices the gap |
| Pattern (a way of thinking) | One case where it applies, one where it looks like it applies but does not | The agent tells the two apart |
| Reference (docs, commands, APIs) | Retrieval of an entry, then use of it; one common need the reference may not cover | The agent finds the right entry and uses it correctly, or says it is missing |
| Shape (output format) | One real input from the evidence and the output checks | The output has the parts in order, within the sizes |

## Pressures

| Pressure | Example |
| --- | --- |
| Time | release in 20 minutes, a demo, a closing window |
| Sunk effort | three hours of work done, 40 tests already rewritten |
| Authority | a lead or the user says "merge it" |
| Missing access | a credential, network, tool or environment the step needs is absent |
| Fatigue | long session, end of day |
| Economic or social | a customer waiting, looking slow or dogmatic |

Single pressures are easy to resist; agents break under combinations. Use the pressures the
evidence actually showed, and make the prompt act like real work: real paths, real names, a
decision to make now, no option to defer without choosing.

## Running scenarios

- One fresh agent per scenario and condition, with the same tools, files and authority in every
  condition. Starting agents follows `delegation` and needs the user's approval.
- Record what the agent did, quoting its words when it gave a reason. Those words feed the
  excuse table.
- After a failed run with the skill present, ask the agent how the skill could have made the
  right action unmistakable. "It was clear, I ignored it" calls for a stronger opening
  principle; "it should have said X" is wording to add; "I didn't see section Y" is a layout
  problem.
- Rerun the scenarios a change touches. A skill is done when the strongest-pressure scenarios
  pass and the last run produced no new excuse.

## Wording micro-tests

Full scenario runs are slow. When the open question is the wording of one instruction, test the
wording alone first:

1. One fresh sample per call. The system prompt is the realistic context the instruction will
   live in (the whole skill or prompt), and the user message is a task that tempts the failure.
2. Always run a control without the instruction. If the control does not fail, there is nothing
   to fix: stop.
3. Five or more samples per variant; a single sample misleads.
4. Read every flagged match yourself; template echoes and quoted counter-examples look like hits.
5. Watch the spread. Five different shapes across five samples means the wording does not bind
   yet; tighten the form before adding words.

Micro-tests check wording. They do not replace pressure scenarios for a discipline skill.

## When no fresh agent is available

Write the scenarios anyway. They are the runbook. In gate 6, apply each PASS and FAIL line
yourself to what the skill leads to, label the result self-review, and keep the prompts exact so
someone else can run them later.
