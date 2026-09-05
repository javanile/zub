---
title: zig-sdl3webgpu
description: sdl3webgpu for zig
license: Zlib
author: akunaakwei
author_github: akunaakwei
repository: https://github.com/akunaakwei/zig-sdl3webgpu
keywords:
date: 2026-09-05
updated_at: 2026-09-05T07:36:42+00:00
last_sync: 2026-09-05T07:36:42Z
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
permalink: /packages/akunaakwei/zig-sdl3webgpu/
---

# sdl3webgpu
This is [sdl3webgpu](https://github.com/eliemichel/sdl3webgpu) for the zig build system.

# Usage
You need to bring your own headers and library for SDL 3 and a WebGPU implementation (dawn for example).  
```zig
pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const sdl3_dep = b.dependency("sdl", .{
        .target = target,
        .optimize = optimize,
    });
    const sdl3_lib = sdl3_dep.artifact("sdl3");

    const dawn_dep = b.dependency("dawn", .{
        .target = target,
        .optimize = optimize,
    });
    const webgpu_lib = dawn_dep.artifact("webgpu_dawn");

    const sdl3webgpu_dep = b.dependency("sdl3webgpu", .{
        .target = target,
        .optimize = optimize,
    });
    const sdl3webgpu_lib = sdl3webgpu_dep.artifact("sdl3webgpu");
    sdl3webgpu_lib.root_module.linkLibrary(sdl3_lib);
    sdl3webgpu_lib.root_module.linkLibrary(webgpu_lib);

    // ...
}
```

# Example
Check out [sdl3 dawn example](https://github.com/akunaakwei/zig-sdl3-dawn-example) for a fully functional example.
