---
title: vitellus
description: Native-first render hardware interface written in zig
license: ""
author: eggyengine
author_github: eggyengine
repository: https://github.com/eggyengine/vitellus
keywords:
date: 2026-07-30
updated_at: 2026-07-30T04:28:33+00:00
last_sync: 2026-07-30T04:28:33Z
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
permalink: /packages/eggyengine/vitellus/
---

# vitellus

vitellus is a native-first rendering hardware interface written in Zig for building game engines and renderers on modern graphics APIs.

## add to project
requires zig `0.16.0`

to use this with the zig build system, import as so:
```bash
zig fetch --save git+https://github.com/eggyengine/vitellus
```

and then in `build.zig`:
```zig
const vit = b.dependency("vitellus", .{
    .target = target,
    .optimize = optimize,

    .enable_dxc = true, // default is false
    .enable_spirv-cross = true, // default is false
});

exe.root_module.addImport("vitellus", vit.module("vitellus"));
```

and lastly in your library/executable:
```zig
const vit = @import("vitellus");
```

## documentation

~~there is a tutorial available in [docs/tutorial](docs/tutorial/README.md) that might be worth checking out~~
