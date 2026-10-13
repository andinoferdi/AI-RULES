# Focus

AI-RULES personal communication skill adapted from
[i-have-adhd](https://github.com/ayghri/i-have-adhd) by Ayoub Ghriss.
The [MIT notice](references/license.md) is retained with the adaptation.

Focus keeps answer-first writing, concrete actions, manageable steps, relevant
state reminders and visible results. AI-RULES adapts these into natural English
or Indonesian aligned with `A. PRIORITAS`: no diagnosis assumptions, fixed list
caps, compulsory time estimates, repeated recaps or rigid response template.
Long explanations, technical evidence and complete requested outputs stay intact.

## Use

Install from the AI-RULES `main` CLI with `ai-rules setup`. Every profile includes
Focus through Andino's dependency. To install only Focus:

```sh
ai-rules setup --capability focus
```

Reload the host session after installation. Invoke `$focus [request]` through the
Codex skill picker, or `/focus [request]` in Claude Code, OpenCode and Antigravity.
The existing setup registers commands/workflows where those hosts require them.
Use `stop focus` or an ordinary instruction to change the communication preference.

Andino automatically selects and loads Focus once through its native host contract;
no second invocation is needed. Restricted or missing host capabilities must be
reported honestly. Focus owns no plan, workflow, tool permissions or task execution.

Rerun setup to update from the configured `focus` branch. User-modified installations
remain protected by the existing installer reconciliation rules.

For web chatbots, copy `A. PRIORITAS` and `X. Focus` from the `WebBased` README.
That text works without an agent filesystem or skill loader.

## Bundled communication contract

Install the whole folder: `SKILL.md`, this README, and `references/` containing
`license.md`, `priority-a.md`, `human-language-indonesia.md` and
`human-language-english.md`. Focus resolves references from its actual installed
directory and instructs the agent to read A and both language files before its
first substantive response. Standalone and Andino activation use the same contract.
Reuse valid context; reload after context loss or package changes. Switching
languages uses already loaded references. Restricted access uses the embedded
essential rules and reports the real boundary without claiming full loading.

A defines communication standards, Focus extends clarity/actionability, and the
language examples provide style only. Host hierarchy, explicit user overrides and
required formats retain authority. No project files or network are needed at runtime.
These are loading instructions, not an enforced host hook. Installer registration
and package checks do not prove model compliance or cross-host communication quality.

WebBased maintains the source at commit
`2d488a46baed247f43d17b44681e197ca400deab`. `priority-a.md` copies the complete
A section from `put-in-your-projects/chat-rules.md`; the fenced A in README was
equivalent at that revision. Both language files are unchanged copies, including
all examples and guardrails. Their textual `chat-rules.md` references denote the
bundled A through SKILL.md's mapping. No source edits or example omissions were
needed. The original upstream attribution and MIT notice remain intact.

Maintainers can check drift with the main quality-plane validator after fetching
the relevant source refs (never during skill use):

```sh
python scripts/validate_skills.py --focus-ref origin/focus --webbased-ref origin/WebBased
```

For an uncommitted runtime tree, replace `--focus-ref` with
`--focus-dir /path/to/focus-package`. Comparison reports differences; it never
overwrites an intentional divergence. Review source changes before updating copies.
See the [family quality contract](https://github.com/andinoferdi/AI-RULES/blob/main/docs/agent-skill-family-standard.md).

Manual smoke checks: informal Indonesian, academic Indonesian, natural/technical
English, mixed languages, complete technical documentation, strict JSON and code-only
output. Check that formats and detail survive, facts/assumptions are not inherited,
greetings and lists are contextual, and `stop focus` prevents reactivation.
Also check first activation reads all three local references, a second turn reuses
them, and restricted access produces an honest fallback. These cases require actual
host execution before claiming behavioral success.
