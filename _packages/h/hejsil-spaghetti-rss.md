---
title: spaghetti-rss
description: A dependency-free RSS parser for Zig
license: MIT
author: Hejsil
author_github: Hejsil
repository: https://github.com/Hejsil/spaghetti-rss
keywords:
  - feed
  - parser
  - rss
  - rss-parser
  - xml
date: 2026-08-07
category: data-formats
updated_at: 2026-08-07T13:39:34+00:00
last_sync: 2026-08-07T13:39:34Z
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
permalink: /packages/Hejsil/spaghetti-rss/
---

# spaghetti-rss

A dependency-free RSS and Atom parser for Zig

## Example

```zig
const std = @import("std");
const rss = @import("spaghetti_rss");

pub fn main(init: std.process.Init) !void {
    var args = std.process.Args.iterate(init.minimal.args);
    _ = args.next(); // skip the program name

    while (args.next()) |path| {
        const source = try std.Io.Dir.cwd().readFileAlloc(init.io, path, init.gpa, .unlimited);
        defer init.gpa.free(source);

        var feed = try rss.parse(init.gpa, source);
        defer feed.deinit(init.gpa);

        std.debug.print("{s}: {d} items\n", .{ feed.title(), feed.itemCount() });
        for (0..feed.itemCount()) |i| {
            if (feed.itemTitle(i)) |title| std.debug.print("  {s}\n", .{title});
        }
    }
}
```
