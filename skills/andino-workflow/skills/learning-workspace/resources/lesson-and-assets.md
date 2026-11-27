# Lessons and assets

The lesson page, the shared components and the reference sheet for a learning workspace.
Operates under Andino Workflow governance; when to build them is in [the skill](../SKILL.md).
Paths are relative to the learner's workspace.

## The lesson page

A lesson is one self-contained HTML file in `lessons/`, named `NNNN-slug.html`, that teaches one
tightly scoped thing in the time the learner has (`NOTES.md`; 10 to 20 minutes when unknown).
Learners keep coming back to their lessons, so they should read well: one column, generous line
height, real headings, code in a monospace block, nothing that moves.

Sections, in this order:

1. **The win.** One or two sentences: what the learner can do after this lesson, on their own
   material ("name the node that makes your `orders` query slow, and say why").
2. **What you need to know.** Only the knowledge the practice needs, built on the learner's own
   example. Each claim carries its source next to it: `<span class="source">(<a href="…">source
   name</a>)</span>`. Keep it short; new knowledge is easier to take in without extra difficulty.
3. **Practice.** A quiz or task in the page with immediate feedback, using `assets/quiz.js`; for a
   physical or real-world skill, a short checklist of steps with what to notice and when to stop.
   Make the learner produce: predict, choose, explain, apply.
4. **Review.** From the second lesson on, one or two questions on earlier lessons mixed with the
   new ones, so earlier material is recalled after a gap.
5. **Read next.** One primary source: the best, most trusted page or video you found for this
   step.
6. **Ask me.** A line reminding the learner to bring questions and their answers back to you in
   the chat.
7. **Links.** Previous lesson, next lesson when it exists, and the reference sheet.

```html
<!doctype html>
<html lang="{language code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>0001 {Lesson title}</title>
<link rel="stylesheet" href="../assets/lesson.css">
</head>
<body>
<p class="win"><strong>After this lesson:</strong> {the win}</p>
<h1>{Lesson title}</h1>
<section>
  <h2>{What you need to know}</h2>
  <p>{claim built on the learner's example} <span class="source">(<a href="{url}">{source}</a>)</span></p>
</section>
<section class="quiz">
  <h2>{Practice}</h2>
  <fieldset data-answer="b" data-why="{one-line reason shown on a correct answer}">
    <legend>1. {question}</legend>
    <label><input type="radio" name="q1" value="a"> {option}</label>
    <label><input type="radio" name="q1" value="b"> {option}</label>
    <label><input type="radio" name="q1" value="c"> {option}</label>
    <p class="feedback" aria-live="polite"></p>
  </fieldset>
</section>
<p class="next"><strong>Read next:</strong> <a href="{url}">{primary source}</a></p>
<p class="ask">Something unclear? Bring your question or your answers back to the chat.</p>
<nav><a href="0000-previous.html">Previous</a> · <a href="../reference/{topic}.html">Reference sheet</a></nav>
<script src="../assets/quiz.js"></script>
</body>
</html>
```

## Shared components

Components live in `assets/` and every lesson links them, so the lessons read as one course and
the second lesson costs less than the first. Before writing a lesson, list `assets/` and build
from what is there. When a lesson needs something a later lesson could reuse (a diagram helper,
a small simulator), write it as a component in `assets/` and link it. Write these two starters
when the workspace has none:

`assets/lesson.css`

