# Andino Workflow

> **Adaptive problem-solving protocol & 59 composable member skills for AI coding agents.** Proportional investigation, evidence-based decisions, and single durable checkpoints across development, troubleshooting, and research.

AI agents without disciplined governance either jump straight into uncontrolled coding, get trapped in repetitive loops, or accumulate bloated unverified changes. **Andino Workflow** acts as the central coordinator for your coding agents (Claude Code, Codex, OpenCode, Antigravity), adapting the depth of investigation to the task and providing 59 specialized, first-class member skills (`andino-*`).

```
  DISCOVER          PLAN            BUILD           VERIFY          DELIVER
 ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
 │Brainstorm│ ─▶ │Architect │ ─▶ │   TDD    │ ─▶ │ DevTools │ ─▶ │  Review  │
 │Interview │    │Decompose │    │Increment.│    │Debug Loop│    │Handoff/PR│
 └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

---

## Bidirectional Architecture

Andino Workflow provides true two-way integration between the master orchestrator and its member skills:

1. **Orchestrated Mode (`/andino-workflow`):**
   When invoked at the task level, Andino evaluates the current task phase, dynamically activates the matching member skill (e.g., `andino-brainstorming` or `andino-tdd`), maintains the single durable execution plan, and coordinates clean phase transitions.
2. **Direct Mode (`/andino-<method>`):**
   When an individual skill is invoked directly (e.g., `/andino-tdd` or `$andino-debugging`), it immediately executes that technique while inheriting Andino Workflow's governance (evidence verification, checkpointing, and anti-loop guards) without recursive overhead.

---

## Member Skills Catalog (59 Skills)

All 59 methods are installed as native, discoverable skills with the `andino-` prefix:

### 1. Define & Explore
| Skill | What It Does |
|---|---|
| `andino-brainstorming` | Explores diverse directions for open-ended or uncertain goals. |
| `andino-decision-interview` | Interrogates missing requirements one focused question at a time. |
| `andino-idea-refine` | Sharpens rough concepts with feasibility and value trade-offs. |
| `andino-specification` | Produces structured buildable specifications before implementation. |
| `andino-design-prototype` | Builds throwaway visual or logic spikes to resolve design questions. |

### 2. Architecture & Planning
| Skill | What It Does |
|---|---|
| `andino-planning` | Formulates sequenced implementation plans with acceptance criteria. |
| `andino-plan-execution` | Executes accepted plans inline with progress checkpointing. |
| `andino-task-decomposition` | Breaks features into bite-sized, dependency-ordered units. |
| `andino-api-and-interface-design` | Designs contract-first APIs, error semantics, and module boundaries. |
| `andino-deep-module-design` | Creates deep interfaces that hide internal complexity cleanly. |
| `andino-architecture-survey` | Identifies architectural friction points and maintainability debt. |
| `andino-domain-modeling` | Aligns code vocabulary with domain models and ADRs. |

### 3. Implementation & Testing
| Skill | What It Does |
|---|---|
| `andino-tdd` | Enforces the strict RED-GREEN-REFACTOR cycle with automated tests. |
| `andino-incremental-implementation` | Implements thin vertical slices with commit-as-save-point discipline. |
| `andino-source-driven-development` | Grounds framework decisions in official, cited documentation. |
| `andino-constraint-driven-development` | Establishes and enforces immutable quality contracts. |
| `andino-doubt-driven-development` | Runs adversarial fresh-context reviews on critical invariants. |
| `andino-frontend-ui-engineering` | Implements responsive, accessible (WCAG AA) component interfaces. |

### 4. Verification & Debugging
| Skill | What It Does |
|---|---|
| `andino-debugging` | Disciplined 5-step root-cause diagnosis for failing tests or bugs. |
| `andino-verification` | Requires falsifiable proof before declaring any task complete. |
| `andino-browser-testing-with-devtools` | Live runtime DOM, console, network, and performance profiling. |
| `andino-performance-optimization` | Measure-first performance profiling and bottleneck elimination. |
| `andino-session-diagnostics` | Investigates agent misbehavior, ignored plans, or session loops. |

### 5. Review & Delivery
| Skill | What It Does |
|---|---|
| `andino-code-review` | Multi-axis review across coding standards, smells, and spec compliance. |
| `andino-code-simplification` | Reduces cognitive complexity while preserving exact behavior. |
| `andino-security-and-hardening` | Audits OWASP Top 10 vulnerabilities, auth, and trust boundaries. |
| `andino-git-workflow-and-versioning` | Atomic commits, trunk-based development, and changelog management. |
| `andino-handoff` | Compacts active state for seamless cross-agent/session continuation. |
| `andino-pr-description` | Formulates evidence-backed pull request summaries and blast radii. |

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

Andino coordinates seamlessly with AI-RULES sibling capabilities:
- **`focus`:** Default communication layer (installed as a required dependency).
- **`search-first`:** Delegated to whenever meaningful API/external research is required.
- **`council`:** Summoned for high-stakes, multi-perspective strategic forks.
- **`ai-codebase-rescue`:** Delegated to when stabilizing tangled legacy modules.
- **`skripsi-skill`:** Engaged when navigating academic thesis milestones.
- **`threejs-skills`:** Engaged for 3D scene, shader, and WebGL rendering tasks.

---

## References

- [`SKILL.md`](SKILL.md) — Runtime contract and bidirectional dispatching rules.
- [`references/internal-method-index.md`](references/internal-method-index.md) — Exhaustive catalog of all 59 member skills.
- [`references/method-dispatch.md`](references/method-dispatch.md) — Explicit and implicit routing contracts.
- [`references/execution-plan-template.md`](references/execution-plan-template.md) — Portable task checkpoint structure.
