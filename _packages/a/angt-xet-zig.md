---
title: xet.zig
description: A Zig implementation of the Xet content-addressed storage protocol
license: MIT
author: angt
author_github: angt
repository: https://github.com/angt/xet.zig
keywords:
  - xet
date: 2026-11-22
updated_at: 2026-11-22T20:39:31+00:00
last_sync: 2026-11-22T20:39:31Z
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
permalink: /packages/angt/xet.zig/
---

# xet.zig

A Zig implementation of the Xet content-addressed storage protocol.

## Example

```zig
const std = @import("std");
const xet = @import("xet");

pub fn roundTrip(
    allocator: std.mem.Allocator,
    io: std.Io,
    cas_url: []const u8,
    cas_token: []const u8,
) !void {
    var cas = try xet.http.Client.init(allocator, io, cas_url, cas_token);
    defer cas.deinit();

    const uploaded = try cas.upload(allocator, "Hello, Xet!", .{});

    // Downloads the complete file, verifies it, and returns caller-owned bytes
    const downloaded = try cas.download(allocator, uploaded.file_hash);
    defer allocator.free(downloaded);
}
```
