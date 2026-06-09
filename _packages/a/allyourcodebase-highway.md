---
title: highway
description: Google Highway built with the Zig build system
license: MIT
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/highway
keywords:
date: 2026-06-02
updated_at: 2026-06-02T10:00:37+00:00
last_sync: 2026-06-02T10:00:37Z
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
permalink: /packages/allyourcodebase/highway/
---

# Google Highway

This is [Google Highway](https://github.com/google/highway), packaged for
[Zig](https://ziglang.org/).

**Does not yet include `libhwy_contrib`.**

## How to use it

First, update your `build.zig.zon`:

```
zig fetch --save git+https://github.com/allyourcodebase/highway
```

Next, in `build.zig`, declare the dependency and link with the static library:

```zig
const highway_dep = b.dependency("highway", .{
    .target = target,
    .optimize = optimize,
});

// ...
exe.linkLibrary(highway_dep.artifact("hwy"));
```
