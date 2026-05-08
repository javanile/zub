---
title: nestegg
description: nestegg on the Zig Build System
license: 0BSD
author: KNnut
author_github: KNnut
repository: https://github.com/KNnut/nestegg
keywords:
  - nestegg
date: 2026-04-18
updated_at: 2026-04-18T12:02:03+00:00
last_sync: 2026-04-18T12:02:03Z
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
permalink: /packages/KNnut/nestegg/
---

# nestegg

[nestegg](https://github.com/mozilla/nestegg) on the [Zig Build System](https://ziglang.org/learn/build-system/).

## Usage

Add this package to `build.zig.zon`:

```sh
zig fetch --save git+https://github.com/KNnut/nestegg
```

And then import `nestegg` in `build.zig` with:

```zig
const nestegg_dep = b.dependency("nestegg", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.linkLibrary(nestegg_dep.artifact("nestegg"));
```
