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
