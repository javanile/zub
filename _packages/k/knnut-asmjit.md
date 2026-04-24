---
title: asmjit
description: AsmJit on the Zig Build System
license: BSD-3-Clause
author: KNnut
author_github: KNnut
repository: https://github.com/KNnut/asmjit
keywords:
  - asmjit
date: 2026-04-18
updated_at: 2026-04-18T12:08:37+00:00
last_sync: 2026-04-18T12:08:37Z
package_kind: library
has_library: true
has_binary: false
has_distributable_binary: false
binary_count: 0
distributable_binary_count: 0
multiple_binaries: false
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/KNnut/asmjit/
---

# AsmJit

[AsmJit](https://asmjit.com/) on the [Zig Build System](https://ziglang.org/learn/build-system/).

## Usage

Add this package to `build.zig.zon`:

```sh
zig fetch --save git+https://github.com/KNnut/asmjit
```

And then import `asmjit` in `build.zig` with:

```zig
const asmjit_dep = b.dependency("asmjit", .{
    .target = target,
    .optimize = optimize,
});
lib.root_module.linkLibrary(asmjit_dep.artifact("asmjit"));
```
