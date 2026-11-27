# Worked example: shopping list from a meal plan

A recipe app (`larder`) plans meals for the week. The request: "Turn the shopping-list spec and
what we agreed in chat into tickets." The tracker configuration says local Markdown in
`.scratch/<feature>/issues/`, labels `ready` (ready-for-agent) and `needs-human`
(ready-for-human), and AI-written tickets start with `> *AI draft.*`.

## Steps 1 and 2: what is decided, and the code today

From `docs/specs/shopping-list.md`: (R1) `larder list` prints every ingredient of the week's
planned meals; (R2) the same ingredient in two recipes is merged and its amounts added when the
units match; (R3) `larder list --have` hides what the pantry already holds; (R4) the list is
saved so ticking items off survives a restart.

From the chat: amounts in different units are listed separately, not converted (Mo); printing
to PDF is out of scope this release (Mo); whether staples such as salt are always hidden is
undecided, and Priya decides.

Existing tickets: none in `.scratch/shopping-list/issues/` and no title matches elsewhere.

Code: ingredient amounts are parsed by hand in both the recipe importer and the pantry module,
with slightly different rules ("1/2 cup" works only in the importer). Merging amounts needs one
parser, so a prefactor ticket comes first.

## Steps 3 to 5: breakdown and quiz

```text
1. Parse ingredient amounts in one place (AFK, prefactor). Blocked by: none.
   Delivers: importer and pantry read "1/2 cup" and "2 tbsp" the same way.
2. Print the week's shopping list (AFK). Blocked by: 1.
   Delivers: `larder list` prints every ingredient, merged when units match.
3. Hide what the pantry holds (AFK). Blocked by: 2.
   Delivers: `larder list --have` leaves out pantry items, reducing partial amounts.
4. Tick items off and keep them ticked (AFK). Blocked by: 2.
   Delivers: `larder tick <item>` survives a restart.
5. Decide whether staples are always hidden (HITL, Priya). Blocked by: none.
   Delivers: the rule recorded; 3 neither hides nor shows staples specially until then.
Out of scope: unit conversion (listed separately), PDF printing.
Granularity right? Is each "blocked by" a real gate? Merge or split anything?
```

The user answers: "Split nothing. 4 doesn't need 3, right?" It does not; the edge already says
2. They approve.

## Step 6: two of the five files

`.scratch/shopping-list/issues/02-print-the-weeks-shopping-list.md`:

```markdown
> *AI draft.*

# 02: Print the week's shopping list

**Status:** ready

**Blocked by:** 01

**What to build:** `larder list` prints one line per ingredient needed by the meals planned for
the current week, `<amount> <unit> <ingredient>`, alphabetically. The same ingredient in two
recipes is one line with the amounts added when the units match; different units stay separate
lines.

**Out of scope:** converting between units; pantry filtering (ticket 03); staples (ticket 05).

- [ ] With the sample plan (pancakes and soup), `larder list` prints `3 cup flour` once
- [ ] `1 cup milk` and `200 ml milk` print as two lines
- [ ] An empty week prints `nothing planned` and exits 0
```

`.scratch/shopping-list/issues/05-decide-whether-staples-are-hidden.md`:

```markdown
> *AI draft.*

# 05: Decide whether staples are always hidden from the list

**Status:** needs-human

**Blocked by:** None (can start immediately)

**Owner:** Priya

**What to build:** a decision, not code. Options raised: always hide a fixed staples list; hide
only staples the pantry marks as stocked; never hide them. Until it is recorded, ticket 03
treats staples like any other item.

- [ ] The decision is written into the shopping-list spec as a new numbered requirement
```

The graph check on the folder prints `OK 5 tickets`.

## Step 7: report

```text
Tickets: .scratch/shopping-list/issues/ - created 01 Parse ingredient amounts in one place,
  02 Print the week's shopping list, 03 Hide what the pantry holds, 04 Tick items off and keep
  them ticked, 05 Decide whether staples are always hidden; changed none; left alone none
Frontier (can start now): 01, 05
Waiting on people: 05 staples rule - Priya
Out of scope: unit conversion (chat, Mo); PDF printing (chat, Mo)
Graph check: OK 5 tickets
Not published: none
```

## A rerun two weeks later

01 and 02 are done. The spec gains (R5) "`larder list --store <name>` groups lines by the
aisle order saved for that store", and Priya's answer arrives: staples are hidden only when the
pantry marks them stocked.

- 01 and 02 are done: left alone, even though R5 changes how the list prints.
- R5 is new: ticket 06, blocked by 02, numbered after the highest existing number.
- 05 holds the decision: updated in place with "2026-05-12: Priya decided: hide only stocked
  staples", then closed on the user's word.
- 03 is open and now needs that rule: a dated line adds the staples criterion to it.

The report lists created 06; changed 03 and 05; left alone 01, 02 and 04. No ticket exists
twice.
