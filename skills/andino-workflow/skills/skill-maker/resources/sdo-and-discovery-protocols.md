# Skill Discovery Optimization (SDO) and Discovery Protocols

Supporting craft protocol for `andino-skill-maker`. Read with [SKILL.md](../SKILL.md) and [GUIDE.md](../GUIDE.md).

## 1. The Discovery Lifecycle Across Runtimes

Modern agent runtimes (Claude Code, Codex, Antigravity, OpenCode) operate in two distinct discovery stages:
1. **Startup / Indexing Stage:** The host pre-loads **only** YAML metadata (`name` and `description`) across all installed skills into the root system prompt or tool catalog.
2. **On-Demand Activation Stage:** The model reads the full `SKILL.md` body and supporting resources **only** after determining that the triggering conditions match the current user intent.

Because the description is present in every turn while the skill body is deferred, the description acts as an **activation gate**. If the gate is improperly constructed, either the skill will never trigger (*false negative*), trigger indiscriminately (*false positive*), or—worst of all—cause the model to bypass the full skill body entirely.

## 2. The Golden Rule: Trigger Conditions ONLY

```
CRITICAL PRINCIPLE:
Description = WHEN to use (trigger conditions & symptoms)
Description != WHAT the skill does (workflow or process summary)
```

### The Workflow Summary Leakage Trap

Empirical testing across frontier LLMs exposes a severe failure mode:
When a skill's description summarizes its internal workflow, the model frequently treats the description as a complete inline instruction and **skips reading the full skill body**.

**Documented Empirical Case Study:**
- **Leaky Description:** `description: Code review between tasks - dispatches subagent per task with spec and quality review`
  - *Observed AI Behavior:* The agent executed only a single, shallow review pass. It completely skipped reading `SKILL.md`, ignoring the mandatory two-track review protocol (Track 1: Spec Compliance, Track 2: Code Quality) and the 5-round escalating fix loop.
- **Trigger-Only Description:** `description: Use when executing implementation plans with independent tasks in the current session`
  - *Observed AI Behavior:* The agent recognized the activation match, called the skill, read the full operational flowchart, and faithfully executed both review tracks.

**Mechanical Reality:** Summarizing workflow in metadata creates a cognitive shortcut. LLMs optimize for minimal effort under token pressure; given a summarized workflow in context, the model will rationalize that fetching the full skill is redundant.

## 3. Description Specification & Rules

Every skill frontmatter must conform to the following schema:

```yaml
---
name: andino-kebab-case-name
description: Use when [specific triggering symptoms, situations, and operational conditions]
---
```

### Mandatory Constraints
1. **Third-Person Register:** Injected into system prompts; write in third-person imperative. Never use first-person (`"I will help you..."`) or conversational filler.
2. **"Use when..." Anchor:** Always start the description with `"Use when..."` to force focus onto observable external triggers.
3. **Problem-Oriented, Technology-Agnostic:** Describe the underlying symptom or problem (*"tests pass/fail inconsistently"*, *"subagent write sets collide"*), not incidental tool signatures (*"tests use setTimeout"*), unless the skill itself is intrinsically technology-specific.
4. **Length Ceiling:** Maximum 1024 characters total frontmatter. Target descriptions between 150 and 350 characters for maximum token efficiency.

### Negative Guidance: What Never Goes into Descriptions
- Do not list internal steps (*"first do A, then do B, then return C"*).
- Do not state output formats (*"generates a 5-column markdown table with..."*).
- Do not include governance justifications or legal notices in metadata.

## 4. Contrastive Description Examples

| Quality | YAML Description Example | Mechanical Evaluation |
| :--- | :--- | :--- |
| **FAIL** (Vague) | `description: For debugging code and tests.` | Too abstract; matches almost any request, causing false-positive pollution. |
| **FAIL** (First Person) | `description: I help you write unit tests when they fail.` | Conversational prompt contamination; lacks precise activation boundary. |
| **FAIL** (Workflow Leak) | `description: Systematic debugging by reproducing the bug with a script, minimizing input, forming hypotheses, and applying minimal fix.` | **Fatal Leak:** Model will attempt to debug inline using this sentence and skip the 6-phase gated FSM in `SKILL.md`. |
| **FAIL** (Implementation Detail) | `description: Use when tests use setTimeout or sleep and are flaky.` | Excessively narrow; misses event loop timing, race conditions, and socket races. |
| **PASS** (Crisp Trigger) | `description: Tests/build fail, runtime output is wrong, a regression slows down or a bug is reported. Operates under Andino Workflow governance.` | Explicit triggers (failures, wrong output, regression); zero workflow leak. |
| **PASS** (Domain Seam) | `description: Bounded independent tasks, parallel dispatch, or subagent-driven implementation under parent ownership. Operates under Andino Workflow governance.` | Precise architectural preconditions without summarizing worker protocols. |

## 5. Keyword Coverage Engineering

Future agents search skill catalogs using regex, grep, and semantic retrieval. Embed terms that appear in real developer workflows:

1. **Verbatim Error Signatures:**
   Include exact compiler, runtime, or harness errors:
   - `"ENOTEMPTY"`, `"ECONNREFUSED"`, `"SIGSEGV"`, `"timeout exceeded"`, `"circular dependency"`.
2. **Operational Symptoms:**
   Use the exact terms an engineer or agent types when encountering friction:
   - `"flaky"`, `"hanging"`, `"zombie process"`, `"context pollution"`, `"race condition"`, `"memory leak"`, `"stale cache"`.
3. **Synonym Clusters:**
   Cover natural terminology clusters across stacks:
   - `timeout / hang / freeze / block`
   - `cleanup / teardown / afterEach / dispose / unmount`
   - `mock / stub / fake / spy / double`
4. **Tool and Protocol Vocabulary:**
   Reference relevant tools, file types, and protocols:
   - `pytest`, `cargo`, `docker-compose`, `webpack`, `git rebase`, `jsonl`.

## 6. Naming Conventions

Skill naming directly influences discovery score:
- **Active Voice / Verb-First:** Prefer `andino-skill-maker` over `andino-skill-creation-system`; prefer `condition-based-waiting` over `async-helpers`.
- **Gerunds (-ing) for Operational Protocols:** Gerunds (`brainstorming`, `debugging`, `delegation`, `planning`) cleanly denote ongoing active methodologies.
- **Flat Namespace Integrity:** Names must consist strictly of lowercase letters, numbers, and hyphens (`[a-z0-9-]+`). No uppercase, underscores, or parentheses.
