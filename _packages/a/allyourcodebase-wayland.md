---
title: wayland
description: wayland ported to the zig build system
license: MIT
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/wayland
keywords:
date: 2026-04-16
updated_at: 2026-04-16T23:15:28+00:00
last_sync: 2026-04-16T23:15:28Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 2
distributable_binary_count: 2
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/allyourcodebase/wayland/
---

[![CI](https://github.com/allyourcodebase/wayland/actions/workflows/ci.yaml/badge.svg)](https://github.com/allyourcodebase/wayland/actions)

# Wayland

This is [Wayland](https://gitlab.freedesktop.org/wayland/wayland), packaged for [Zig](https://ziglang.org/).

## Installation

First, update your `build.zig.zon`:

```
# Initialize a `zig build` project if you haven't already
zig init
zig fetch --save git+https://github.com/allyourcodebase/wayland.git#1.24.0-4
```

You can then import `wayland` in your `build.zig` with:

```zig
const wayland = b.dependency("wayland", .{
    .target = target,
    .optimize = optimize,
});
const wayland_server = wayland.artifact("wayland-server");
const wayland_client = wayland.artifact("wayland-client");
const wayland_egl = wayland.artifact("wayland-egl");
const wayland_cursor = wayland.artifact("wayland-cursor");

// Makes sure we get `wayland-scanner` for the host platform even when cross-compiling
const wayland_host = b.dependency("wayland", .{
    .target = b.graph.host,
    .optimize = std.builtin.OptimizeMode.Debug,
});
const wayland_scanner = wayland_host.artifact("wayland-scanner");
```
