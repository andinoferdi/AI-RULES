# Out-of-scope records

Read this when a new request may repeat a past rejection, or when the maintainer rejects an
enhancement. The project's `.out-of-scope/` folder (or the location its tracker configuration
names) keeps one Markdown file per rejected **concept**, not per issue. It does two jobs:

1. **Memory.** The reason for a rejection survives after the issue is closed.
2. **Deduplication.** When the same idea returns, triage shows the earlier decision instead of
   arguing it again.

```text
.out-of-scope/
├── plugin-system.md
├── offline-sync.md
└── public-api.md
```

## Matching a new request

During step 3, read every file in the folder. Match by concept, not by keyword: "user
scripts", "extensions" and "custom hooks" can all be the concept a `plugin-system.md` record
rejected. When a record matches, show it to the maintainer with its reason and ask:

> This resembles `.out-of-scope/plugin-system.md`. It was rejected because <reason>. Do you
> still feel the same way?

Do not close anything yet. The maintainer answers one of three ways:

| Answer | What happens |
| --- | --- |
| **Confirm** | Add the new item to the record's Prior requests list, comment, then close the item as wontfix |
| **Reconsider** | Delete or update the record; the item goes through normal triage |
| **Distinct** | The ideas are related but different; the item goes through normal triage and the record stays |

## Writing a record

Write or extend a record only when the maintainer rejects an **enhancement** (an issue or a
pull request) as wontfix. Never for a bug, and never when the request is closed because the
behavior **already exists**: that is a built feature, and recording it would make later
triage reject requests for something the project actually does. The closing comment points to
where the feature lives instead.

1. Check whether a record for the same concept already exists.
2. If it does, append the item to its Prior requests list; keep its reason unless the
   maintainer gave a new one.
3. If not, create `<concept>.md` with the format below and the item as its first prior
   request.
4. Post a comment on the item (disclaimer first) explaining the decision and naming the file.
5. Close the item with the wontfix label.

### Format

Write it like a short design note for someone meeting the decision for the first time:
paragraphs, examples and code where they help.

```markdown
# Plugin system

The project does not load third-party plugins or user scripts.

## Why this is out of scope

Every command runs with the user's credentials, so loading arbitrary code would hand those
credentials to whoever wrote the plugin. A sandbox would need a permission model the project
does not have. Users who need automation call the CLI from their own scripts instead.

## Prior requests

- #31: "Support plugins"
- #58: "Let me add custom commands"
```

### Naming and reasons

- Name the file after the concept in short kebab-case (`plugin-system.md`, `offline-sync.md`),
  so someone scanning the folder knows what was rejected without opening it.
- Give a reason that lasts: the project's scope or philosophy, a technical constraint, or a
  strategic decision. "Not now" or "we're busy" is a deferral, not a rejection; leave the item
  open (needs-triage or ready-for-human) instead of writing a record.

## Changing a decision

When the maintainer reconsiders a concept, delete or update the record. Old closed issues stay
closed as history; the item that prompted the change goes through normal triage.
