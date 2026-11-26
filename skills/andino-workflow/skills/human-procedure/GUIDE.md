# Prepare steps only a person can do

Internal method ID: `human-procedure`. Stable technique adapted to Andino ownership.

## Purpose

Some steps only a person can take: logging in to a dashboard, copying a secret, approving a
cutover, clicking a toggle in a console the agent cannot reach. Left to a chat message, those
steps arrive vague, out of order, with invented button names and with secrets pasted back into
the conversation. This skill turns them into an artifact the person can follow alone, in their
own shell, in one pass: every value traced from where they get it to where it is written, every
stage ending in something they can see, nothing repeated that already happened, nothing
irreversible without a typed word, and no secret ever passing through the agent.

## Trigger and non-trigger

Use when:

- a required step needs the person's login, browser session, hardware key or approval;
- secrets have to reach `.env`, a CI secret store or a config file and the agent must not see
  them;
- a one-off migration, cutover or rotation runs on the person's machine or accounts;
- the person asks for a wizard, setup script, runbook or checklist for such steps.

Do not select for:

- work the agent can do itself with its own tools and authority: do it (the quick path below);
- general setup advice with no step that only a person can take;
- a request to paste a secret into the chat so the agent can configure it: decline the paste
  and offer this procedure instead;
- a recurring operational process: that is a runbook for the planning skill's recurring-process
  resource.

## Select a resource, not a second lifecycle

Load only the resource the current step names. It runs inside this procedure and current
authority; it starts no second plan.

| Current need | Resource | Skip when |
| :--- | :--- | :--- |
| Stage fields, screen layout, checklist template, script requirements, shell table, `.env` snippets | [stage contract](resources/stage-contract.md) | The quick path applies |
| One complete procedure from repository scan to reply | [worked example](resources/worked-example.md) | The procedure is already clear |

## Prerequisites

Read the person's request and the repository's README, then find out which machine and shell
the person will use: the README, a runbook, the request, or the files they keep (`.ps1`,
`Makefile`, `.zshrc` notes). Note what the agent is allowed to do: local file edits, but no
remote writes, live commands or account actions unless the person authorized them.

## Procedure

