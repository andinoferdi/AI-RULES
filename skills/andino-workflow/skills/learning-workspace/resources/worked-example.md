# Worked example: one learner, two sessions

Operates under Andino Workflow governance. This follows [the skill](../SKILL.md) for a learner
who wants to understand safe retries for a payments service. The conversation is condensed; the
files are the ones the steps produce. A runnable version of the files closes the page.

## Session 1: the mission first

> **Learner:** Use this folder, I want to learn safe retries over the next couple of weeks.

The folder is empty, so this is a new workspace (step 1). The why is unknown, so the reply is one
open question with a guess, and nothing is written yet (step 2):

> Happy to use this folder. Before I write anything: what do you want to be able to do once you
> know this? My guess is that something at work retries requests and you have seen, or fear,
> duplicates. Is that it?

> **Learner:** Yes. Our mobile app retries `POST /payments` on timeout and we had two double
> charges last month. I want to diagnose why and explain to the team how duplicates should be
> handled. I know timeouts and HTTP status codes well. 15 minutes a day. Distributed consensus is
> not for now.

Now the files (steps 2 to 6):

- `MISSION.md`: Why "diagnose safe retries for `POST /payments` after two double charges";
  Success "explain duplicate handling to the team", "say which requests are safe to retry and
  why"; Constraints "15 minutes a day"; Out of scope "distributed consensus".
- `RESOURCES.md`: RFC 9110 section 9.2.2 (idempotent methods) and the Stripe guide to idempotent
  requests, both opened and annotated; Gaps: "how our gateway logs retries".
