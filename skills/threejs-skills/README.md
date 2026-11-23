# Three.js Skills

Three.js Skills packages 45 specialized Three.js and NixieFX engineering methods into one installable family: 3D graphics, custom GLSL/WGSL shaders, lighting, skeletal animation, physics, particle systems, and WebGL/WebGPU optimization.

Building advanced 3D web applications involves shader pipelines, draw-call budgets, shadow-map cascades, matrix transformations, and asset management. **Three.js Skills** gives your agent domain guidance through one registration rather than adding 45 separate skill registrations to the system prompt.

## What It Does

### The specialist catalog (45 methods)

The family covers these areas of 3D interactive graphics:

| Domain | Key Specialists | What They Handle |
|---|---|---|
| **Shaders & VFX** | `threejs-shaders`, `threejs-postprocessing`, `nixie-fx-*` | Custom GLSL/WGSL shaders, postprocessing chains, bloom, depth of field, and NixieFX particle effects. |
| **Lighting & Realism** | `threejs-lighting`, `threejs-shadows`, `threejs-environment` | Physically based lighting (PBR), shadow-map resolution tuning, HDR environments, and tone mapping. |
| **Geometry & Math** | `threejs-geometry`, `threejs-math`, `threejs-procedural` | Custom BufferGeometry, procedural meshes, quaternion rotations, spatial indexing, and raycasting. |
| **Animation & Rigging** | `threejs-animation`, `threejs-skeletal`, `threejs-morph` | Keyframe tracks, skeletal bone hierarchies, morph targets, and animation mixer blending. |
| **Interaction & Input** | `threejs-interaction`, `threejs-camera`, `threejs-controls` | Raycast pointer picking, orbit/first-person camera controls, viewport resize, and touch events. |
| **Architecture & Game** | `threejs-architecture`, `threejs-game-director`, `threejs-performance` | Component scene graphs, GLTF/GLB asset loading pipelines, draw-call minimization, and FPS profiling. |

Consult the complete [Specialist Index](references/specialists.md) for detailed descriptions of all 45 methods.

## When to Use

| Use for | Do not use for |
|---|---|
| WebGL/WebGPU 3D scenes, models, and canvases | Standard 2D DOM / HTML / CSS web development |
| Custom vertex/fragment shaders and visual effects | Routine React / Tailwind frontend component styling |
| 3D asset optimization, GLTF loading, and rigging | General full-stack architecture without 3D surfaces |
| 3D browser games, interactive physics, and cameras | Backend-only services or simple canvas chart widgets |

## Quick Start

### Installation

Install with the **AI-RULES CLI** (included in the `threejs` and `everything` profiles):

```sh
git clone --branch main https://github.com/andinoferdi/AI-RULES.git
cd AI-RULES && python -m pip install .

# Option A: the Three.js family only
ai-rules setup --capability threejs-skills --host <host> --scope project --project-root .

# Option B: the full 3D profile (Three.js + Andino + Focus + Search First)
ai-rules setup --profile threejs --host <host> --scope project --project-root .
```

`<host>` is one of `codex`, `claude-code`, `opencode`, `antigravity-cli` or `antigravity-ide`.

<details>
<summary>Manual installation</summary>

Copy `skills/threejs-skills/` from `main` into your host's skills directory:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/andinoferdi/AI-RULES.git ai-rules-src
git -C ai-rules-src sparse-checkout set skills/threejs-skills
cp -r ai-rules-src/skills/threejs-skills "<skills-dir>/threejs-skills"
```

| Host | Global skills directory | Project skills directory |
|---|---|---|
| **Codex** | `~/.agents/skills/threejs-skills` | `.agents/skills/threejs-skills` |
| **Claude Code** | `~/.claude/skills/threejs-skills` | `.claude/skills/threejs-skills` |
| **OpenCode** | `~/.config/opencode/skills/threejs-skills` | `.agents/skills/threejs-skills` |
| **Antigravity** | `~/.gemini/antigravity-cli/skills/threejs-skills` | `.agents/skills/threejs-skills` |

</details>

### Usage

Invoke the family name, and optionally name a specific specialist method:

- **Claude Code:**
  `/threejs-skills create a custom underwater caustics shader using threejs-shaders`
- **Codex:**
  `$threejs-skills optimize skeletal animation blending and LOD transitions for character models`
- **With Andino Workflow:**
  `Use andino-workflow and threejs-skills to build an interactive solar system with orbital controls and physically based lighting`

## How It Works

### One registration, guides on demand

The family installs as one directory (`threejs-skills`) with one root `SKILL.md`. Internal specialist guides are loaded as needed from `skills/<method-id>/GUIDE.md`.

## Works With Other Skills

- **Andino Workflow:** When Andino is active, it retains the overall lifecycle, execution plan, and checkpointing. `threejs-skills` provides technical domain execution within that task.
- **Standalone:** Works within the host's normal task context.

## Files

- [`SKILL.md`](SKILL.md) — Runtime contract and selective method dispatching rules.
- [`references/specialists.md`](references/specialists.md) — Index and trigger criteria for all 45 methods.
- `skills/<method-id>/` — The 45 specialist guides, each with its own `README.md` and `GUIDE.md`.
- [`references/legal/license.md`](references/legal/license.md) — MIT license notice for AI-RULES-authored content.
- [docs/threejs/inventory.json](https://github.com/andinoferdi/AI-RULES/tree/main/docs/threejs) — Complete verification inventory, file hashes, and provenance records (in the repository, not installed).

## License

AI-RULES-authored content in this skill is released under the [MIT License](references/legal/license.md). Third-party material keeps its original license (MIT, CC0 or GPL); see the notice beside each bundled resource.