**Quick path.** When every step can be done by the agent with its own tools and authority (a
local `.env` line, a config edit, a command that needs no one's login), do it, run the check
that proves it, and reply in a few lines with what changed and the check's result. No script,
no checklist. When any step needs the person, the seven gates below apply, in order; the gate
that a "Done when" line names is not done until that line is true.

1. **Scope from the repository.** Read the files that declare what the procedure must produce:
   `.env.example` and other `.env*` files, the README, `docker-compose*`, framework config,
   every CI workflow (each `secrets.X` and `vars.X` it reads), deploy and infrastructure files,
   and runbooks or docs that describe the services. Leave out what nobody sets: built-ins such
   as `secrets.GITHUB_TOKEN`, and values the workflow sets inline. Write a value map: name,
   where the person gets it, every destination (`.env`, CI secret, CI variable, nowhere),
   secret or public, and what reads it. Add the actions that produce no value (a toggle, an
   endpoint to create, an approval). Done when: the value map is written where the person will
   see it (the artifact header or the reply), and every CI reference and every key in
   `.env.example` is either in it or named as not needed, with the reason.
2. **Find out what may already have happened.** Existing values in `.env`, endpoints or keys
   that may already exist, a previous attempt that stopped halfway, a change whose outcome the
   person does not know. Make the first stage read-only: it observes each such effect (a check
   command, a DNS lookup, a status endpoint, a dashboard row the person reads) and branches:
   not done, do it; done and verified, skip it; anything unclear, stop and ask for the
   observation. Every later stage that has an effect starts with the same check, so a re-run
   repeats nothing. Done when: each effect in the procedure has its check and its three
   branches, and no stage retries an effect whose outcome is unknown.
3. **Map each journey from a confirmed source.** For each stage write the URL and the exact
   labels from a source you read: project docs, a runbook, the provider's current
   documentation, or what the person reported seeing. Where no source gives the path, say so in
   the stage and in the reply, give what is known (where the value ends up, the format it must
   match), and ask the person to write the path down afterwards; never write a click path you
   did not read. Treat platform behaviour the same way: how a CLI reads a value, which scope a
   CI secret has, what a migration command changes. Check it in the tool's `--help`, the
   provider's docs or the source, or mark it unverified in the artifact. Done when: every
   instruction in every stage traces to a source you can name, or carries the word
   "unconfirmed".
4. **Choose the artifact for the person's shell.** A script when the procedure captures or
   writes values, or has three or more stages, and the person's shell is known: bash 3.2 for a
   stock Mac, Windows PowerShell 5.1 for a Windows machine with nothing else, the shell the
   repository already scripts in otherwise. A checklist when there are one or two stages of
   pure clicking, when no interpreter the person has can do the work safely, or when the person
   asked for one. A checklist plus a read-only status script is a good fit for a cutover the
   person drives by hand. Keep the artifact in the repository where the person will run it
   (`scripts/`, `docs/`), and treat it as one-off unless the person wants it kept. Done when:
   the artifact type, the shell and the one-line reason are stated in the reply.
5. **Write every stage to the stage contract.** Use the fields, the screen layout or checklist
   template, and the script requirements in the [stage contract](resources/stage-contract.md):
   one outcome per stage, Stage N of M, the URL before the prompt, hidden input for secrets,
   `.env` writes through the published snippet, every remote write named, shown and confirmed
   with `yes`, every hard-to-undo effect with its consequence, its undo and a stage-specific
   typed word, a Done when per stage observed before the stage counts as done, progress
   recorded by stage name only, and a closing summary. Done when: you walked every stage
   against the requirement list in the stage contract and fixed each line that failed.
6. **Verify without running the person's steps.** Run the syntax check for the shell
   (`bash -n`, `shellcheck` when installed; the PowerShell parser), run the `.env` writer on a
   disposable copy of the real file, and trace every value in the value map to the line that
   captures it and the line that writes it, and every CI name to the workflow line that reads
   it. Do not run anything that touches the person's accounts, remote systems, databases or
   irreversible commands, even to "test" them. Done when: the outputs of those checks are in
   your notes and the trace found no value without a destination and no name that differs from
   the workflow.
7. **Hand off.** Reply with: where and how to run it (folder and exact command, execution
   policy if Windows needs it), what it changes (files, remote targets) and what cannot be
   undone, what is unconfirmed, what the first stage decides, and which non-sensitive results
   to send back (a check command's output, a status line). Never ask for a secret. Done when:
   the reply holds all five and no secret value appears in it or in any file you wrote.

**When the person comes back mid-procedure.** Ask for the last Done when they saw and the
first stage's observations, not for values. Resume at the first stage whose Done when is not
true, after reconciling any effect they are unsure about.

## Rules for every procedure

- **Secrets go from the source to the destination without passing the agent.** Not in chat,
  in a command line, a log, a progress file, a checklist example or the reply. When a secret
  must reach CI from PowerShell, let `gh` prompt for it.
- **Remote writes and hard-to-undo effects belong to the person.** The artifact names the
  target, shows the effect and waits for the typed word; the agent never performs them.
- **Name things the way the source does.** Labels, menu paths and variable names are copied,
  not paraphrased; a different name is a different button.
- **One outcome per stage.** If a stage needs two Done when lines, it is two stages.

## Shortcuts that break the procedure

| Shortcut | What to do instead |
| --- | --- |
| "The dashboard surely has an API keys page under Settings." | Write only paths you read. Mark the rest unconfirmed and give the value's format. |
| "Ask them to paste the token here and I'll write the file." | Hidden input in their own shell; the value never reaches the chat. |
| "Write the GitHub secrets right after each paste; it saves a step." | Show the target repository and the names, wait for `yes`, then write. |
| "They already tried once, so start from stage 1 again." | Make the first stage find out what already happened and branch on it. |
| "bash works everywhere." | Write for the shell the person has: Windows PowerShell 5.1 is not bash. |
| "I'll run the script once to make sure it works." | Run syntax checks and the `.env` writer on a copy; the person runs the live steps. |
| "Environment secrets are the only ones an environment job can read." | Check platform behaviour in its docs or `--help`, or mark it unverified. |
| "A one-line `.env` fix still deserves a proper wizard." | The quick path: do it and say so. |

## Red flags

- A click path or label that no file, document or person supplied.
- A secret in a command-line argument, an `echo`, a log or progress file, or the reply.
- A remote write or an irreversible command with no named target and no typed confirmation.
- A first stage that changes something before checking what already happened.
- A stage without a Done when, or a Done when that shows a secret value.
- A bash script for a Windows-only operator, or bash 4 syntax for a stock Mac.
- The agent running a migration, a key deletion or a `gh secret set` "to test it".
- A wizard for work the agent could have done itself.

## Ownership and permission boundary

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its full procedure, required resources, artifact detail and technical
checks. Coordinator brevity/density never truncates these. User/project authority,
Focus/research/domain boundaries and real invocation controls still apply. Native
`andino-human-procedure` and this guide expose one method, without recursive workflow invocation.

Existing scope authorization persists. Local examples use disposable data; real Git mutations,
external messages/tracker writes, credentials, global setup, deployments and recurring jobs
require their actual authority. A source example never grants it. Preserve user edits, secrets
and current staging.

## Output

- The artifact in the repository: a script for the person's shell, a checklist, or a checklist
  with a read-only status script, each stage built to the stage contract, with the value map in
  its header.
- The reply, in the person's words: how and where to run it, what it changes and what cannot be
  undone, what is unconfirmed, what the first stage decides, and what to send back.
- For the quick path: the change, the check's result, a few lines.

## Verification

Before handing off, check that:

- [ ] every CI `secrets.*`/`vars.*` reference and every `.env.example` key is in the value map
  or named as not needed;
- [ ] each value has its source, destinations, secrecy and reader;
- [ ] the first stage is read-only and every effect has its check-first and three branches;
- [ ] every path and label traces to a source, or is marked unconfirmed in the artifact and the
  reply;
- [ ] platform claims were checked or are marked unverified;
- [ ] the artifact suits the person's shell and passed its syntax check;
- [ ] the `.env` writer ran on a disposable copy and kept the other lines;
- [ ] remote writes and hard-to-undo effects wait for a typed word, with target, consequence
  and undo stated;
- [ ] every stage has a Done when the person can observe without seeing a secret;
- [ ] no live step was run by the agent, and no secret is in any file written or in the reply;
- [ ] the reply holds the five hand-off items.

These are properties of the artifact. How a model behaves with this skill is shown only by a
trial: the comparison record is in the AI-RULES repository at
`docs/validation/human-procedure/trial.md`.

## Worked example and anti-pattern

The [worked example](resources/worked-example.md) builds a two-stage procedure for a sandbox
client and shows what its generated checklist proves and what it does not.

Anti-pattern: "I can't reach the dashboard, so: go to Settings → API, copy the key and paste it
here, and I'll add it to `.env` and GitHub." Invented labels, a secret in chat, a remote write
the person never sees, and nothing that says when a step is done.

## Fallback

- **No interpreter the person can use, or no safe way to write the file:** a checklist built to
  the stage contract; the person edits the file themselves.
- **No source for a path and nobody to ask:** keep the stage, mark it unconfirmed, give the
  value's format and destination, and list it in the reply.
- **A syntax checker is not installed:** say so in the reply and name the command the person
  can run first.

## Local resources

- [Stage contract](resources/stage-contract.md): stage fields, screen layout, checklist
  template, script requirements, shell table and the tested `.env` snippets.
- [Worked example](resources/worked-example.md): one procedure through the gates.
- MIT notice: [references/license.md](references/license.md).

## Provenance

Independently adapted from these audited local snapshot paths (provenance only; runtime never
reads or installs those repositories):

- `mattpocock/skills:skills/engineering/wizard/SKILL.md`

From Matt Pocock's `wizard` (later revisions up to 49dd158 consulted): the repository scan for
values, the rule against inventing steps, the stage-by-stage screen with progress, the URL
before the prompt, hidden entry, the closing summary, static verification without running the
wizard, and the hand-off. Its `template.sh` library is not imported: the stage contract states
its useful behaviour as requirements and publishes tested `.env` snippets instead, and adds
what the template lacks (a read-only first stage, confirmed remote writes, typed gates for
irreversible effects, a refusal to write through a symlink, Windows PowerShell 5.1). Snapshot
identities and licensing are recorded in the package provenance/legal records
([references/license.md](references/license.md)). Upstream bootstrap, automatic commit/push,
hooks and installers are not imported as authority.
