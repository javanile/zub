---
title: humpty
description: A physics engine written in Zig
license: ""
author: eggyengine
author_github: eggyengine
repository: https://github.com/eggyengine/humpty
keywords:
date: 2026-10-15
updated_at: 2026-10-15T05:56:10+00:00
last_sync: 2026-10-15T05:56:10Z
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
permalink: /packages/eggyengine/humpty/
---

# humpty

*humpty* is a physics library written in Zig and for the eggy engine project. 

## add to project
requires zig `0.16.0` (have not tested for other zig versions, however likely works fine. please open a PR to reduce down the minimum version). 

to use this with the zig build system, import as so:
```bash
zig fetch --save git+https://github.com/eggyengine/humpty
```

and then in `build.zig`:
```zig
const humpty = b.dependency("humpty", .{
    .target = target,
    .optimize = optimize,
});

exe.root_module.addImport("humpty", humpty.module("humpty"));
```

and lastly in your library/executable:
```zig
const humpty = @import("humpty");
```
