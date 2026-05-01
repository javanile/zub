---
title: zstd
description: zstd ported to the zig build system
license: MIT
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/zstd
keywords:
date: 2026-04-22
updated_at: 2026-04-22T16:32:55+00:00
last_sync: 2026-04-22T16:32:55Z
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
permalink: /packages/allyourcodebase/zstd/
---

[![CI](https://github.com/allyourcodebase/zstd/actions/workflows/ci.yaml/badge.svg)](https://github.com/allyourcodebase/zstd/actions)

# zstd

This is [zstd](https://github.com/facebook/zstd), packaged for [Zig](https://ziglang.org/).

## Installation

First, update your `build.zig.zon`:

```
# Initialize a `zig build` project if you haven't already
zig init
zig fetch --save git+https://github.com/allyourcodebase/zstd.git#1.5.7-1
```

You can then import `zstd` in your `build.zig` with:

```zig
const zstd_dependency = b.dependency("zstd", .{
    .target = target,
    .optimize = optimize,
});
your_exe.linkLibrary(zstd_dependency.artifact("zstd"));
```
