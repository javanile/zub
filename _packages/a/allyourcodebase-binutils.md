---
title: binutils
description: binutils ported to the zig build system
license: GPL-2.0
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/binutils
keywords:
date: 2026-04-16
updated_at: 2026-04-16T22:27:13+00:00
last_sync: 2026-04-16T22:27:13Z
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
permalink: /packages/allyourcodebase/binutils/
---

[![CI](https://github.com/allyourcodebase/binutils/actions/workflows/ci.yaml/badge.svg)](https://github.com/allyourcodebase/binutils/actions)

# binutils

This is [binutils](https://www.gnu.org/software/binutils/), packaged for [Zig](https://ziglang.org/).

The following subset of tools and libraries have been ported:

- `bfd` - A library for manipulating binary files in a variety of different formats.
- `libsframe` - A library for assembling and disassembling a variety of different assembler languages.
- `opcodes` - A library for manipulating the SFRAME debug format.

## Installation

First, update your `build.zig.zon`:

```
# Initialize a `zig build` project if you haven't already
zig init
zig fetch --save git+https://github.com/allyourcodebase/binutils.git
```

You can then import `binutils` in your `build.zig` with:

```zig
const binutils_dependency = b.dependency("binutils", .{
    .target = target,
    .optimize = optimize,
});
your_exe.root_module.linkLibrary(binutils_dependency.artifact("binutils"));
```
