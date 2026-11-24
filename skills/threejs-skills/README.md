# Three.js Skills

Three.js Skills packages 57 specialized Three.js and NixieFX engineering methods into one installable family: photoreal environments, open-ocean water, scanned-asset pipelines, custom GLSL/WGSL shaders, lighting, animation, particle systems, games, and WebGL/WebGPU optimization.

Building advanced 3D web applications involves shader pipelines, draw-call budgets, shadow-map cascades, captured assets and one coherent light and colour pipeline. **Three.js Skills** gives your agent domain guidance through one registration rather than adding 57 separate skill registrations to the system prompt.

## What It Does

### The specialist catalog (57 methods)

The family covers these areas of 3D interactive graphics:

| Domain | Key Specialists | What They Handle |
|---|---|---|
| **Realism** | `threejs-realism-director`, `threejs-open-ocean`, `threejs-sky-background`, `threejs-hires-textures`, `threejs-crafted-materials` | The stylized-or-photoreal decision, reference teardown, CC0 scanned assets, open-sea water with a working module, skies, close-up materials, and scored fixed frames. |
| **Shaders & VFX** | `threejs-shaders`, `threejs-postprocessing`, `threejs-procedural-vfx`, `nixie-fx-authoring` | Custom GLSL/WGSL shaders, post-processing chains, real-time effects, and NixieFX particle effects. |
| **Lighting & Image** | `threejs-lighting`, `threejs-shadow-systems`, `threejs-exposure-color-grading`, `threejs-image-pipeline` | Light types and IBL, stable shadows, exposure and tone mapping, and multi-pass image ownership. |
| **Geometry & Worlds** | `threejs-geometry`, `threejs-procedural-geometry`, `threejs-procedural-vegetation`, `threejs-high-poly-models` | BufferGeometry, procedural meshes, plants, detailed models and LODs. |
| **Animation & Camera** | `threejs-animation`, `threejs-procedural-animation`, `threejs-camera-direction` | Keyframe and skeletal animation, procedural motion, and camera rigs. |
| **Games** | `threejs-game-director`, `threejs-gameplay-systems`, `threejs-qa-release` | Building, upgrading, testing and shipping browser games. |

Consult the complete [Specialist Index](references/specialists.md) for detailed descriptions of all 57 methods.

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
- **Photoreal scene:**
  `/threejs-skills make this island scene photoreal`
- **Codex:**
  `$threejs-skills optimize skeletal animation blending and LOD transitions for character models`
- **With Andino Workflow:**
  `Use andino-workflow and threejs-skills to build an interactive solar system with orbital controls and physically based lighting`

## How It Works

### One registration, guides on demand

The family installs as one directory (`threejs-skills`) with one root `SKILL.md`. Internal specialist guides are loaded as needed from `skills/<method-id>/GUIDE.md`.

### Target and selection record

Before visual work the agent settles the target: stylized (code-made) or photoreal (captured assets), because code-only work tops out at stylized. It then writes a short selection record naming the renderer, the methods it read in full and the nearby methods it left out, so you can see which guides shaped the result.

## Works With Other Skills

- **Andino Workflow:** When Andino is active, it retains the overall lifecycle, execution plan, and checkpointing. `threejs-skills` provides technical domain execution within that task.
- **Standalone:** Works within the host's normal task context.

## Files

- [`SKILL.md`](SKILL.md) — Runtime contract and selective method dispatching rules.
- [`references/specialists.md`](references/specialists.md) — Index and trigger criteria for all 57 methods.
- `skills/<method-id>/` — The 57 specialist guides, each with its own `README.md` and `GUIDE.md`.
- [`references/legal/license.md`](references/legal/license.md) — MIT license notice for AI-RULES-authored content.
- [src/ai_rules/verification/data/threejs_inventory.json](https://github.com/andinoferdi/AI-RULES/blob/main/src/ai_rules/verification/data/threejs_inventory.json) — Complete verification inventory and file hashes (in the repository, not installed).

## License

AI-RULES-authored content in this skill is released under the [MIT License](references/legal/license.md). Third-party material keeps its original license (MIT, CC0 or GPL); see the notice beside each bundled resource. Eleven methods are adapted from [MengTo/Skills](https://github.com/MengTo/Skills) under the MIT license; each keeps its notice in `references/legal/mengto-skills-license.md`.
