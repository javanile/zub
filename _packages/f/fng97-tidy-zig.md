---
title: tidy.zig
description: "Code tidiness checks based on TigerBeetle's tidy script"
license: MIT
author: fng97
author_github: fng97
repository: https://github.com/fng97/tidy.zig
keywords:
date: 2026-04-19
updated_at: 2026-04-19T16:31:37+00:00
last_sync: 2026-04-19T16:31:37Z
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
permalink: /packages/fng97/tidy.zig/
---

# `tidy.zig`

> [!NOTE]
> This is a work in progress.

Code tidiness checks based on [TigerBeetle](https://tigerbeetle.com)'s
[`tidy.zig`][tigerbeetle-tidy], simplified and parameterised for reuse across projects. See
[Matklad's notes on tidy scripts][matklad-notes].

## Checks

- line length
- leftover FIXMEs
- leftover `dbg()` calls
- large git blobs

## Usage

Drop `tidy.zig` in your project or add this project as a dependency:

```
zig fetch --save git+https://github.com/fng97/tidy.zig
```

Then wire it up in `build.zig`:

```zig
const test_step = b.step("test", "Run tests");
// Optionally pass options here. See `build.zig` for the available options and their defaults.
const tidy_dep = b.dependency("tidy", .{
    .target = b.graph.host,
    .optimize = .ReleaseSafe,
    // Bump max line length to 120 from default of 100.
    .line_column_max = 120,
});
test_step.dependOn(blk: {
    const exe = b.addTest(.{ .name = "tidy_checks", .root_module = tidy_dep.module("tidy") });
    const run = b.addRunArtifact(exe);
    break :blk &run.step;
});
```

## Attribution

TigerBeetle is licensed under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). See
[`src/NOTICE_TIGERBEETLE`](src/NOTICE_TIGERBEETLE).

[tigerbeetle-tidy]: https://github.com/tigerbeetle/tigerbeetle/blob/main/src/tidy.zig
[matklad-notes]: https://matklad.github.io/2025/12/06/mechanical-habits.html#Tidy-Script
