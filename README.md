# Three.js Skills for AI-RULES

> **45 specialized Three.js & NixieFX engineering methods in one installable family.** Production-grade 3D graphics, custom GLSL/WGSL shaders, lighting, skeletal animation, physics, particle systems, and WebGL/WebGPU optimization.

Building advanced 3D web applications requires deep mathematical and rendering discipline: shader pipelines, draw-call budgets, shadow-map cascades, matrix transformations, and asset management. **Three.js Skills** packages 45 battle-tested graphics specialist methods into a single unified capability, giving your agent expert guidance without polluting your system prompt with 45 separate skill registrations.

---

## The Specialist Catalog (45 Methods)

The family covers the complete 3D interactive graphics stack:

| Domain | Key Specialists | What They Handle |
|---|---|---|
| **Shaders & VFX** | `threejs-shaders`, `threejs-postprocessing`, `nixie-fx-*` | Custom GLSL/WGSL shaders, postprocessing chains, bloom, depth of field, and NixieFX particle effects. |
| **Lighting & Realism** | `threejs-lighting`, `threejs-shadows`, `threejs-environment` | Physically based lighting (PBR), shadow-map resolution tuning, HDR environments, and tone mapping. |
| **Geometry & Math** | `threejs-geometry`, `threejs-math`, `threejs-procedural` | Custom BufferGeometry, procedural meshes, quaternion rotations, spatial indexing, and raycasting. |
| **Animation & Rigging** | `threejs-animation`, `threejs-skeletal`, `threejs-morph` | Keyframe tracks, skeletal bone hierarchies, morph targets, and animation mixer blending. |
| **Interaction & Input** | `threejs-interaction`, `threejs-camera`, `threejs-controls` | Raycast pointer picking, orbit/first-person camera controls, viewport resize, and touch events. |
| **Architecture & Game** | `threejs-architecture`, `threejs-game-director`, `threejs-performance` | Component scene graphs, GLTF/GLB asset loading pipelines, draw-call minimization, and FPS profiling. |

Consult the complete [Specialist Index](references/specialists.md) for detailed descriptions of all 45 methods.

---

## When to Use

| ✅ Use Three.js Skills For | ❌ Do NOT Use For |
|---|---|
| WebGL/WebGPU 3D scenes, models, and canvases | Standard 2D DOM / HTML / CSS web development |
| Custom vertex/fragment shaders and visual effects | Routine React / Tailwind frontend component styling |
| 3D asset optimization, GLTF loading, and rigging | General full-stack architecture without 3D surfaces |
| 3D browser games, interactive physics, and cameras | Backend-only services or simple canvas chart widgets |

---

## Quick Start

### 1. Installation

Install via the **AI-RULES CLI** (included in the `threejs` and `everything` profiles):

```sh
# Install CLI
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES && python -m pip install .

# Option A: Install Standalone Family
ai-rules setup --capability threejs-skills --host <host> --scope project --project-root .

# Option B: Install Complete 3D Dev Profile (Three.js + Andino + Focus + Search First)
ai-rules setup --profile threejs --host <host> --scope project --project-root .
```

<details>
<summary>Manual Installation</summary>

```sh
git clone --depth 1 --single-branch --branch threejs-skills https://github.com/andinoferdi/AI-RULES.git "<skills-dir>/threejs-skills"
```

| Host | Global Skills Directory | Project Skills Directory |
|---|---|---|
| **Codex** | `~/.agents/skills/threejs-skills` | `.agents/skills/threejs-skills` |
| **Claude Code** | `~/.claude/skills/threejs-skills` | `.claude/skills/threejs-skills` |
| **OpenCode** | `~/.config/opencode/skills/threejs-skills` | `.agents/skills/threejs-skills` |
| **Antigravity** | `~/.gemini/antigravity-cli/skills/threejs-skills` | `.agents/skills/threejs-skills` |

</details>

### 2. Usage Examples

Invoke the family name, and optionally name a specific specialist method:

- **Claude Code:**
  `/threejs-skills create a custom underwater caustics shader using threejs-shaders`
- **Codex:**
  `$threejs-skills optimize skeletal animation blending and LOD transitions for character models`
- **With Andino Workflow:**
  `Use andino-workflow and threejs-skills to build an interactive solar system with orbital controls and physically based lighting`

---

## Architecture & Integration

- **Single Host Registration:** Installs as one clean directory (`threejs-skills`) containing one root `SKILL.md`. Internal specialist guides are loaded selectively on demand from `skills/<method-id>/GUIDE.md`.
- **With Andino Workflow:** When Andino is active, it retains the overall lifecycle, execution plan, and checkpointing. `threejs-skills` provides technical domain execution within that task.
- **Standalone:** Functions autonomously within the host's normal task context.

---

## References & Verification

- [`SKILL.md`](SKILL.md) — Runtime contract and selective method dispatching rules.
- [`references/specialists.md`](references/specialists.md) — Index and trigger criteria for all 45 methods.
- [docs/threejs/inventory.json](https://github.com/andinoferdi/AI-RULES/tree/main/docs/threejs) — Complete verification inventory, file hashes, and provenance records.
