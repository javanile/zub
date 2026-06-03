---
title: libxml2
description: libxml2 ported to the zig build system
license: MIT
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/libxml2
keywords:
date: 2026-05-30
updated_at: 2026-05-30T16:33:27+00:00
last_sync: 2026-05-30T16:33:27Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 2
distributable_binary_count: 1
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/allyourcodebase/libxml2/
---

[![CI](https://github.com/allyourcodebase/libxml2/actions/workflows/ci.yaml/badge.svg)](https://github.com/allyourcodebase/libxml2/actions)

# libxml2

This is [libxml2](https://gitlab.gnome.org/GNOME/libxml2), packaged for [Zig](https://ziglang.org/).

## Installation

First, update your `build.zig.zon`:

```
# Initialize a `zig build` project if you haven't already
zig init
zig fetch --save git+https://github.com/allyourcodebase/libxml2.git#2.15.1-2
```

You can then import `libxml2` in your `build.zig` with:

```zig
const libxml2_dependency = b.dependency("libxml2", .{
    .target = target,
    .optimize = optimize,

    // libxml2 will try to link to iconv on macOS by default which will
    // fail when cross-compiling. You may disable iconv support for or
    // link against GNU libiconv which is licensed under LGPL.

    // disable iconv support on all targets
    // .iconv = false,

    // disable iconv support when compiling to macOS
    // .iconv = !target.result.os.tag.isDarwin(),

    // disable iconv support when cross-compiling to macOS
    // .iconv = !(target.query.isNativeOs() and target.result.os.tag.isDarwin()),

    // Use GNU libiconv on macOS which is licensed under LGPL.
    // .@"iconv-impl" = @as(?enum{libc, libiconv, win_iconv}, if (target.result.os.tag.isDarwin()) .libiconv else null),
});
your_exe.linkLibrary(libxml2_dependency.artifact("xml"));
```
