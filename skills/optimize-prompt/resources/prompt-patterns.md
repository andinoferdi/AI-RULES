# Prompt patterns

Bundled copy of the rules and examples in the `main` branch `README.md` ("How to Prompt") and
`docs/prompt-examples.md`. Those files are the source of truth. The tables and examples below are
kept verbatim, and a test on `main` fails when they drift. Edit them there first, then here.

## Slot contract

```text
Skills: [domain or sibling skills the workflow cannot infer; never phase skills]
Tools/MCP: [MCP or browser the task must use, e.g. playwright for screenshots]
Mode: [brainstorm first | plan only | just do it]

Task: [what you want in one or two sentences, plus any decision still open]

Context/evidence:
- [full error, file and line, versions]
- [links, screenshots, repro steps]

Done when:
- [a check you could see or run]
- [another check]

Constraints: [what must not change or must not happen]
```

- **Task**, **Context/evidence** and **Done when** are always present. Other slots appear only
  when they change the result, in this order.
- `Mode` holds one of its three values. Omitting it means "just do it".
- Open decisions go in `Task`. `Done when` lists only checks.
- `[brackets]` mark what the user fills in.

Layout, so a person can read the prompt at a glance:

- `Skills`, `Tools/MCP` and `Mode` sit together, one line each. A blank line separates every
  slot from `Task` on.
- A slot with one item stays on one line: `Label: item`.
- A slot with two or more items puts the label alone, then each item on its own `- ` line: one
  check, file, fact or limit per bullet. The open decision in `Task` gets its own bullet.
- No line is wrapped by hand and no line starts with spaces. A bullet that ends in a
  `[placeholder]` takes no period.

Phase members never appear in `Skills`: `andino-brainstorming`, `andino-planning`,
`andino-plan-execution`, `andino-tdd`, `andino-debugging`, `andino-verification` and every other
`andino-*` member. The workflow loads them when their phase arrives. `Mode` and **Done when**
steer them. Name one only to force or forbid it ("plan only, do not execute").

## Which skill to name

| You want to… | Name | Must be in the prompt |
|---|---|---|
| Explore an idea or a feature whose shape is open | nothing extra: write `Mode: brainstorm first` | Goal, references, open decisions |
| Build or change UI | `design-taste-frontend`, `impeccable` | Page, current style, visual reference |
| Build a 3D / Three.js scene | `threejs-skills` (+ the two UI skills for art direction) | Visual style, camera, duration, references |
| Fix a bug or error | nothing extra | Full error, repro steps, expected vs actual, versions |
| Fix something on your machine | nothing extra | OS, device, symptom, what changed recently |
| Install or configure a tool or MCP | nothing extra | Target hosts, source URLs |
| Make a costly-to-reverse decision | `council` | The options and what is at stake |
| Thesis progress or research | `skripsi-skill` | Current chapter/progress, campus |
| Write or polish prose | `natural-writing` | Audience, the draft |
| Stabilize fragile code with repeated regressions | `ai-codebase-rescue` | Which area, the symptoms |
| Review a branch or PR | nothing extra: say "review" in `Task` | Branch or PR, what it should do |
| Read a video, post or social link | `agent-reach` | The link |

`council` runs five advisors plus a peer review. Keep it for decisions that are expensive to undo, not for a hover animation. `ponytail` is for evidenced over-building, not a general "keep code efficient" switch.

## Which MCP to name

| Need | MCP |
|---|---|
| Docs for the exact library version you use | `context7` |
| Click through a flow, screenshot at 360/768/1440 px | `playwright` |
| Console errors, network requests, performance trace | `chrome-devtools` |
| Callers and impact across a large codebase | `graphify` |
| Inspect a binary, APK, bundle or desktop app | `rea` |

## Examples

#### Bug fix: the evidence carries the prompt

```text
Mode: just do it

Task: fix the preloader animation that stops halfway when switching language, then errors.

Context/evidence:
- Repro: open /id, switch to EN.
- Error: [paste the full console error]
- Location: src/app/[locale]/layout.tsx:92.
- Version: Next.js 16.4.3 (Turbopack).

Done when: the full animation plays on every language switch and the console stays clean.

Constraints: keep the current preloader design and timing.
```

#### 3D scene: the domain owner from the start

```text
Skills: threejs-skills, design-taste-frontend, impeccable, council
Mode: brainstorm first

Task:
- Build the scene "The Airship That Cannot Dock".
- Visual style, camera and loop length are still open: decide them with me, then ask council about the art direction before planning.

Context/evidence: [paste the story and the seven animation stages]

Done when:
- All seven stages play in order in one loop.
- The airship never jumps position between frames.
- Its nose always points along its path.

Constraints: keep the story and the seven stages unchanged.
```

#### Machine troubleshooting: details instead of skills

```text
Mode: just do it

Task: fix my webcam.

Context/evidence:
- Windows 11, [laptop/webcam model]
- Black screen in Zoom and the Camera app since [date or update]

Done when: the Camera app and Zoom both show video.

Constraints:
- Ask before changing drivers or system settings.
- No Windows reset or reinstall.
```