- `NOTES.md`: language, 15 minutes, no community preference stated yet.
- `learning-records/0001-prior-knowledge.md`: knows timeouts and status codes well (stated).
- `assets/lesson.css`, `assets/quiz.js` from the starters.
- `lessons/0001-retry-identity.html`: the win ("say whether a retried `POST /payments` can charge
  twice, and why"), the knowledge with sources beside each claim, three quiz questions with
  options of near-equal length and the correct answer in different positions, the primary source
  to read next, the ask-me line, the link to the reference sheet.
- `reference/retry-identity.html`: the safe-to-retry table and the idempotency-key flow.

The hand-over names the files and the first step: open the lesson, then answer in the chat
"a client times out after the server charged the card; what happens on retry without a key?".

## Session 2: evidence and a misconception

> **Learner:** Done, 3 out of 3. And retries are always safe as long as we wait long enough
> between them, right?

A perfect quiz score is not a record: the learner has only seen the lesson. The second sentence
is a misconception that leads to double charges, so the reply corrects it first, with the RFC as
source: waiting changes when the duplicate arrives, not whether it charges again; only a request
the server can recognise as a repeat is safe to retry. That correction becomes
`learning-records/0002-retry-safety-misconception.md` with the learner's words as evidence. The
next lesson will practise telling safe and unsafe retries apart, with one review question on
retry identity.

## Run the example

The block below writes the session-1 files plus the session-2 record into the current folder,
checks them the way the lesson checklist does, and writes `result.json`. It uses only Python's
standard library. Run it in an empty, disposable folder. The repository's
`scripts/check_andino_matt_methods.py` runs this exact block in a temporary folder and compares
the result and files with its own expected values.

```python
from pathlib import Path
import json
import re

files = {
    "MISSION.md": (
        "# Mission: Safe retries\n\n## Why\nWe had two double charges after the app retried "
        "POST /payments; I want to diagnose safe retries and stop them.\n\n## Success looks like\n"
        "- Explain duplicate handling to the team\n- Say which requests are safe to retry and why\n\n"
        "## Constraints\n- 15 minutes a day\n\n## Out of scope\n- Distributed consensus\n"),
    "RESOURCES.md": (
        "# Safe Retries Resources\n\n## Knowledge\n\n- RFC 9110, section 9.2.2 Idempotent Methods\n"
        "  Covers which HTTP methods are idempotent. Use for: what may be retried automatically.\n\n"
        "## Wisdom (communities)\n\n(No preference stated yet.)\n\n## Gaps\n\n- How our gateway logs retries\n"),
    "NOTES.md": "# Notes\n\n- Time: 15 minutes a day.\n",
    "assets/lesson.css": "body { max-width: 42rem; margin: 2.5rem auto; }\n",
    "assets/quiz.js": "// shared quiz component, see lessons and assets\n",
    "learning-records/0001-prior-knowledge.md": (
        "# Knows timeouts and HTTP status codes\n\nStated in session 1; do not re-teach them.\n\n"
        "**Evidence**: the learner's own statement.\n"),
    "learning-records/0002-retry-safety-misconception.md": (
        "# Corrected: waiting between retries does not make them safe\n\n"
        "The learner believed retries are safe with enough delay. Only a repeat the server can "
        "recognise is safe (RFC 9110, 9.2.2).\n\n**Evidence**: the learner's words in session 2.\n"),
    "reference/retry-identity.html": (
        "<!doctype html><title>Retry identity reference</title>"
        "<link rel=\"stylesheet\" href=\"../assets/lesson.css\">"
        "<h1>Retry identity</h1><p>Safe to retry: GET, PUT, DELETE. POST needs an idempotency key "
        "(<a href=\"../lessons/0001-retry-identity.html\">lesson 1</a>).</p>"),
}

quiz = [
    {"q": "A POST times out after the charge. What does a retry without a key do?",
     "options": ["Returns the first result", "Shows a timeout error", "Charges the card again"], "answer": 2},
    {"q": "Which method is idempotent by definition?",
     "options": ["PUT replacing a resource", "POST creating a payment", "PATCH adding a line"], "answer": 0},
    {"q": "What lets the server recognise a repeated POST?",
     "options": ["A longer client timeout", "The same idempotency key", "A smaller request body"], "answer": 1},
]
letters = "abc"
fieldsets = "".join(
    f"<fieldset data-answer=\"{letters[item['answer']]}\"><legend>{n}. {item['q']}</legend>"
    + "".join(f"<label><input type=\"radio\" name=\"q{n}\" value=\"{letters[i]}\"> {text}</label>"
              for i, text in enumerate(item["options"]))
    + "<p class=\"feedback\"></p></fieldset>"
    for n, item in enumerate(quiz, start=1))
files["lessons/0001-retry-identity.html"] = (
    "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>0001 Retry identity</title>"
    "<link rel=\"stylesheet\" href=\"../assets/lesson.css\"></head><body>"
    "<p class=\"win\">After this lesson: say whether a retried POST /payments can charge twice, and why.</p>"
    "<h1>Retry identity</h1><p>GET, PUT and DELETE are idempotent; POST is not "
    "<span class=\"source\">(RFC 9110, 9.2.2 in <a href=\"../RESOURCES.md\">resources</a>)</span>.</p>"
    f"<section class=\"quiz\">{fieldsets}</section>"
    "<p class=\"next\">Primary source: RFC 9110, section 9.2.2.</p>"
    "<p class=\"ask\">Bring your answers and questions back to the chat.</p>"
    "<nav><a href=\"../reference/retry-identity.html\">Reference sheet</a></nav>"
    "<script src=\"../assets/quiz.js\"></script></body></html>")

for relative, text in files.items():
    path = Path(relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def links_resolve(page):
    targets = re.findall(r'(?:href|src)="([^"#:]+)"', page.read_text(encoding="utf-8"))
    return all((page.parent / target).resolve().is_file() for target in targets)

records = [
    {"concept": "timeouts", "kind": "prior knowledge"},
    {"concept": "retry identity", "kind": "covered"},
    {"concept": "retry safety misconception", "kind": "misconception corrected"},
]
widths = [[len(option.split()) for option in item["options"]] for item in quiz]
result = {
    "files": sorted(p.as_posix() for p in Path(".").rglob("*")
                    if p.is_file() and p.suffix in (".md", ".html", ".css", ".js")),
    "recorded": [r["concept"] for r in records if r["kind"] != "covered"],
    "covered_not_learned": [r["concept"] for r in records if r["kind"] == "covered"],
    "quiz_positions": [item["answer"] for item in quiz],
    "quiz_options_within_two_words": all(max(w) - min(w) <= 2 for w in widths),
    "links_resolve": all(links_resolve(Path(p)) for p in files if p.endswith(".html")),
    "scheduled": False,
}
Path("result.json").write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
```

## What the run establishes

`result.json` lists the workspace files, records only the stated prior knowledge and the
corrected misconception (the covered lesson is not a record), shows the correct quiz answers in
three different positions with options at most two words apart, confirms every relative link in
the lesson and reference sheet points to a file that exists, and schedules nothing. It is a
bounded operational example of the file contracts; it does not show how a model chooses a route,
how well it teaches, or how the pages render in a browser.
