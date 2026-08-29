---
title: libevdev
description: libevdev ported to the zig build system
license: MIT
author: krish-r
author_github: krish-r
repository: https://github.com/krish-r/libevdev
keywords:
date: 2026-08-29
updated_at: 2026-08-29T07:53:00+00:00
last_sync: 2026-08-29T07:53:00Z
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
permalink: /packages/krish-r/libevdev/
---

# libevdev

This is [libevdev](https://www.freedesktop.org/software/libevdev/doc/latest/), packaged for [Zig](https://ziglang.org/).

**NOTE**: This repository includes only basic build functionality (still a WIP, not thoroughly tested yet).

## Dependencies

* Python3

## Usage

* Update your `build.zig.zon`:

```
zig fetch --save git+https://github.com/krish-r/libevdev.git
```

* Add the following snippet to your `build.zig` script:

```zig
const dep_optimize = b.option(std.builtin.OptimizeMode, "dep-optimize", "optimization mode") orelse .ReleaseFast;

const libevdev = b.dependency("libevdev", .{
    .target = target,
    .optimize = dep_optimize,
});
your_compilation.linkLibrary(libevdev.artifact("evdev"));
```

This will provide libevdev as a shared library to `your_compilation`.


## Credits

- [libevdev](https://gitlab.freedesktop.org/libevdev/libevdev)
- [All Your Codebase](https://github.com/allyourcodebase)
- [Ziggit](https://ziggit.dev)
