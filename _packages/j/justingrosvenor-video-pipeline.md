---
title: video-pipeline
description: Agent-authored video effects engine. Describe an effect in plain English, Claude writes the WGSL, the engine fuses and applies it. Zig + libav + WGSL, driven by CLI or MCP.
license: Zlib
author: justinGrosvenor
author_github: justinGrosvenor
repository: https://github.com/justinGrosvenor/video-pipeline
keywords:
  - ai-agents
  - ffmpeg
  - mcp
  - shaders
  - video
  - video-effects
  - wgsl
date: 2026-07-19
category: game-development
updated_at: 2026-07-19T17:15:03+00:00
last_sync: 2026-07-19T17:15:03Z
package_kind: binary
has_library: false
has_binary: true
has_distributable_binary: true
binary_count: 2
distributable_binary_count: 2
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/justinGrosvenor/video-pipeline/
---

# video-pipeline

An agent-authored video effects engine. You describe an effect in plain
English, Claude writes the WGSL, the engine compiles and applies it to a clip,
and you look at the result — then iterate. Effects Claude writes for you
accumulate into a reusable library.

Built in Zig on top of the [droids-engine](https://github.com/justinGrosvenor/droids-engine)
renderer, with `libav*` linked directly for video I/O. Exposed to Claude
Desktop over MCP, and usable as a plain CLI.

```bash
vp preview clip.mp4 -o frame.png --frame 30 --chain "vignette:strength=0.9;grain:amount=0.3"
vp render  clip.mp4 out.mp4 --chain "pixelate:block=12"
```

## Status

Pre-v1, and honest about it: macOS-only, offline batch processing (not
real-time), no GUI, no timeline or keyframes. It is not trying to be After
Effects or Resolve. See [DESIGN.md](DESIGN.md) for the architecture and the
reasoning behind the non-goals.

## Why it exists

TouchDesigner, After Effects, Resolve, ISF, mpv glsl-shaders, and OBS shader
filters are all GUI-first or human-coder-first. None are built around the loop
*agent writes shader → applies to clip → inspects result → refines*. That loop
is what this optimizes for.

**Fusion.** A chain like `vignette;grain` is naively two GPU passes with an
intermediate texture. Effects are composed into a single fused shader instead.
Agents write naive chains; the compiler makes them tight. `vp fuse` prints the
generated shader, and the render path reports what it did:

```
vp: rendering 1280x720 @ 30/1 fps, 2 effects -> 1 passes
```

A type-checked host↔shader uniform contract is a design goal but is **not yet
implemented** — effect parameters currently go through a shared
`params: array<vec4f, 14>` block. See [DESIGN.md](DESIGN.md) for where this is
headed.

## Requirements

- Zig 0.16.0 (stable)
- ffmpeg libraries (`brew install ffmpeg`) — `avformat`, `avcodec`, `avutil`, `swscale`
- macOS on Apple Silicon

```bash
zig build          # -> zig-out/bin/vp and zig-out/bin/vp-ui
```

## CLI

```
vp inspect <in>                                              probe a clip
vp effects                                                   list effects and parameters
vp fuse    <chain-spec>                                      show the fused shader
vp author  <effect.wgsl>                                     add an effect to the library
vp preview <in> [-o out.png] [--frame n] [--chain spec]      single-frame preview
vp render  <in> <out.mp4> [--max-frames n] [--chain spec]    full render
```

Chain spec is `name:k=v,k=v;name2:...` — semicolons separate effects. Built-in
effects include `chromatic_ab`, `vignette`, `grain`, `scanlines`, `halftone`,
`kuwahara`, `pixelate`, and `edge`; run `vp effects` for the full list with
parameter defaults.

`vp-ui` is a windowed player for scrubbing a clip with a live effect chain.

## MCP

`mcp/server.py` is a thin MCP server (stdio) that shells out to the same `vp`
binary, exposing `inspect`, `list_effects`, `preview`, `render`, and
`author_effect`. Previews come back as inline images, so the refine loop
happens in chat.

Point your MCP client at `mcp/server.py` after building `vp`.

## License

zlib. See `LICENSE`.
