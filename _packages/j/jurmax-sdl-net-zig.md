---
title: SDL_net_zig
description: A port of SDL_net to the Zig build system
license: MIT
author: JurMax
author_github: JurMax
repository: https://github.com/JurMax/SDL_net_zig
keywords:
  - sdl
  - sdl3
date: 2026-07-03
category: game-development
updated_at: 2026-07-03T06:05:46+00:00
last_sync: 2026-07-03T06:05:46Z
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
permalink: /packages/JurMax/SDL_net_zig/
---

# SDL_net_zig

This is a port of [SDL3_net](https://github.com/libsdl-org/SDL_net) to the [Zig](https://ziglang.org/) build system. It does not provide any Zig bindings.

## How to use it

### As a library

First, fetch this repository:

```sh
zig fetch --save git+https://github.com/JurMax/SDL_net_zig
```

Next, add it to your `build.zig`:

```zig
const sdl_net_dependency = b.dependency("sdl_net", .{
    .target = target,
    .optimize = optimize,
    .build_sdl = false, // Set to true to also build SDL3 itself.
});
exe.root_module.linkLibrary(sdl_net_dependency.artifact("SDL3_net"));
```

This will add the SDL_net library and header to `exe`.

### Running the examples

You can run the SDL_net examples by running any of the following commands.

```sh
zig build voipchat
zig build simple-http-get
zig build resolve-hostnames
zig build get-local-addrs
zig build echo-server
```
