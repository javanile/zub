---
title: vitellus
description: Native-first render hardware interface written in zig
license: ""
author: eggyengine
author_github: eggyengine
repository: https://github.com/eggyengine/vitellus
keywords:
date: 2026-07-21
updated_at: 2026-07-21T07:22:38+00:00
last_sync: 2026-07-21T07:22:38Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 3
distributable_binary_count: 3
multiple_binaries: true
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
});

exe.root_module.addImport("vitellus", vit.module("vitellus"));
```

```zig
const vit = b.dependency("vitellus", .{
    .target = target,
    .optimize = optimize,
});
```

and lastly in your library/executable:
```zig
const vit = @import("vitellus");
```

## documentation

~~there is a tutorial available in [docs/tutorial](docs/tutorial/README.md) that might be worth checking out~~
