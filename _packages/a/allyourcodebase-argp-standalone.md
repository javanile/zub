---
title: argp-standalone
description: argp-standalone ported to the zig build system
license: LGPL-2.1
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/argp-standalone
keywords:
date: 2026-10-14
updated_at: 2026-10-14T21:20:58+00:00
last_sync: 2026-10-14T21:20:58Z
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
permalink: /packages/allyourcodebase/argp-standalone/
---

[![CI](https://github.com/allyourcodebase/argp-standalone/actions/workflows/ci.yaml/badge.svg)](https://github.com/allyourcodebase/argp-standalone/actions)

# argp-standalone

This is [argp-standalone](https://github.com/argp-standalone/argp-standalone), packaged for [Zig](https://ziglang.org/).

## Installation

First, update your `build.zig.zon`:

```
# Initialize a `zig build` project if you haven't already
zig init
zig fetch --save git+https://github.com/allyourcodebase/argp-standalone.git
```

You can then import `argp_standalone` in your `build.zig` with:

```zig
const argp_dependency = b.dependency("argp_standalone", .{
    .target = target,
    .optimize = optimize,
});
your_exe.root_module.linkLibrary(argp_dependency.artifact("argp"));
```
