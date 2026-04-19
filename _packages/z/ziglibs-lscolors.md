---
title: lscolors
description: A zig library for colorizing paths according to LS_COLORS
license: MIT
author: ziglibs
author_github: ziglibs
repository: https://github.com/ziglibs/lscolors
keywords:
  - ls-colors
date: 2026-04-10
updated_at: 2026-04-10T14:52:37+00:00
last_sync: 2026-04-10T14:52:37Z
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
environment variable. Designed to work with Zig 0.15.2.

## Quick Example

```zig
const std = @import("std");

const LsColors = @import("lscolors").LsColors;

pub fn main() !void {
    var gpa: std.heap.DebugAllocator(.{}) = .init;
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var lsc = try LsColors.fromEnv(allocator);
    defer lsc.deinit();

    var dir = try std.fs.cwd().openDir(".", .{ .iterate = true });
    defer dir.close();

    var iterator = dir.iterate();
    while (try iterator.next()) |itm| {
        std.log.info("{}", .{try lsc.styled(itm.name)});
    }
}
```
