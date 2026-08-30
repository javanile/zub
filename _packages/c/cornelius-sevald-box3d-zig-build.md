---
title: box3d-zig-build
description: Box3D physics engine packaged for the Zig build system
license: MIT
author: cornelius-sevald
author_github: cornelius-sevald
repository: https://github.com/cornelius-sevald/box3d-zig-build
keywords:
  - box2d
date: 2026-08-18
updated_at: 2026-08-18T12:34:05+00:00
last_sync: 2026-08-18T12:34:05Z
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
permalink: /packages/cornelius-sevald/box3d-zig-build/
---

# Box3D

This is the [Box3D](https://box2d.org/documentation3d/) physics engine packaged for the Zig build system.

## Usage

Add the dependency to your build.zig.zon:

```shell
zig fetch --save git+https://github.com/cornelius-sevald/box3d.git
```

Use the dependency in your build.zig:

```zig
pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const box3d = b.dependency("box3d", .{
        .target = target,
        .optimize = optimize,
    });
    const box3d_lib = box3d.artifact("box3d");

    const exe = b.addExecutable(.{
        // ...
    });
    exe.root_module.addIncludePath(box3d.path("."));
    exe.root_module.linkLibrary(box3d_lib);

    // ...
}
```

Import and use the C library:

```zig
const c = @cImport({
    @cInclude("box3d/box3d.h");
});

pub fn main() void {
    var worldDef = c.b3DefaultWorldDef();
    const worldId = c.b3CreateWorld(&worldDef);
    defer c.b3DestroyWorld(worldId);
    // ...
}
```

## Examples

This build script can also run the official examples. From this repository run:

```shell
zig build -Dtest run
```

Note that this requires you to have OpenGL, X11 and GTK3 installed on your system.

## Acknowledgements

Thanks to Erin Catto for making Box3D, and thanks to Stevie Hryciw for packaging [Box2D](https://github.com/allyourcodebase/box2d) for AYC.
