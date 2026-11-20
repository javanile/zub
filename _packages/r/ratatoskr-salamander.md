---
title: salamander
description: Typed interfaces between Zig, C, JavaScript and Lua.
license: MIT
author: ratatoskr
author_github: ratatoskr
repository: https://github.com/ratatoskr/salamander
keywords:
  - async
  - c
  - ffi
  - ffi-bindings
  - ffi-wrapper
  - javascript
  - lua
  - plugin-system
  - plugins
date: 2026-11-19
category: networking
updated_at: 2026-11-19T22:01:59+00:00
last_sync: 2026-11-19T22:01:59Z
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
permalink: /packages/ratatoskr/salamander/
---

# Salamander

Typed interfaces between Zig, C, JavaScript and Lua. Write your API once in a `.sal` schema, and plugins, scripts and native code all call each other through it. C++, Rust and C# are being considered next.

Pre-release. Expect breaking changes.

## Features

- `.sal` schemas: structs, enums, bitfields, errors, and traits with plain, async and failing methods.
- Generates Zig, with plain types and their wire forms, and C headers.
- TypeScript and LuaLS typings for scripts' editors.
- Trait objects that cross DLLs, checked by hash, and stop when their owner goes.
- JavaScript (QuickJS-ng) and Lua 5.5 scripts call traits and implement them.
- Calls and detours for signatures only known at runtime.
- Describes code that already exists too, like a game's structs, vtables and functions.
- Edits `.sal` text in place, for editors and tools.
- Windows and Linux on x64, x86 and ARM64, and macOS.

## Building

You need the Zig version in `build.zig.zon` under `minimum_zig_version`. Then:

```
zig build test
```

`zig build build-test` builds the test programs into `zig-out/bin` without running them. Pass `-Dtarget=` to build for another platform, like `x86_64-linux-musl`.

`src/runtime/core.zig` is generated from `core.sal`. After changing it, run `zig build core`.

Want to help? See [CONTRIBUTING.md](https://github.com/ratatoskr/.github/blob/main/CONTRIBUTING.md). Found a security problem? See [SECURITY.md](https://github.com/ratatoskr/.github/blob/main/SECURITY.md).

## License

Copyright (c) 2026 Asgard. Salamander is under the MIT License, see [LICENSE](LICENSE).

Third-party notices in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
