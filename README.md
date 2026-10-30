# Andino Workflow

Andino Workflow coordinates problem solving for AI coding agents, with 59 member skills for development, troubleshooting, and research. It adjusts investigation to the task, checks decisions against evidence, and keeps one durable checkpoint when work needs to continue across sessions.

Use it with Claude Code, Codex, OpenCode, or Antigravity to select the relevant method, track ongoing work, and verify changes before calling a task complete. The member skills use the `andino-*` prefix.

```
  DISCOVER          PLAN            BUILD           VERIFY          DELIVER
 ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
 │Brainstorm│ ─▶ │Architect │ ─▶ │   TDD    │ ─▶ │ DevTools │ ─▶ │  Review  │
 │Interview │    │Decompose │    │Increment.│    │Debug Loop│    │Handoff/PR│
 └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

---

## Workflow and Direct Invocation

You can invoke the workflow or a member skill directly:

1. **Orchestrated Mode (`/andino-workflow`):**
   Andino checks the current task phase, selects the matching member skill (e.g., `andino-brainstorming` or `andino-tdd`), and maintains one durable execution plan as the work progresses.
2. **Direct Mode (`/andino-<method>`):**
   A directly invoked skill (e.g., `/andino-tdd` or `$andino-debugging`) runs its technique under Andino's rules for evidence, checkpoints, and avoiding repeated unsuccessful work. It does not invoke the workflow recursively.

---

## Member Skills Catalog (59 Skills)

All 59 methods are installed as native, discoverable skills with the `andino-` prefix:

### 1. Define & Explore
| Skill | What It Does |
|---|---|
| `andino-brainstorming` | Explores possible directions for open-ended or uncertain goals. |
| `andino-decision-interview` | Clarifies missing requirements one focused question at a time. |
| `andino-idea-refine` | Refines rough concepts by considering feasibility and value trade-offs. |
| `andino-specification` | Defines requirements clearly enough to guide implementation. |
| `andino-design-prototype` | Builds throwaway visual or logic spikes to resolve design questions. |

### 2. Architecture & Planning
| Skill | What It Does |
|---|---|
| `andino-planning` | Orders implementation tasks and defines acceptance criteria. |
| `andino-plan-execution` | Executes accepted plans inline with progress checkpointing. |
| `andino-task-decomposition` | Breaks features into small tasks ordered by dependency. |
| `andino-api-and-interface-design` | Designs contract-first APIs, error semantics, and module boundaries. |
| `andino-deep-module-design` | Designs interfaces that hide internal complexity. |
| `andino-architecture-survey` | Identifies architectural friction points and maintainability debt. |
| `andino-domain-modeling` | Aligns code vocabulary with domain models and ADRs. |

### 3. Implementation & Testing
| Skill | What It Does |
|---|---|
| `andino-tdd` | Enforces the strict RED-GREEN-REFACTOR cycle with automated tests. |
| `andino-incremental-implementation` | Implements thin vertical slices with commit-as-save-point discipline. |
| `andino-source-driven-development` | Grounds framework decisions in official, cited documentation. |
| `andino-constraint-driven-development` | Defines quality requirements and prevents them from being weakened during implementation. |
| `andino-doubt-driven-development` | Runs adversarial fresh-context reviews on critical invariants. |
| `andino-frontend-ui-engineering` | Implements responsive, accessible (WCAG AA) component interfaces. |

### 4. Verification & Debugging
| Skill | What It Does |
|---|---|
| `andino-debugging` | Uses 5 steps to investigate the root cause of failing tests or bugs. |
| `andino-verification` | Requires evidence that can be checked before declaring a task complete. |
| `andino-browser-testing-with-devtools` | Live runtime DOM, console, network, and performance profiling. |
| `andino-performance-optimization` | Measures performance, locates bottlenecks, and checks improvements. |
| `andino-session-diagnostics` | Investigates agent misbehavior, ignored plans, or session loops. |

### 5. Review & Delivery
| Skill | What It Does |
|---|---|
| `andino-code-review` | Reviews code against the specification, coding standards, and maintainability concerns. |
| `andino-code-simplification` | Reduces cognitive complexity while preserving exact behavior. |
| `andino-security-and-hardening` | Audits OWASP Top 10 vulnerabilities, auth, and trust boundaries. |
| `andino-git-workflow-and-versioning` | Atomic commits, trunk-based development, and changelog management. |
| `andino-handoff` | Records the state another agent or session needs to continue the task. |
| `andino-pr-description` | Writes pull request summaries that explain the changes, affected areas, and verification. |

*View the complete index with trigger/exclusion rules in [`references/internal-method-index.md`](references/internal-method-index.md).*

---

## Quick Start

### 1. Installation

Install via the **AI-RULES CLI** (included in all profiles):

```sh
# Install CLI
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES && python -m pip install .

# Setup Andino Workflow (installs the master orchestrator + all 59 member skills)
ai-rules setup --capability andino-workflow --host <host>
```

<details>
<summary>Manual Installation</summary>

```sh
git clone --depth 1 --single-branch --branch andino-workflow https://github.com/andinoferdi/AI-RULES.git "<skills-dir>/andino-workflow"
```

| Host | Global Skills Directory | Project Skills Directory |
|---|---|---|
| **Codex** | `~/.agents/skills/andino-workflow` | `.agents/skills/andino-workflow` |
| **Claude Code** | `~/.claude/skills/andino-workflow` | `.claude/skills/andino-workflow` |
| **OpenCode** | `~/.config/opencode/skills/andino-workflow` | `.agents/skills/andino-workflow` |
| **Antigravity** | `~/.gemini/antigravity-cli/skills/andino-workflow` | `.agents/skills/andino-workflow` |

</details>

### 2. Usage Examples

- **Master Orchestrator:**
  - Claude Code: `/andino-workflow resume the existing task plan and implement the next slice`
  - Codex: `$andino-workflow resolve database connection pool exhaustion under load`
- **Individual Member Skills:**
  - Claude Code: `/andino-brainstorming explore caching strategies for real-time leaderboards`
  - Claude Code: `/andino-tdd implement the token refresh endpoint with failing tests first`
  - Codex: `$andino-debugging diagnose why the WebSocket handshake drops on mobile clients`
  - Codex: `$andino-code-review review staged changes for security and contract drift`

---

## Integration with Sibling Skills

Andino coordinates with these AI-RULES capabilities:
- **`focus`:** Default communication layer (installed as a required dependency).
- **`search-first`:** Researches APIs and external sources when the task needs that evidence.
- **`council`:** Examines consequential decisions from multiple independent perspectives.
- **`ai-codebase-rescue`:** Helps stabilize tangled legacy modules.
- **`skripsi-skill`:** Guides work on academic thesis milestones.
- **`threejs-skills`:** Supports 3D scene, shader, and WebGL rendering tasks.

---

## References

- [`SKILL.md`](SKILL.md): Runtime contract and rules for workflow and direct invocation.
- [`references/internal-method-index.md`](references/internal-method-index.md): Complete catalog of all 59 member skills.
- [`references/method-dispatch.md`](references/method-dispatch.md): Rules for explicit and implicit method selection.
- [`references/execution-plan-template.md`](references/execution-plan-template.md): Portable task checkpoint structure.
