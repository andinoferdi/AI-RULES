# Prompt patterns

The two tables and the `council` note below are copied verbatim from the `main` branch
`README.md` ("Which skill do I name?", "Which MCP do I name?"). A test on `main` fails when they
drift. Edit them there first, then here. They feed suggestions in `Notes` only; nothing from them
is added to the user's prompt.

## Labels people use

People write the same request in many shapes. All of these are fine and stay as written:

- A short header, any casing or language: `skill:`, `skills:`, `mode:`, `mcp:`, `task:`,
  `Skills:`, `Tools/MCP:`, `Mode:`, `Task:`, `Context/evidence:`, `Done when:`, `Constraints:`.
- Mode words in the user's own spelling: `brainstorm-first`, `brainstorm first`, `plan only`,
  `just do it`, "tanya dulu", or a sequence such as "brainstorm, lalu council, lalu planning".
- Free sentences with skills, references and locations inside them.

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
