# Templates

Read at gate 5 only when the repository has no skill conventions of its own. A repository's
README, existing skills or instructions file always win over these templates.

## Skill

Fill every section from the gate artifacts; delete a section rather than leave it empty.

````markdown
---
name: <folder-name>
description: Use when <situations and symptoms that should load this skill>.
---

# <What the agent achieves, as an imperative>

## Purpose
<One paragraph: the failure or capability, and what the agent must leave behind.>

## When to use
- <situation from the brief>
Do not use for: <the near-miss request and where it belongs instead>.

## Procedure
1. <Step>. Done when: <observable output>.
2. <Step>. Done when: <observable output>.

## Excuses that do not apply
| Excuse | Why it does not apply |
| --- | --- |
| "<excuse as said in the evidence>" | <answer> |

Stop signals: <phrases that mean the agent is about to break the rule>.

## Output
<The parts of the output, in order, with a size for each.>

## Verification
- <check an agent or reviewer can run on the output>
````

Keep "Excuses that do not apply" only for discipline rows, and "Output" as an ordered recipe for
shape rows.

## Runbook (for people, or people and agents together)

````markdown
# Runbook: <operation>

## Preconditions and authority
- <role or permission required>
- <approval, window or ticket>
- <backup or snapshot check, with its command>

## Steps
### 1. <Non-destructive check>
```bash
<exact command>
```
Expected: <output that means continue>
Stop: <output that means abort, and who to tell>

### 2. <Change>
```bash
<exact command>
```
Expected: <output>

## Rollback
When <observable condition>:
1. <exact undo command>
2. <restore command>
3. <evidence to capture, with its command>
````
