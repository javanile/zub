---
title: droids-engine
description: "A Zig game engine built agent-first: stdin/stdout control protocol, headless rendering, and scene introspection so coding agents can drive the build-run-capture-inspect loop directly."
license: Zlib
author: justinGrosvenor
author_github: justinGrosvenor
repository: https://github.com/justinGrosvenor/droids-engine
keywords:
  - ai-agents
  - claude
  - game-engine
  - gamedev
  - headless
  - renderer
  - webgpu
date: 2026-07-19
category: game-development
updated_at: 2026-07-19T17:14:34+00:00
last_sync: 2026-07-19T17:14:34Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 4
distributable_binary_count: 4
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/justinGrosvenor/droids-engine/
---

# droids

A Zig game engine built agent-first. Every game you build on droids gets a stdin/stdout
control protocol, headless rendering, and scene introspection for free — so an agent
(Claude Code, Codex, a shell script) can drive the whole build → run → capture → inspect
loop without a wrapper process, a GUI, or a window server.

```bash
printf 'load /tmp/model.glb\ncamera 5 6 5 0 0 0\nscene\ncapture /tmp/preview.jpg\nquit\n' \
  | ./zig-out/bin/preview
```

That single pipe loads a model, positions the camera, dumps the scene graph as text, and
writes a rendered JPEG to disk. The agent reads stdout and the image, decides what to
change, and pipes the next command sequence.

## Why

Most engines assume a human at a keyboard: a window, a viewport, a mouse. An agent has
none of those. droids inverts the default — the headless, scriptable path is the primary
interface, and the windowed path is the option on top. Humans and agents drive the same
primitives, so there is no separate "automation API" to keep in sync with the real one.

## Requirements

- Zig 0.16.0 (current stable — the codebase targets the stable `std.Io` API, not master)
- Blender (optional) for the model-authoring bridge

