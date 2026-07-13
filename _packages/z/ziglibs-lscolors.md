---
title: lscolors
description: A zig library for colorizing paths according to LS_COLORS
license: MIT
author: ziglibs
author_github: ziglibs
repository: https://github.com/ziglibs/lscolors
keywords:
  - ls-colors
date: 2026-07-04
updated_at: 2026-07-04T13:23:11+00:00
last_sync: 2026-07-04T13:23:11Z
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
permalink: /packages/ziglibs/lscolors/
---

# lscolors

![CI](https://github.com/ziglibs/zig-lscolors/workflows/CI/badge.svg)

A zig library for colorizing paths according to the `LS_COLORS`
environment variable. Designed to work with Zig 0.16.0.

## Quick Example

```zig
const std = @import("std");

const LsColors = @import("lscolors").LsColors;

pub fn main(init: std.process.Init) !void {
    const allocator = init.arena.allocator();
    const io = init.io;

    var lsc = try LsColors.fromEnv(allocator, init.environ_map);
    defer lsc.deinit();

    var dir = try std.Io.Dir.cwd().openDir(io, ".", .{ .iterate = true });
    defer dir.close(io);

    var iterator = dir.iterate();
    while (try iterator.next(io)) |itm| {
        std.log.info("{f}", .{try lsc.styled(io, itm.name)});
    }
}
```
