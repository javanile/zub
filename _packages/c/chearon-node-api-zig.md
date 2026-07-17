---
title: node-api-zig
description: zig build instead of node-gyp
license: ""
author: chearon
author_github: chearon
repository: https://github.com/chearon/node-api-zig
keywords:
  - n-api
  - node-addon-api
  - node-gyp
date: 2026-07-10
updated_at: 2026-07-10T04:00:37+00:00
last_sync: 2026-07-10T04:00:37Z
package_kind: binary
has_library: false
has_binary: true
has_distributable_binary: true
binary_count: 1
distributable_binary_count: 1
multiple_binaries: false
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/chearon/node-api-zig/
---

# node-api-zig

Easily cross-compile a native nodejs C++ addon using Zig's build system. This exposes both the low-level [N-API](https://nodejs.org/api/n-api.html) and [node-addon-api](https://github.com/nodejs/node-addon-api).

On Unixes, building an addon is as simple as including the headers and telling the linker to leave those symbols undefined. On Windows, an import library has to be generated from the .def files included with the [N-API headers](https://github.com/nodejs/node-api-headers). This project hides almost all of that complexity behind `lib.addObject(node_api)`, where `node_api` is this dependency's artifact, and `lib` is your library.

See the `example` directory for a full working example.

```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
  const target = b.standardTargetOptions(.{});
  const optimize = b.standardOptimizeOption(.{});
  const node_api = b.dependency("node_api", .{
    .target = target,
    .optimize = optimize,
  }).artifact("node_api");

  const lib = b.addLibrary(.{
    .name = "example_callbacks",
    .linkage = .dynamic,
    .root_module = b.createModule(.{
      .target = target,
      .optimize = optimize,
    })
  });

  // this tells the Unixes to allow napi_ functions to be unresolved
  lib.linker_allow_shlib_undefined = true;

  // add your sources/flags here
  lib.addCSourceFiles(.{
    .files = &.{"addon.cc"},
    .flags = &.{}
  });

  // makes node-addon-api (C++) and n-api (C) headers available
  // on Windows, this links to import libraries
  // on Unixes, it links to an empty object file
  lib.addObject(node_api);

  lib.linkLibCpp();

  // name/move the addon to a place addon.js loads it from
  const move = b.addInstallFile(lib.getEmittedBin(), "../addon.node");
  move.step.dependOn(&lib.step);
  b.getInstallStep().dependOn(&move.step);
}
```
