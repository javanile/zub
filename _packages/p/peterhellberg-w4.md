---
title: w4
description: A small Zig module, primarily meant for my own experiments with WASM-4
license: MIT
author: peterhellberg
author_github: peterhellberg
repository: https://github.com/peterhellberg/w4
keywords:
  - wasm4
date: 2026-06-03
updated_at: 2026-06-03T19:38:22+00:00
last_sync: 2026-06-03T19:38:22Z
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
permalink: /packages/peterhellberg/w4/
---

# w4 :zap:

A small [Zig](https://ziglang.org/) ⚡ module, primarily meant for my own experiments with [WASM-4](https://wasm4.org/) 🎮

Based on the [wasm4.zig template](https://github.com/aduros/wasm4/blob/main/cli/assets/templates/zig/src/wasm4.zig)

> [!IMPORTANT]
> You might want to install the [w4-init](https://github.com/peterhellberg/w4-init) tool and use that instead of manually creating the files for your cart.

## Usage

You can have `zig build` retrieve the `w4` module if you specify it as a dependency.

### Create a `build.zig.zon` that looks something like this:
```zig
.{
    .name = .w4_game,
    .fingerprint = 0x9364c2ea98294635,
    .version = "0.0.0",
    .paths = .{""},
    .dependencies = .{
        .w4 = .{
            .url = "https://github.com/peterhellberg/w4/archive/refs/tags/v0.1.4.tar.gz",
        },
    },
}
```

> [!NOTE]
> If you leave out the hash then `zig build` will tell you that it is missing the hash, and what it is.
> Another way to get the hash is to use `zig fetch`, this is probably how you _should_ do it :)

### Then you can add the module in your `build.zig` like this:
```zig
// Add the w4 module to the executable
exe.addModule("w4", b.dependency("w4", .{}).module("w4"));
```

### In your `src/main.zig` you should now be able to:
```zig
const w4 = @import("w4");

export fn start() void {}

export fn update() void {
    const hello = "Hello from Zig!";

    w4.color(2);
    w4.text(hello, 15, 11);
    w4.color(3);
    w4.text(hello, 16, 10);
}
```
