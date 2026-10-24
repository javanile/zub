---
title: vitellus
description: Native-first render hardware interface written in zig
license: ""
author: eggyengine
author_github: eggyengine
repository: https://github.com/eggyengine/vitellus
keywords:
  - graphics
  - graphics-library
date: 2026-10-24
category: game-development
updated_at: 2026-10-24T11:16:43+00:00
last_sync: 2026-10-24T11:16:43Z
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
permalink: /packages/eggyengine/vitellus/
---

# vitellus

vitellus is a native-first rendering hardware interface written in Zig for building game engines and renderers on modern graphics APIs.

guides and API reference: https://eggyengine.github.io/vitellus/

> [!NOTE]
> **Needed**: Metal developers or really anyone with a mac should consider contributing to this

## add to project
requires zig `0.16.0`

to use this with the zig build system, import as so:
```bash
zig fetch --save git+https://github.com/eggyengine/vitellus#0.16.0
```

and then in `build.zig`:
```zig
const vit = b.dependency("vitellus", .{
    .target = target,
    .optimize = optimize,

    .enable_dxc = true, // default is false; adds the vitellus_dxc module
    .enable_spirv_cross = true, // default is false
    .enable_slang = true, // default is false; adds the vitellus_slangc module
});

exe.root_module.addImport("vitellus", vit.module("vitellus"));
exe.root_module.addImport("vitellus_spirv", vit.module("vitellus_spirv")); // or vitellus_dxc, vitellus_slangc
@import("vitellus").installLibraries(b, vit); // ships DXC and Slang beside your app
```

and lastly in your library/executable:
```zig
const vit = @import("vitellus");
```
