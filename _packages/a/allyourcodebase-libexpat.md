---
title: libexpat
description: libexpat ported to the zig build system
license: MIT
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/libexpat
keywords:
date: 2026-04-16
updated_at: 2026-04-16T22:54:37+00:00
last_sync: 2026-04-16T22:54:37Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 4
distributable_binary_count: 4
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/allyourcodebase/libexpat/
---

[![CI](https://github.com/allyourcodebase/libexpat/actions/workflows/ci.yaml/badge.svg)](https://github.com/allyourcodebase/libexpat/actions)

# Expat

This is [Expat](https://github.com/libexpat/libexpat), packaged for [Zig](https://ziglang.org/).

## Installation

First, update your `build.zig.zon`:

```
# Initialize a `zig build` project if you haven't already
zig init
zig fetch --save git+https://github.com/allyourcodebase/libexpat.git#2.7.1-3
```

You can then import `expat` in your `build.zig` with:

```zig
const expat_dependency = b.dependency("expat", .{
    .target = target,
    .optimize = optimize,
});
your_exe.linkLibrary(expat_dependency.artifact("expat"));
```