```css
:root { --ink: #1f2328; --muted: #59636e; --accent: #0b5cad; --ok: #1a7f37; --bad: #cf222e;
        --line: #d0d7de; --bg: #fffdf8; --code: #f6f8fa; }
body { max-width: 42rem; margin: 2.5rem auto; padding: 0 1rem; color: var(--ink);
       background: var(--bg); font: 18px/1.65 Georgia, "Times New Roman", serif; }
h1, h2, legend { font-family: system-ui, sans-serif; line-height: 1.25; }
h1 { font-size: 1.6rem; } h2 { font-size: 1.2rem; margin-top: 2rem; }
code, pre { font: 14px/1.45 ui-monospace, Consolas, monospace; }
pre { background: var(--code); padding: .75rem 1rem; overflow-x: auto; }
a { color: var(--accent); }
.win { border-left: 3px solid var(--accent); padding-left: .75rem; }
.source { color: var(--muted); font-size: .85em; }
.quiz fieldset { border: 1px solid var(--line); margin: 1rem 0; padding: .75rem 1rem; }
.quiz label { display: block; margin: .25rem 0; cursor: pointer; }
.feedback.ok { color: var(--ok); } .feedback.bad { color: var(--bad); }
nav { margin-top: 2.5rem; font-family: system-ui, sans-serif; }
@media print { body { background: #fff; margin: 0; } nav, .quiz label input { display: none; } }
```

`assets/quiz.js`

```js
// Each question: <fieldset data-answer="b" data-why="..."> with radio inputs valued a, b, c...
// and an empty <p class="feedback">. Feedback appears as soon as an option is chosen.
document.querySelectorAll('.quiz fieldset').forEach(function (set) {
  set.addEventListener('change', function (event) {
    var feedback = set.querySelector('.feedback');
    var correct = event.target.value === set.dataset.answer;
    feedback.className = 'feedback ' + (correct ? 'ok' : 'bad');
    feedback.textContent = correct
      ? 'Correct. ' + (set.dataset.why || '')
      : 'Not yet. Look at the example again and try another option.';
  });
});
```

Translate the two feedback strings into the learner's language. Keep everything local: no
fonts, scripts or styles from the network, so the lessons open offline and print cleanly.

## Quiz rules

- Every option in a question has nearly the same length: at most two words apart.
- The correct option's position changes across questions; do not let it settle on one letter.
- Nothing in wording, order or formatting points to the answer: no "all of the above", no
  absolute words only on the wrong options, no option that repeats the question's phrasing.
- Wrong options are real mistakes learners make, so choosing one teaches something; the feedback
  says why.
- Check before saving: list each question's correct letter and option lengths.

## The reference sheet

Lessons are done once; reference sheets are what the learner comes back to. Each lesson creates
or extends one sheet in `reference/{topic}.html` with the lesson's compressed essence: syntax,
the steps of a procedure, a decision table, a pose sequence with its cautions, a glossary
excerpt. It links `../assets/lesson.css`, fits on one or two printed pages, cites its sources
and links back to the lessons that taught each part.

```html
<!doctype html>
<html lang="{language code}">
<head><meta charset="utf-8"><title>{Topic} reference</title><link rel="stylesheet" href="../assets/lesson.css"></head>
<body>
<h1>{Topic} reference</h1>
<ul>
  <li><code>{item}</code>: {one-line meaning} (<a href="../lessons/0001-{slug}.html">lesson 1</a>)</li>
</ul>
<p class="source">Sources: <a href="{url}">{source}</a></p>
</body>
</html>
```

## Lesson checklist

Before handing a lesson over, check:

- [ ] one tightly scoped topic, sized to the learner's session time;
- [ ] the win is stated first and uses the learner's own material;
- [ ] every claim has its source next to it, or is marked unverified;
- [ ] practice with immediate feedback; quiz rules hold;
- [ ] review questions on earlier lessons (second lesson onward);
- [ ] one primary source, the ask-me reminder, and links to the previous lesson and reference sheet;
- [ ] `assets/lesson.css` and `assets/quiz.js` are linked, not copied inline;
- [ ] every relative link points to a file that exists in the workspace;
- [ ] written in the learner's language, with the field's technical terms.

## Markdown fallback

When there is no browser or the learner prefers plain text, write `lessons/NNNN-slug.md` with the
same sections. Put the questions in the Practice section and the answer key, with the reason for
each answer, under a final `## Answers` heading, so the learner can try before looking. The
reference sheet becomes `reference/{topic}.md`.
