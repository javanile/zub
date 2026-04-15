---
title: zig-sdl3webgpu
description: sdl3webgpu for zig
license: Zlib
author: akunaakwei
author_github: akunaakwei
repository: https://github.com/akunaakwei/zig-sdl3webgpu
keywords:
date: 2026-04-15
updated_at: 2026-04-15T07:14:48+00:00
last_sync: 2026-04-15T07:14:48Z
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
        .sdl3_headers = sdl3_lib.getEmittedIncludeTree(),
        .sdl3_library = sdl3_lib.getEmittedBin(),
        .webgpu_headers = webgpu_lib.getEmittedIncludeTree(),
        .webgpu_library = webgpu_lib.getEmittedBin(),
    });

    const exe = b.addExecutable(.{
        .name = "example",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target = target,
            .optimize = optimize,
        }),
    });
    exe.root_module.addImport("sdl3", sdl3_mod);
    exe.root_module.addImport("webgpu", webgpu_mod);
    exe.root_module.addImport("sdl3webgpu", sdl3webgpu_mod);
}
```

# Example
Check out [sdl3 dawn example](https://github.com/akunaakwei/zig-sdl3-dawn-example) for a fully functional example.
