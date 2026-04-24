---
title: blend2d
description: Blend2D on the Zig Build System
license: BSD-3-Clause
author: KNnut
author_github: KNnut
repository: https://github.com/KNnut/blend2d
keywords:
  - blend2d
date: 2026-04-18
updated_at: 2026-04-18T12:08:30+00:00
last_sync: 2026-04-18T12:08:30Z
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
permalink: /packages/KNnut/blend2d/
---

# Blend2D

[Blend2D](https://blend2d.com/) on the [Zig Build System](https://ziglang.org/learn/build-system/).

## Usage

Add this package to `build.zig.zon`:

```sh
zig fetch --save git+https://github.com/KNnut/blend2d
```

And then import `blend2d` in `build.zig` with:

```zig
const blend2d_dep = b.dependency("blend2d", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.linkLibrary(blend2d_dep.artifact("blend2d"));
```
