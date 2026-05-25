---
title: raylib-bar_chart
description: Bar chart widget for Raylib-zig.
license: MIT
author: RomaricKc1
author_github: RomaricKc1
repository: https://github.com/RomaricKc1/raylib-bar_chart
keywords:
  - raylib-zig
date: 2026-05-25
updated_at: 2026-05-25T12:08:01+00:00
last_sync: 2026-05-25T12:08:01Z
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
permalink: /packages/RomaricKc1/raylib-bar_chart/
---

# Raylib Bar chart lib

Bar chart widget for [Raylib-zig](https://github.com/Not-Nik/raylib-zig).

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
zig fetch --save git+https://github.com/RomaricKc1/raylib-bar_chart/
```

And add these lines to your `build.zig` file:

```zig
const rl_bar_chart_dep = b.dependency("raylib_bar_chart", .{
    .target = target,
    .optimize = optimize,
});
const rl_bar_chart = rl_bar_chart_dep.module("raylib_bar_chart"); // bar chart widget
```

Now add the modules to your target:

```zig
exe.root_module.addImport("rl_bar_chart", rl_bar_chart);
```

You can then import it in your code.

```zig
const rl_bar_chart = @import("rl_bar_chart");
```

## Checkout another widget

- [Raylib-lists](https://github.com/RomaricKc1/raylib-lists)
