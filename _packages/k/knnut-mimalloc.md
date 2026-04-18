---
title: mimalloc
description: mimalloc on the Zig Build System
license: BSD-3-Clause
author: KNnut
author_github: KNnut
repository: https://github.com/KNnut/mimalloc
keywords:
  - mimalloc
date: 2026-04-12
updated_at: 2026-04-12T09:32:47+00:00
last_sync: 2026-04-12T09:32:47Z
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
permalink: /packages/KNnut/mimalloc/
---

# mimalloc

[mimalloc](https://github.com/microsoft/mimalloc) on the [Zig Build System](https://ziglang.org/learn/build-system/).

## Usage

Add this package to `build.zig.zon`:

```sh
zig fetch --save git+https://github.com/KNnut/mimalloc
```

### Static library

Import `mimalloc` in `build.zig` with:

```zig
const mimalloc_dep = b.dependency("mimalloc", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.linkLibrary(mimalloc_dep.artifact("mimalloc"));
```

### Object file

Link with the `mimalloc` single object file in `build.zig` with:

```zig
const mimalloc_dep = b.dependency("mimalloc", .{
    .target = target,
    .optimize = optimize,
    .object = true,
});
exe.root_module.addObject(mimalloc_dep.artifact("mimalloc"));
```
