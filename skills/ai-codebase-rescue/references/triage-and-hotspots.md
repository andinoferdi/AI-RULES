# Choose where to start

Use when the eligible boundary holds more than one candidate area, or when the
request names a symptom but not the code behind it. The goal is one starting target
with a known contract, a change point and a test point. Ranking never widens the
authorized boundary.

## Work from the symptom to the test point

1. **Symptom.** Restate what users or checks observe, with the input that shows it.
2. **Violated contract.** Name the rule the symptom breaks: a requirement, README
   rule, consumer expectation or test. If no contract can be found, the area stays
   INVESTIGATE until the owner states one.
3. **Change point.** The code that must change to restore the contract.
4. **Test point.** The nearest place where a test can observe the effect of that
   change. It is often not the change point: effects surface in a caller, a return
   value, a write or a log.

## Signals to collect

Collect only what the boundary needs. Record each value; rank with the values, not
with an invented score.

| Signal | How to read it |
| --- | --- |
| User symptom or failing check | Direct link to a contract. Strongest reason to start there. |
| Churn | Files changed often in the last months. Frequent change plus defects marks where the next change will land. |
| Fix density | Commits whose message says fix, hotfix or patch on the same file. Patch-on-patch areas hide divergent copies. |
| Size and branching | Long functions, deep nesting, many branches. Proxy for how hard a change is to make safely. |
| Consumers | Importers, callers, config or plugin registrations, external API users. More consumers means a wider blast radius. |
| Test trust | Whether existing tests exercise the contract with meaningful assertions. Green but shallow tests are not protection. |
| Core domain | Money, permissions, data integrity, user-visible output. Raises urgency, not certainty. |

Read-only commands for a Git repository (adjust the scope path):

```sh
# Most-changed files in the scope over the last year
git log --since=12.months --format=format: --name-only -- <scope> | grep -v '^$' | sort | uniq -c | sort -rg | head -15

# Fix-labelled commits on one file
git log --since=12.months --oneline -i --grep='fix' --grep='hotfix' --grep='patch' -- <path> | wc -l

# History of one file, oldest change last
git log --follow --format='%h %ad %s' --date=short -- <path> | head -20

# Who uses a module: imports, plus names in config, plugin lists and strings
grep -rn "<module_name>" --include='*.py' --include='*.json' --include='*.toml' --include='*.yaml' --include='*.cfg' .
```

Commit messages are leads. A message that says "AI patch" or "quick fix" is
provenance, not evidence of a defect; the finding still needs its own proof.

## Rank the candidates

Place each candidate in a churn x complexity quadrant, then intersect with the
reported symptom:

| | Complex | Simple |
| --- | --- | --- |
| **High churn** | Start here when it carries the symptom. | Usually fine; check for duplicated rules. |
| **Low churn** | Next, if a contract depends on it. | Leave alone unless the symptom points here. |

A healthy area with good tests gets KEEP even when it changes often. A complex area
nobody changes and no symptom touches stays untouched; record it as assessed.

## Effect sketch and pinch point

Before changing a target, trace forward from the change point to every place its
effect leaves the code: return values, writes, outgoing calls, logs and raised
errors. Draw it as a list or small graph. A **pinch point** is a narrow place that
every interesting effect passes through, such as one public function that both the
preview and the charge path call. A few pins there cover more behavior than many
tests on helpers.

If the sketch shows the change reaching many files or two coupled modules, split
the work or introduce a seam first (see refactoring-moves.md).

## Output

Record a ranked target table in the existing task record:

| Rank | Area | Symptom / contract | Churn | Size / branches | Consumers | Test trust | First action |
| --- | --- | --- | --- | --- | --- | --- | --- |

Stop ranking when the top target has a contract, a change point and a test point,
or when the only remaining question is a product decision for the owner.
