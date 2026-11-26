# Intent checklists

Pick the row whose signals match the task in the prompt; a prompt that fits two rows uses both.
A row only chooses three things: which project facts to check, which facts to ask the user for,
and which verification step to add. It never adds a requirement, technology, cause or design the
user did not give. When the project cannot be read, skip the "Check" column and say so in the
diagnosis.

| Intent | Signals | Check in the project | Ask the user only when missing | Verification step to add |
| --- | --- | --- | --- | --- |
| bug | error, broken, wrong result, gagal, salah, tidak jalan | The named file and function exist; the test command from the manifest; existing tests for that code; project rules in `AGENTS.md`/`CLAUDE.md` | Full error text, the steps that trigger it, expected and actual result | Write a test that fails on the user's case first, fix, then run the project's test command and report its real output |
| UI or redesign | page, tampilan, desain, remake, landing, responsive, layout | The page file the user means; framework and version from the manifest; dev command | Which page or site; what is wrong now; a visual reference or what "better" means | Open the page and compare against the user's done-when; when the host block names viewport widths for its browser tool, use those widths |
| feature | add, tambah, buat fitur, export, endpoint | Files the feature touches (the page, the data function); framework version; test command | What done looks like, when the prompt never says | Run the test command; check each done-when line through the real entrypoint |
| refactor | rapikan, refactor, clean up, restructure, tanpa ubah perilaku | Callers of the code; existing test coverage of it; test command | Nothing, unless the target file is unclear | Record current behaviour with tests before changing code, run the same tests after and expect identical results; list anything that looks wrong without changing it |
| research or decision | which, pilih, compare, library, should we | Versions and constraints the answer depends on (framework, router, existing dependencies) | The options or criteria only the user knows, such as budget or a hosting rule | One recommendation tied to the user's requirements, with each claim backed by the source it came from |
| review | review, audit, cek PR, periksa | The branch or PR exists; what it should do (description, issue) | What the change is meant to do, when nothing records it | Findings with file and line, each tied to the stated intent |
| install or configure | install, setup, pasang, konfigurasi, MCP | The host files and versions involved | Target host and OS, the source URL | Show the command output or status check that proves it is installed |
| docs or writing | dokumentasi, README, tulis, artikel | The existing document and its audience | Audience and purpose, when the prompt never says | Re-read the result against the user's stated purpose |

Plan-only prompts (`mode: plan only`, "rencana saja") keep the user's mode: the verification step
checks the saved plan (files and checks named for each task), not code.
