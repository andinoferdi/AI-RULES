# Teach so the learner can do something new, and keep what they learned

Internal method ID: `andino-learning-workspace` (alias: `learning-workspace`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: proportional investigation, evidence-based
> decisions, one durable checkpoint and clean handoff. Do not invoke the workflow
> recursively. Loading this resource changes neither tools nor permissions.

## Purpose

Help one person get able to do something they could not do before, and keep that progress
where the next session can find it. Reading about a topic produces the feeling of knowing it;
recalling it, using it on their own material and getting feedback produces the ability. A quick
question gets a short lesson in the conversation and no files. A goal that spans sessions gets a
learning workspace: a mission, trusted sources, short lessons with practice and feedback,
reference sheets, and records of what the learner has shown they can do. Every lesson is tied to
why the learner is learning, built from sources rather than memory, and sized to their next step.

## Trigger and non-trigger

Use when:

- the user asks to be taught, to learn, or for a lesson on a concept, process, tool or skill
  ("teach me X", "ajarin aku X");
- the user wants to learn over several sessions or names a folder for learning materials;
- the current folder holds a learning workspace (`MISSION.md` with `lessons/` or
  `learning-records/`) and the user continues;
- the user says an explanation in this conversation did not land.

Do not select for:

- A factual question with a short answer ("what is PostgreSQL's default port?"): answer it in the
  first sentence and stop.
- Documentation, onboarding guides or runbooks for other people: `documentation-and-adrs` or
  `human-procedure`.
- Reminders, schedules, accounts, subscriptions or course purchases: never from this skill.

## Choose the route first

Pick the route from the request and the folder before writing anything.

| The user | Route | Files |
| --- | --- | --- |
| Asks a factual question | Direct answer | None |
| Wants to understand something now ("explain", "teach me quickly") | [Quick lesson](#quick-lesson-in-the-conversation) | None |
| Says the last explanation did not land | [Repair](#repair-an-explanation-that-did-not-land) | None |
| Wants to learn over sessions, names a folder, or continues a workspace | [Workspace](#workspace-procedure) | Only in the learning folder |
| Asks to scaffold or renumber course exercises | [course exercises](resources/course-exercises/guide.md) | In the course repository |

No file is written outside the workspace route. When a quick lesson turns into a goal that
spans sessions, offer the workspace in one line and create it only after the user says yes.

## Select a resource, not a second lifecycle

Load only the resource the current step names. It runs inside this procedure and current
authority; it starts no second plan.

| Current need | Resource | Skip when |
| :--- | :--- | :--- |
| Writing or updating `MISSION.md`, `RESOURCES.md`, `NOTES.md`, `GLOSSARY.md` or a learning record | [workspace formats](resources/workspace-formats.md) | Quick lesson or repair |
| Writing a lesson page, a reference sheet, the shared stylesheet or quiz component, or a Markdown lesson | [lessons and assets](resources/lesson-and-assets.md) | No lesson or reference sheet this turn |
| Choosing the next lesson, designing practice and review, judging evidence, answering a question that needs practitioner judgment, health and safety topics | [how people learn](resources/pedagogy.md) | The next lesson and its practice are already fixed |
| Scaffolding numbered course exercises in a course repository | [course exercises](resources/course-exercises/guide.md) | Teaching the learner directly |
| One workspace session end to end | [worked example](resources/worked-example.md) | The steps are already clear |

## Prerequisites

- Read the user's request in full and list the current folder. When it holds `MISSION.md`, read
  `MISSION.md`, `NOTES.md`, `RESOURCES.md`, `GLOSSARY.md`, every learning record and the lesson
  list before replying, and do not ask for anything they already answer.
- Treat each learner and each workspace as separate. Preferences, opt-outs and prior knowledge
  come only from this user's own workspace and conversation, never from another folder or
  conversation you have seen.
- Know whether you can search and fetch the web in this session. A workspace lesson needs
  sources; without web access, say which claims you could not check.

## Quick lesson in the conversation

1. **Explain with their case.** Say what the thing is, how it works in the user's own situation
   (their endpoint, their query, their example), one concrete worked example, and the mistake
   people usually make. Assume a sensible starting level, say it in one line, and invite
   correction. Cite the official source for exact rules (status codes, limits, standards) when
   you can check them; mark the rest as your own suggestion. Keep it to what one sitting can
   hold: about 150 words when the user asks for it short, about 250 otherwise. Edge cases and
   extra rules wait for the follow-up. Done when the explanation uses the user's example and
   stays within that length.
2. **Make them retrieve it.** End with one short question or task the user answers from memory
   or applies to their case, and do not answer it in the same message. Say that you will give
   feedback. Done when the message ends on that question.
3. **Give feedback.** When the user answers, say what is right, what is missing and the correct
   version, then one follow-up only if it builds on the gap. If they want to keep going over
   several sessions, offer the workspace in one line. Done when the gap they showed is closed or
   named.

## Repair an explanation that did not land

1. **Start from what it means for them.** First sentence: what the idea lets them do or decide
   in practice. Then the context the earlier explanation skipped, exactly one concrete example
   from their world (a second example or a worked calculation brings back the overload), and
   what to do with it. Keep the technical meaning and any uncertainty unchanged; drop jargon that
   the example made unnecessary. Stay around 150 words. When Focus is installed, its
   `references/explanation-repair.md` resource applies. Done when the reply leads with the
   practical meaning, has one example and stays around 150 words.
2. **Check it landed.** End with one question that makes them use the idea (compare two cases,
   predict a result), not "is it clear now?". Done when that question is the last line.

## Workspace procedure

Each step ends on a "Done when" line naming what must exist before the next step. Formats are in
[workspace formats](resources/workspace-formats.md); lesson and asset contracts in
[lessons and assets](resources/lesson-and-assets.md).

1. **Find the workspace.** Use the folder the user named, or the current folder when it already
   holds `MISSION.md`. Otherwise propose one path and ask once before creating anything. Never
   write into the skill's own installation folder. Done when you know the folder, and have read
   every workspace file in it or confirmed it is empty.

2. **Establish the mission before any material.** When `MISSION.md` is missing or vague, ask one
   open question about why they are learning this: what they want to be able to do and where
   (their job, a project, a race), with your guess and its reason. Write no lesson, curriculum or
   skeleton yet. Ask follow-ups one turn at a time, and only for what their answer left unknown:
   observable success, constraints (time per day, deadline, language, budget), prior knowledge
   and what is out of scope. For health, safety-critical, legal or financial topics, also ask what
   limits a professional (doctor, physiotherapist, lawyer) has set; say that you will not hand
   over a procedure (poses, doses, moves) from your own knowledge, and that later material will
   come from trusted sources within those limits and should be confirmed with that professional.
   Then write `MISSION.md` in the user's own words. Done when `MISSION.md` holds a concrete Why,
   observable Success bullets, Constraints and Out of scope, or your one question is sent.

3. **Ground the topic in sources.** Before the first lesson, find high-trust sources for what
   the mission needs: official documentation, standards, textbooks, recognised experts,
   clinical guidelines for health. Search and fetch when the host allows it, and open each page
   you cite. Write `RESOURCES.md` with every entry annotated (what it covers, when to use it),
   Knowledge apart from Wisdom (communities), a Gaps section, and the community opt-out when this
   user gave one. Do not teach a precise claim, number or procedure you could not source; mark
   it unverified in the lesson. Done when `RESOURCES.md` lists at least two opened high-trust
   sources (the main reference and one for the next steps of the mission), each lesson claim area
   has a source there, and every entry has its annotation.

4. **Record the starting point.** Write one learning record for the prior knowledge the user
   stated, with its depth ("can write `CREATE INDEX`; has never read a plan"), and put their
   preferences in `NOTES.md` (language, minutes per session, lesson length, community opt-out).
   Nothing from a lesson they have not done yet is recorded. Done when the record and `NOTES.md`
   exist and contain only what the user said.

5. **Choose the next lesson.** Take the smallest step that gives one tangible win toward a
   Success bullet, building on what the records show and not re-teaching recorded prior
   knowledge. A misconception goes first, and one that could cause harm (data loss, injury,
   money) is corrected in the reply itself before anything else, with the safe alternative and
   its source. A missed quiz item becomes the next practice target. Use
   [how people learn](resources/pedagogy.md) when the choice is not obvious. Done when you can
   state the lesson's win in one sentence that names a Success bullet.

6. **Build the lesson and its reference sheet.** One HTML file `lessons/NNNN-slug.html` that:
   - opens with the win and works on the learner's own material (their query, code, routine);
   - teaches only the knowledge the practice needs, each claim with its source next to it;
   - has practice with immediate feedback (a quiz or task in the page using the shared
     component), options of nearly equal length and the correct position varied;
   - from the second lesson on, has one or two retrieval questions on earlier lessons, mixed with
     the new ones;
   - names one primary source to read or watch next, reminds the learner to bring questions back
     to you, and links the previous lesson, the next one when it exists and the reference sheet.

   Link the shared `assets/lesson.css` and `assets/quiz.js`; create them from the starters in
   [lessons and assets](resources/lesson-and-assets.md) when they are missing, reuse them when
   they exist, and never inline what the next lesson would copy. Create or extend a short,
   printable reference sheet in `reference/` with the lesson's compressed essence. Size the
   lesson to the session time in `NOTES.md`. Done when the lesson and reference sheet exist,
   every relative link points to a file that exists, and the lesson checklist in
   [lessons and assets](resources/lesson-and-assets.md) passes.

7. **Hand over.** Tell the user, in about 120 words, which files you created or changed (one
   short line per file or group), where the lesson is, and the first thing to do: open the
   lesson (open it for them only when the host allows opening files), then answer one retrieval
   question in the chat. Leave out caveats the lesson already marks; keep only a safety warning.
   Done when the message names the files, the lesson path and that first step within that
   length.

## Continuing a workspace

- **Evidence.** When the user answers, explains or practises, give feedback first. Write a
  learning record only for demonstrated understanding (they explained or applied it correctly
  in their own words), stated prior knowledge, a corrected misconception, or a mission shift. A
  quiz score alone, or a lesson merely completed, is not a record: treat a missed item as a gap.
  Number records in sequence; mark an outdated record `Status: superseded by NNNN` instead of
  rewriting or deleting it. Add a term to `GLOSSARY.md` only after the user has used it
  correctly, and use the glossary's terms in every later lesson.
- **Misconceptions.** Correct a wrong belief plainly with its source, give the safe alternative
  when acting on the belief could cause harm, and record the corrected misconception as a
  learning record with the evidence.
- **Mission changes.** When the goal moves (new technology, deadline, job), ask how the mission
  should change, with two or three concrete options and your recommendation. Edit `MISSION.md`
  and add a record only after the user confirms. Earlier records stay.
- **Questions that need practitioner judgment** ("how do seniors decide…"): answer with your
  reasoning, marked as judgment, and a way to test it on their own case. Then suggest one or two
  concrete, well-moderated places where practitioners discuss this (a named forum, mailing list,
  Q&A site or local group) as a suggestion only, unless this user's `NOTES.md` or `RESOURCES.md`
  records an opt-out. Never create accounts, post or sign up for them.

## Rules for every route

- Files only on the workspace route, only inside the learning folder: never in the skill's
  installation folder, never a schedule, reminder, account, commit or purchase.
- Sources before claims on the workspace route; your memory is a starting point to check, not a
  source. Name what you could not verify.
- Covered is not learned. Only evidence the learner produced goes into a record.
- Quiz options differ by at most two words in length, the correct option's position varies
  across questions, and nothing in wording, order or formatting gives the answer away.
- One learner, one workspace: never carry preferences or opt-outs across users or folders.
- Write in the learner's language and register; keep technical terms as the field uses them.
  In messages, describe what you did in plain words ("I noted that we still need a source for
  this") instead of the workspace's labels (Gaps, learning record, Success bullet, route).

## Shortcuts that cost the learner

| Shortcut | What to do instead |
| --- | --- |
| "They said 'teach me', so I'll set up a workspace." | A quick request stays in the chat. Offer the workspace in one line. |
| "I'll ask everything I need in one go." | While the why is unknown, ask one open question with your guess. |
| "I know this topic well enough." | Workspace lessons cite sources you opened. Mark anything unchecked. |
| "A full curriculum shows I understood the goal." | One short lesson with one win. The next one comes from the evidence. |
| "Inline styles are quicker for one lesson." | Shared `assets/` from the first lesson; the second one reuses them. |
| "The lesson covers it, so no reference sheet." | Learners return to reference sheets, not lessons. Write one per lesson. |
| "4 out of 5, so they've got it." | Record evidence, not scores. The missed item is the next target. |
| "They opted out of communities last time." | Only this user's own workspace says so. Check `NOTES.md` and `RESOURCES.md`. |
| "The goal changed, I'll update MISSION.md." | Ask first, with options. Edit after the user confirms. |
| "Their doctor allowed light exercise, so here's a routine." | No procedure from memory on health topics. Limits first, sources second. |

## Red flags

- A file in the folder after a quick question, a factual question or a repair.
- A quick lesson the user asked to keep short that runs past about 150 words, or a repair with
  more than one example.
- A first `RESOURCES.md` with a single source, or a message to the learner that uses the
  workspace's own labels ("added to Gaps", "a learning record") instead of plain words.
- Several questions in the first workspace reply while the why is still unknown.
- A lesson with no citation, no practice, no primary source or no link to the reference sheet.
- The correct quiz option is the longest one, or always in the same position.
- A learning record for a lesson the learner has not done, or for a quiz score alone.
- An earlier record rewritten or deleted.
- `MISSION.md` edited before the user confirmed the change.
- An opt-out or preference that came from a different user's workspace.
- A pose, dose or move sequence for a medical condition written from memory.

## Ownership and permission boundary

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its procedure, resources and checks; coordinator brevity never shortens the
lessons, records or checks it requires. It grants no authority to install tools, open
accounts, post in communities, schedule reminders, commit or publish. Web research follows the
host's permissions and Search First when that skill is installed. Learning materials belong to
the user: preserve their edits, and never delete their lessons or records.

## Output

| Route | Output |
| --- | --- |
| Direct answer | The answer in the first sentence. |
| Quick lesson | Explanation with their example and one retrieval question; feedback when they answer. |
| Repair | Practical meaning first, the missing context, one example, one check question. |
| Workspace, first session | The mission question; after the answer, `MISSION.md`, `RESOURCES.md`, `NOTES.md`, a starting-point record, `assets/`, the first lesson, a reference sheet and a short hand-over message. |
| Workspace, later session | Feedback, any safety correction first, records for new evidence, the next lesson with review questions, and the hand-over message. |

## Verification

Before you send the reply:

- [ ] the route matches the request, and no file exists outside the workspace route;
- [ ] on a new workspace, the why was asked as one open question before any material;
- [ ] `MISSION.md` holds Why, Success, Constraints and Out of scope in the user's words;
- [ ] every lesson claim has a source the lesson links, and unchecked claims are marked;
- [ ] the lesson has the win, practice with immediate feedback, review questions from the second
  lesson on, a primary source, the ask-me-back reminder and links that resolve;
- [ ] quiz options are of nearly equal length and the correct positions vary;
- [ ] a reference sheet exists for the lesson and the lesson links it;
- [ ] records hold only evidence the learner produced, and no earlier record was rewritten;
- [ ] preferences and opt-outs come from this user's own files and words;
- [ ] a harmful misconception was corrected first, with a safe alternative and its source.

## Worked example and anti-pattern

The [worked example](resources/worked-example.md) follows one learner from "use this folder to
learn about safe retries" through the mission question, the first lesson with its reference
sheet, an answer that shows a misconception, and the record it leaves.

Anti-pattern: "teach me idempotency keys quickly" answered with a new folder, a six-week
curriculum, a glossary of terms the user has never used, and a quiz whose right answers are
always the longest option.

## Fallback

- **No web access.** Teach from what you know, mark the lesson's claims as unverified, list the
  sources the learner should check in `RESOURCES.md` under Gaps, and say so in the hand-over.
- **No browser, or the user prefers plain text.** Write the lesson as Markdown
  (`lessons/NNNN-slug.md`) with the questions first and the answer key in a separate section at
  the end, as described in [lessons and assets](resources/lesson-and-assets.md).
- **The user will not say why.** Make a reasonable guess, write it in `MISSION.md` marked as your
  guess, keep the first lesson small, and ask again after it.

## Local resources

- [Workspace formats](resources/workspace-formats.md): mission, resources, notes, records,
  glossary and folder layout.
- [Lessons and assets](resources/lesson-and-assets.md): lesson contract, starter stylesheet and
  quiz component, reference sheets, quiz rules, Markdown fallback.
- [How people learn](resources/pedagogy.md): knowledge, skills and wisdom, retrieval and
  spacing, choosing the next lesson, evidence, communities, health topics.
- [Course exercises](resources/course-exercises/guide.md): numbered exercise scaffolding.
- [Worked example](resources/worked-example.md): one workspace session end to end.
- MIT notices: [references/license.md](references/license.md).

## Learning mode example

This standard-library example classifies intent only. The quick branch stays in chat; the
structured branch is selected only for an explicit persistent goal; explanation repair remains
separate.

```python evolution-example
import json

def choose_mode(request):
    if request["last_explanation_unclear"]:
        return {"mode": "repair", "persistent_goal": False}
    if request["multi_session_goal"]:
        return {"mode": "structured", "persistent_goal": True}
    if request["explicit_learning_request"]:
        return {"mode": "quick", "persistent_goal": False}
    return {"mode": "direct-answer", "persistent_goal": False}

RESULT = {
    "ordinary": choose_mode({"last_explanation_unclear": False, "multi_session_goal": False, "explicit_learning_request": False}),
    "teach_now": choose_mode({"last_explanation_unclear": False, "multi_session_goal": False, "explicit_learning_request": True}),
    "deliberate": choose_mode({"last_explanation_unclear": False, "multi_session_goal": True, "explicit_learning_request": True}),
    "confused": choose_mode({"last_explanation_unclear": True, "multi_session_goal": False, "explicit_learning_request": True}),
}
print(json.dumps(RESULT, sort_keys=True))
```

Expected result:

```json
{"confused": {"mode": "repair", "persistent_goal": false}, "deliberate": {"mode": "structured", "persistent_goal": true}, "ordinary": {"mode": "direct-answer", "persistent_goal": false}, "teach_now": {"mode": "quick", "persistent_goal": false}}
```

This example demonstrates route selection; it creates no workspace or learning record.

## Provenance

Adapted from Matt Pocock's `teach` (mattpocock/skills, `skills/productivity/teach`, commit
ad5400b) and its four format files, under the MIT license; notices are in
[references/license.md](references/license.md). From `teach`: the mission, resources,
learning-record and glossary formats, knowledge, skills and wisdom, fluency against storage
strength, retrieval, spacing and interleaving, short HTML lessons with shared components,
reference documents, quiz rules and community routing. Andino's own: the route table with the
quick lesson and repair, sources before claims with named gaps, health and safety limits, per-user
isolation, no schedules or accounts, the Markdown fallback and course exercises. The comparison
trial is recorded in the AI-RULES repository at `docs/validation/learning-workspace/trial.md`.
Upstream bootstrap, hooks, installers and automatic commits are not imported.
