---
title: raylib-lists
description: List widget for Raylib-zig.
license: MIT
author: RomaricKc1
author_github: RomaricKc1
repository: https://github.com/RomaricKc1/raylib-lists
keywords:
  - raylib-zig
date: 2026-05-25
updated_at: 2026-05-25T12:01:10+00:00
last_sync: 2026-05-25T12:01:10Z
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
permalink: /packages/RomaricKc1/raylib-lists/
---

# Raylib List widget lib

List widget for [Raylib-zig](https://github.com/Not-Nik/raylib-zig).

Example usage here -> [ZISTORY](https://github.com/RomaricKc1/zistory).

Tested on Zig version `0.16.0`.

> [!NOTE]
> This is configured to work on `wayland`. If you are on `x11`, you'll need to
> change the display `backend`.

In the raylib dependency.

```zig
const raylib_dep = b.dependency("raylib_zig", .{
    .target = target,
    .optimize = optimize,
    .linux_display_backend = .X11,
});
```

## Usage

The project must have been created using `zig init`.

Run this to add it to your `build.zig.zon`:

```
zig fetch --save git+https://github.com/RomaricKc1/raylib-lists/
```

And add these lines to your `build.zig` file:

```zig
const rl_lists_dep = b.dependency("raylib_lists", .{
    .target = target,
    .optimize = optimize,
});
const rl_lists = rl_lists_dep.module("raylib_lists"); // lists widget
```

Now add the modules to your target:

```zig
exe.root_module.addImport("rl_lists", rl_lists);
```

You can then import it in your code.

```zig
const rl_lists = @import("rl_lists");
```

## Checkout another widget

- [Raylib-bar_chart](https://github.com/RomaricKc1/raylib-bar_chart)
