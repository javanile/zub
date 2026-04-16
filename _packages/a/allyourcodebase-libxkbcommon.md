---
title: libxkbcommon
description: libxkbcommon ported to the zig build system
license: MIT
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/libxkbcommon
keywords:
date: 2026-04-13
updated_at: 2026-04-13T19:48:45+00:00
last_sync: 2026-04-13T19:48:45Z
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
permalink: /packages/allyourcodebase/libxkbcommon/
---

[![CI](https://github.com/allyourcodebase/libxkbcommon/actions/workflows/ci.yaml/badge.svg)](https://github.com/allyourcodebase/libxkbcommon/actions)

# libxkbcommon

This is [libxkbcommon](https://github.com/xkbcommon/libxkbcommon), packaged for [Zig](https://ziglang.org/).

## Installation

First, update your `build.zig.zon`:

```
# Initialize a `zig build` project if you haven't already
zig init
zig fetch --save git+https://github.com/allyourcodebase/libxkbcommon.git#1.13.1
```

You can then import `libxkbcommon` in your `build.zig` with:

```zig
const libxkbcommon_dependency = b.dependency("libxkbcommon", .{
    .target = target,
    .optimize = optimize,

    // Set the XKB config root.
    // Will default to "${INSTALL_PREFIX}/share/X11/xkb" i.e. `zig-out/share/X11/xkb`.
    // Most distributions will use `/usr/share/X11/xkb`.
    //
    // The value `""` will not set a default config root directory.
    // To configure the config root at runtime, use the "XKB_CONFIG_ROOT" environment variable.
    //
    // This example will assume that the config root of the host system is in `/usr`.
    // This does not work on distributions that don't follow the Filesystem Hierarchy Standard (FHS) like NixOS.
    .@"xkb-config-root" = "/usr/share/X11/xkb",
    .@"xkb-legacy-root" = "/usr/share/X11/xkb", // Legacy X11 config root

    // The X locale root.
    // Will default to "${INSTALL_PREFIX}/share/X11/locale" i.e. `zig-out/share/X11/locale`.
    // Most distributions will use `/usr/share/X11/locale`.
    //
    // To configure the config root at runtime, use the "XLOCALEDIR" environment variable.
    //
    // This example will assume that the config root of the host system is in `/usr`.
    // This does not work on distributions that don't follow the Filesystem Hierarchy Standard (FHS) like NixOS.
    .@"x-locale-root" = "/usr/share/X11/locale",
});
your_exe.linkLibrary(libxkbcommon_dependency.artifact("libxkbcommon"));
```

For more information, please refer to the [User-configuration](https://github.com/xkbcommon/libxkbcommon/blob/master/doc/user-configuration.md) docs of libxkbcommon.
