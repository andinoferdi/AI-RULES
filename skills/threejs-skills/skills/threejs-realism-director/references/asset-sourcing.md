# Asset sourcing for photoreal scenes

Downloads and package installs need the task's authorization. Ask first, name the
files and their sizes, and keep raw downloads out of the shipped folder.

## Sources

- **Poly Haven** (polyhaven.com): CC0 scanned textures, models and HDRIs. Its public
  API lists assets and file URLs per resolution.
- **ambientCG** (ambientcg.com): CC0 textures.
- Anything else: read the licence before use and record it. Do not assume CC0.

## Textures

- Ship per material: colour (sRGB), normal (OpenGL convention, linear) and ARM
  (ambient occlusion, roughness, metalness in R, G, B; linear).
- Choose resolution from the closest camera view: 1k for mid-distance ground and
  props, 2k for hero surfaces seen up close. Match texel density across surfaces
  that meet.
- Convert to WebP for transfer; use KTX2 when a transcoder is configured and verified.
  Data maps (normal, ARM) need a visual check after compression.
- Terrain and rock: world-space or triplanar UVs so scans do not stretch on slopes;
  break tiling with a second scale or rotation. Blend sets by height and slope.
- Set `colorSpace` to sRGB on colour maps only, enable mipmaps and anisotropy capped by
  `renderer.capabilities.getMaxAnisotropy()`.

## Models

- Prefer scanned glTF with its own PBR maps. Decimate to a runtime mesh plus a `_lo`
  LOD, compress geometry (meshopt or Draco) and verify the decoded result.
- Keep scale and proportions of scans; vary rotation and placement, not stretch.
- Instance repeated rocks and plants. Merge static meshes by material.

## Manifest and budget

- Keep a manifest per asset: source id, URL, licence, resolution and shipped bytes.
- Budget the shipped megabytes and the decoded GPU memory (a 2048² RGBA8 texture with
  mips is about 21 MiB on the GPU).
- Load captured assets after the first frame so the scene appears quickly, then swap
  them in without changing UV scale or material identity.