[`zig-webgpu`](https://github.com/justinGrosvenor/zig-webgpu) and
[`mathkit`](https://github.com/justinGrosvenor/mathkit) are fetched automatically as
pinned dependencies — no sibling checkouts needed:

```bash
git clone https://github.com/justinGrosvenor/droids-engine.git droids
cd droids && zig build
```

## Build

```bash
zig build                      # preview binary → zig-out/bin/preview
zig build -Dheadless=true      # no native windowing (server / scripting mode)

zig build demo                 # rendering demo
zig build editor               # scene editor with harness support
zig build test                 # unit tests
zig build bench                # job-system benchmarks
```

`-Dheadless=true` passes through to `zig_webgpu` so the renderer never links native
windowing. Downstream games should forward the option to their `droids` dependency.

## Modules

Exposed via `b.dependency("droids", ...)`:

| Module | What it is |
|---|---|
| `renderer` | WebGPU renderer — scene graph, meshes, materials, instancing, text, picking, shadow map, tween, `SceneRenderer`, scene inspector |
| `harness` | Line-based stdin/stdout protocol for headless control ([src/harness.zig](src/harness.zig)) |
| `jobs` | Chase-Lev work-stealing job system ([docs/jobs.md](docs/jobs.md)) |
| `mem` | Block pool + arena allocators |
| `registry` | Generational asset registry (meshes, materials, textures, prefabs) |
| `validate` | Mesh sanity checks — vertex counts, index alignment, bounds, normals |
| `scene_parser` | Markdown scene DSL parser |
| `gpu_utils` | Shared GPU resource helpers |
| `mathkit` / `gpu` | Re-exported math library and WebGPU bindings |
| `console` | Write-only stdout helpers |

## The harness protocol

Commands go in on stdin, one per line. After each response the harness writes a `READY`
sentinel so the caller knows it can send the next one. Closing stdin quits.

Every droids game inherits the built-in command set — `capture`, `scene`, `inspect`,
`load`, `dump`, `camera`, `move`, `scale`, `rotate`, `color`, `hide`, `show`, `delete`,
`create`, `rename`, `parent`, `fov`, `light`, `shadow`, `bg`, `help`, `quit`. Game-specific
commands arrive as `.line` and are dispatched by the game.

Wiring is a `switch` over `Command` in your game loop; see the walkthrough in
[CLAUDE.md](CLAUDE.md#harness-protocol) and the reference implementations in
[`preview/main.zig`](preview/main.zig) and [`editor/main.zig`](editor/main.zig).

Name your nodes (`scene.setName(handle, "board")`) — the scene dump is only as useful to
an agent as the names in it.

## SceneRenderer

`renderer.SceneRenderer` bundles the standard GPU plumbing — uniforms, shadow map, bind
groups, lit/alpha pipelines, depth buffer — into one init, with a split-phase draw API so
games can inject custom passes between opaque and alpha:

```zig
var sr = try renderer.SceneRenderer.init(r.device, r.queue, r.format, r.width, r.height);
defer sr.deinit();

sr.ensureDepthSize(r.device, r.width, r.height);
sr.uniforms.writeFrame(r.queue, &frame_data);
_ = sr.uploadSceneUniforms(r.queue, &scene, vp, 0);
sr.shadowPass(enc, r.queue, &scene, light_vp, &.{});
const pass = sr.beginMainPass(enc, frame);
sr.drawOpaque(pass, &scene, 0);
// custom draws here — grid lines, instanced overlays
sr.drawAlpha(pass, &scene, 0);
```

All fields are public; reach into `sr.uniforms`, `sr.bindings`, `sr.pipeline_layout` for
custom pipelines. See [docs/renderer.md](docs/renderer.md) and [`demo/main.zig`](demo/main.zig).

## Shader library

`renderer` ships WGSL sources and pipeline helpers: `standard_lit`, `standard_toon`,
`standard_hologram`, `standard_outline`, `standard_sky`, `standard_ground`, `standard_line`,
plus a post-process chain (`tonemap`, `bloom_threshold`, `blur`, `bloom_composite`) and
`PostProcessStack` / `StandardBindings` to wire them up. Material shaders share a unified
6-binding material group.

## Blender pipeline

[`tools/blender_bridge.py`](tools/blender_bridge.py) is a JSON command interface for
Blender — build models, apply modifiers, export GLB — in one-shot or persistent server
mode. [`tools/blender_mcp.py`](tools/blender_mcp.py) wraps it as an MCP server so Claude
Code can call it directly (`blender`, `execute_blender_code`, `preview`, `ingest`,
`catalog`).

The asset flow: `ingest` a GLB → refine in Blender → `preview` it rendered in the engine →
`catalog approve` to publish it to `assets/<name>/` with a GLB, thumbnail, and metadata.

**Preview in the engine, not in Blender.** Blender renders are slow and don't show how the
model will actually look in-game. Export the GLB, then `load` + `capture` in a droids
binary.

Configuration lives in `.mcp.json`; set `BLENDER_PATH` to override the Blender binary and
`ASSET_CATALOG_ROOT` to relocate the catalog.

## Layout

```
src/       engine source
vendor/    stb_image, stb_truetype, meshoptimizer, basis_universal
tools/     Blender bridge + MCP server
preview/   minimal model viewer — the agent loop's default target
demo/      rendering demo
editor/    scene editor
bench/     job-system benchmarks
tests/     integration tests
docs/      jobs.md, renderer.md
```

[CLAUDE.md](CLAUDE.md) carries the detailed agent-facing reference — full command tables,
harness wiring code, and Blender bridge footguns.

## Related

- [mathkit](https://github.com/justinGrosvenor/mathkit) — the math library, developed alongside this engine
- [zig-webgpu](https://github.com/justinGrosvenor/zig-webgpu) — the wgpu-native binding underneath the renderer

## License

zlib. See `LICENSE`.
