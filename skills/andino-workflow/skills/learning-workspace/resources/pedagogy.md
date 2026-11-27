# How people learn

The teaching choices behind the workspace steps in [the skill](../SKILL.md). Operates under
Andino Workflow governance. Use it to choose the next lesson, design practice and review, judge
evidence, and handle questions that need practitioners or professionals.

## Knowledge, skills and wisdom

To learn something deeply a learner needs three things, in different amounts per topic:

- **Knowledge**: facts and concepts, taken from high-trust sources. Your memory is a lead to
  check, not a source; until `RESOURCES.md` covers the mission, finding good sources is the
  first job.
- **Skills**: the ability to use that knowledge, built through practice you design with feedback.
  Reading a query plan, holding a pose, writing a retry handler.
- **Wisdom**: judgment that comes from real use and from other practitioners: when to break the
  rule, what matters in practice. You can offer a reasoned view, but it grows outside the lesson.

A theory-heavy topic leans on knowledge; a craft or physical skill leans on skills. Teach the
knowledge a skill needs, then practise the skill.

## Fluency is not storage

- **Fluency** is recalling something right after seeing it. It feels like mastery and fades.
- **Storage** is recalling it days later, in a new situation. That is the goal.

Build storage with desirable difficulty in practice:

- **Retrieval**: the learner produces the answer from memory (a question before showing the
  answer, "explain it in your own words", predict the result) instead of re-reading.
- **Spacing**: earlier material comes back after a gap. Each lesson from the second on carries
  one or two questions on earlier lessons.
- **Interleaving**: practice mixes related kinds of problems (an index question next to a
  statistics question) so the learner must first decide which idea applies. Use it for skills
  practice, not for a first explanation.

Difficulty works in opposite directions in the two halves of a lesson. While new knowledge comes
in, it eats the working memory needed to understand: keep explanations plain, concrete and
short. In practice, effortful recall is what makes it stick: make the learner work for the
answer.

## Choosing the next lesson

The next lesson sits just past what the learner can already do: challenging, but reachable with
what they have. Find it from the files, not from a syllabus:

1. Read `MISSION.md`: which Success bullet is next, or closest to reach?
2. Read the learning records: what is demonstrated, what was stated as prior knowledge, which
   misconceptions were corrected, which quiz items were missed.
3. Pick the smallest step toward that Success bullet that builds on demonstrated knowledge and
   gives one tangible win. A missed item or open misconception comes before new ground.
4. If the learner asked for something specific, teach it, and connect it to the mission in one
   sentence.

Signs the step is wrong: the learner breezes through (too small; skip ahead next time) or cannot
start the practice (too big; split it and teach the missing piece first).

## Feedback loops

Every practice needs feedback, as soon and as automatic as possible:

- **Knowledge checks**: in-page quiz with immediate right or wrong and a one-line reason.
- **Applying to their material**: a task on their own query, code or routine, answered in the
  chat; your feedback names what is right, what is missing and the corrected version.
- **Procedures and physical skills**: a checklist of steps with what they should notice, how to
  tell they did it right, and when to stop; the learner reports back and you adjust.

## What counts as evidence

| Counts | Does not count |
| --- | --- |
| The learner explains the idea in their own words, correctly | They read the lesson |
| They apply it to a new case, their own or one you give | They scored well right after the lesson |
| They spot and fix an error | They said "makes sense" |
| They state prior experience, with its depth (record it as stated) | You covered it |

A quiz score is a hint about where to look, not a record. A missed item is a gap to work on next.

## Misconceptions

A wrong belief predicts more mistakes than a gap. Name it plainly, show why it is wrong with a
source, give the correct version, and record it. When acting on it could cause harm (deleting
production data, an unsafe movement, a financial loss), correct it at the start of the reply,
before anything else, with a safe alternative.

## Questions that need wisdom

Some questions have no textbook answer: "how do experienced people decide…", "is this normal at
my level?". Answer them, because a reasoned view helps, but mark it as judgment, give the
learner a way to test it on their own case, and point them to where practitioners can test it
with them:

- choose places with a reputation for quality and moderation: the project's own forum or mailing
  list, a well-moderated Q&A site for the field, a respected subreddit, a local class or meetup;
- name one or two concrete places, with what each is good for, and add the chosen ones to
  `RESOURCES.md` under Wisdom;
- this is a suggestion only: never create accounts, post or sign the learner up;
- when this learner has said they do not want communities, respect it and only mention that the
  option exists if they ask again.

## Health, safety, legal and money topics

- Establish the limits a professional set (what is allowed, what to avoid, warning signs) before
  any material, and record them in `MISSION.md` under Constraints.
- Never give a procedure from memory: no exercise sequences for an injury, no doses, no legal
  steps. Material comes from authoritative sources (clinical guidelines, national health
  services, official regulators), stays within the professional's limits, and tells the learner
  to confirm it with that professional.
- Name the warning signs that mean stop and get help, with their source.
- When the learner pushes for "just give me the routine", explain in one or two sentences why the
  limits come first and offer what you can do now (questions to ask the professional, the
  principles behind safe practice).
