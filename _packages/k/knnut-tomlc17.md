---
title: tomlc17
description: tomlc17 on the Zig Build System
license: 0BSD
author: KNnut
author_github: KNnut
repository: https://github.com/KNnut/tomlc17
keywords:
  - tomlc17
date: 2026-04-21
updated_at: 2026-04-21T04:22:04+00:00
last_sync: 2026-04-21T04:22:04Z
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
permalink: /packages/KNnut/tomlc17/
---

# tomlc17

[tomlc17](https://github.com/cktan/tomlc17) on the [Zig Build System](https://ziglang.org/learn/build-system/).

## Usage

Add this package to `build.zig.zon`:

```sh
zig fetch --save git+https://github.com/KNnut/tomlc17
```

And then import `tomlc17` in `build.zig` with:

```zig
const tomlc17_dep = b.dependency("tomlc17", .{
    .target = target,
    .optimize = optimize,
});
const tomlc17_artifact = tomlc17_dep.artifact("tomlc17");
exe.root_module.linkLibrary(tomlc17_artifact);

const wf = b.addWriteFiles();
const translate_c = b.addTranslateC(.{
    .root_source_file = wf.add("c.h",
        \\#include <tomlc17.h>
    ),
    .target = target,
    .optimize = optimize,
});
translate_c.addIncludePath(tomlc17_artifact.getEmittedIncludeTree());
exe.root_module.addImport("c", translate_c.createModule());
```
