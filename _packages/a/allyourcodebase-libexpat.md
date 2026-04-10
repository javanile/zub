---
title: libexpat
description: libexpat ported to the zig build system
license: MIT
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/libexpat
keywords:
date: 2026-04-09
last_sync: 2026-04-09T10:49:59Z
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
zig fetch --save git+https://github.com/allyourcodebase/libexpat.git#2.7.1-2
```

You can then import `expat` in your `build.zig` with:

```zig
const expat_dependency = b.dependency("expat", .{
    .target = target,
    .optimize = optimize,
});
your_exe.linkLibrary(expat_dependency.artifact("expat"));
```
