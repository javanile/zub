---
title: elfutils
description: elfutils ported to the zig build system
license: GPL-3.0
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/elfutils
keywords:
date: 2026-04-18
updated_at: 2026-04-18T19:43:22+00:00
last_sync: 2026-04-18T19:43:22Z
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
permalink: /packages/allyourcodebase/elfutils/
---

[![CI](https://github.com/allyourcodebase/elfutils/actions/workflows/ci.yaml/badge.svg)](https://github.com/allyourcodebase/elfutils/actions)

# elfutils

This is [elfutils](https://sourceware.org/elfutils/), packaged for [Zig](https://ziglang.org/).

## Installation

First, update your `build.zig.zon`:

```
# Initialize a `zig build` project if you haven't already
zig init
zig fetch --save git+https://github.com/allyourcodebase/elfutils.git
```

You can then import `elfutils` in your `build.zig` with:

```zig
const elfutils_dependency = b.dependency("elfutils", .{
    .target = target,
    .optimize = optimize,
});
const libelf = elfutils_dependency.artifact("elf");
const libdw = elfutils_dependency.artifact("dw");
const libasm = elfutils_dependency.artifact("asm");

your_exe.linkLibrary(libelf);
your_exe.linkLibrary(libdw);
your_exe.linkLibrary(libasm);
```
