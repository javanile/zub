---
title: tuft
description: A Zig toolkit for modding x64 and x86 Windows games.
license: AGPL-3.0
author: ratatoskr
author_github: ratatoskr
repository: https://github.com/ratatoskr/tuft
keywords:
  - assembly
  - detours
  - directx
  - disassembler
  - dll-injection
  - game-modding
  - hardware-breakpoints
  - hooking
  - imgui
  - memory-scanner
  - modding
  - proxy-dll
  - reverse-engineering
  - vulkan
  - windows
  - x86
  - x86-64
date: 2026-11-21
category: game-development
updated_at: 2026-11-21T19:44:25+00:00
last_sync: 2026-11-21T19:44:25Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 1
distributable_binary_count: 1
multiple_binaries: false
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/ratatoskr/tuft/
---

# Tuft

[![CI](https://img.shields.io/github/actions/workflow/status/ratatoskr/tuft/main_ci.yml?branch=main&label=CI)](https://github.com/ratatoskr/tuft/actions/workflows/main_ci.yml)
[![License](https://img.shields.io/github/license/ratatoskr/tuft)](https://github.com/ratatoskr/tuft/blob/main/LICENSE)
[![Zig](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fraw.githubusercontent.com%2Fratatoskr%2Ftuft%2Fmain%2Fbuild.zig.zon&search=minimum_zig_version%5Cs%2A%3D%5Cs%2A%22%28%5B%5E%22%2B%5D%2B%29&replace=%241&label=zig&color=f7a41d&logo=zig&logoColor=white)](https://github.com/ratatoskr/tuft/blob/main/build.zig.zon)

A Zig toolkit for modding x64 and x86 Windows games.

Pre-release. Expect breaking changes.

## Features

- Function, mid-instruction and pointer hooks, plus patches and code caves.
- Hardware breakpoints and watchpoints.
- Read and write memory in any process, with pattern, signature and value scans.
- Module and symbol lookup.
- x86 and x64 assembly and disassembly in Intel syntax.
- Hooks the game's present for D3D9, D3D10, D3D11, D3D12, OpenGL and Vulkan.
- Frame capture, with HDR.
- Dear ImGui drawn in the game, with plots, gizmos, a sequencer and a graph editor.
- Dev tools: hex view, disassembly, struct editor, address list and search.
- Keyboard, mouse and controller (XInput) input, with rebindable keys and clash checks.
- IME for text boxes, even in games that switch it off, with its windows at the caret.
- Sees every file the game opens, and can change it or serve files from memory.
- DLL injection, even x64 into WoW64, and proxy DLLs.
- Game memory read by the types in a Salamander `.sal` schema, and its `[Sig]`s found.
- Mono and IL2CPP reflection through the game's own runtime.
- Image decoding and PNG encoding.

## Building

You need the Zig version in `build.zig.zon` under `minimum_zig_version`. Then:

```
zig build test
```

`zig build build-test` builds the test programs into `zig-out/bin` without running them, to run one on its own.

`-Dmono-game=<folder>` or `-Dil2cpp-game=<folder>` also tests `tuft_managed` on an installed Unity game's runtime, started without the game. Games with Denuvo can't be tested this way, since it stops the runtime starting outside the game.

Want to help? See [CONTRIBUTING.md](https://github.com/ratatoskr/.github/blob/main/CONTRIBUTING.md). Found a security problem? See [SECURITY.md](https://github.com/ratatoskr/.github/blob/main/SECURITY.md).

## License

Copyright (c) 2026 Asgard. Tuft is under the GNU Affero General Public License v3.0, see [LICENSE](LICENSE). Anything built on it that you share is under the AGPL too.

Want to build something closed-source or commercial on Tuft? Ask about a commercial license at https://docs.wraith.io/commercial.

Third-party notices in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
