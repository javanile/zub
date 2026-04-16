---
title: zlib
description: zlib ported to the zig build system
license: MIT
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/zlib
keywords:
date: 2026-04-13
updated_at: 2026-04-13T23:01:07+00:00
last_sync: 2026-04-13T23:01:07Z
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
permalink: /packages/allyourcodebase/zlib/
---

# zlib

This is [zlib](https://www.zlib.net/),
packaged for [Zig](https://ziglang.org/).

## How to use it

First, update your `build.zig.zon`:

```
zig fetch --save https://github.com/allyourcodebase/zlib/archive/refs/tags/1.3.1.tar.gz
```

Next, add this snippet to your `build.zig` script:

```zig
const zlib_dep = b.dependency("zlib", .{
    .target = target,
    .optimize = optimize,
});
your_compilation.linkLibrary(zlib_dep.artifact("z"));
```

This will provide zlib as a static library to `your_compilation`.
