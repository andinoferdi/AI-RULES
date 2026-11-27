# Publishing tickets

Read this at step 6, after the user approved the breakdown. The tickets are the same on every
tracker; only where they live and how their edges are stored change.

## Read the tracker configuration

Look in `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.json` or the `AGENTS.md`
section that names the tracker, and record:

- where tickets live (a folder pattern, or a remote tracker and project);
- numbering and file naming;
- the label string for ready-for-agent and ready-for-human, and any other states it lists;
- a required first line for AI-written text;
- anything it says about edges or parents.

The configuration wins over every default here. Without one, use the local folder below and
say so in the report.

## Local folder

- Folder `.scratch/<feature>/issues/`, file `<NN>-<slug>.md`, numbered from `01` in dependency
  order (blockers first), one ticket per file.
- "Blocked by" names ticket numbers in the same folder. A gate in another feature's folder is
  written as a sentence in **What to build**, not as an edge.
- After writing, run the graph check on the folder and fix every finding:
  `python <installed andino-workflow>/skills/writing-tickets/scripts/ticket_graph.py .scratch/<feature>/issues`

## GitHub

Remote writes need the user's go-ahead for this tracker (see the skill's authority rule). Check
`gh auth status` first; a missing login is a stop, not a reason to write elsewhere.

1. Write the tickets as local drafts in a scratch folder and run the graph check on them.
2. Create issues in dependency order so every blocker already has a number:
   `gh issue create --title "<title>" --body-file <draft> --label "<ready-for-agent string>"`.
3. Set native links where the repository supports them, and record each identifier:
   - sub-issue of the parent: `gh api -X POST repos/<owner>/<repo>/issues/<parent>/sub_issues -F sub_issue_id=<child issue id>`;
   - blocked by: `gh api -X POST repos/<owner>/<repo>/issues/<ticket>/dependencies/blocked_by -F issue_id=<blocker issue id>`.

   The `id` here is the issue's numeric database id (`gh api repos/<owner>/<repo>/issues/<n> --jq .id`),
   not its number. When either call is refused or unavailable, keep the "Blocked by" or "Parent"
   section in the body instead.
4. Never close, retitle or edit the parent issue.

Other trackers (Linear, Jira and others): publish through the tool the configuration names,
in the same order, using its native blocking links if it has them and the "Blocked by" section
if not. Without a tool that can write to it, hand the drafts to the user and say they are not
published.

## Reruns without duplicates

Before creating anything, list the tickets that already exist for this work: the feature
folder, the parent's sub-issues, or a search by title and label
(`gh issue list --search "<words> in:title" --state all`).

| Existing ticket | Source now | Action |
| --- | --- | --- |
| Open, still matches | unchanged | Leave it alone |
| Open, behaviour changed | changed | Update it in place; add a dated line saying what changed and why |
| Done | changed after it | Leave it alone; the new behaviour is a new ticket blocked by it if needed |
| Open, no longer wanted | requirement removed | Propose closing it in the quiz; close only on the user's word |
| None | new requirement | New ticket, numbered after the highest existing number |

Edges from new tickets to existing ones use the existing numbers. The report lists created,
changed and untouched tickets separately.
