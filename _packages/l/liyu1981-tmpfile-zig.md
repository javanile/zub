---
title: tmpfile.zig
description: a convenient util to use tmp files with zig
license: ""
author: liyu1981
author_github: liyu1981
repository: https://github.com/liyu1981/tmpfile.zig
keywords:
date: 2026-09-08
updated_at: 2026-09-08T21:23:13+00:00
last_sync: 2026-09-08T21:23:13Z
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
permalink: /packages/liyu1981/tmpfile.zig/
---

# tmpfile.zig

## why

So far as I found there is no good lib in `zig` for creating temp files, so I write one for myself. This util file provides methods to create temp dir or temp file in system temp folder less tedious and manageable.

## Zig 0.16 API

This library has been updated for Zig 0.16. The API now requires an `*Io.Threaded` parameter for all operations.

### Quick Start

```zig
const std = @import("std");
const Io = std.Io;
const tmpfile = @import("tmpfile").tmpfile;

pub fn main() !void {
    var threaded = Io.Threaded.init(std.heap.page_allocator, .{});
    defer threaded.deinit();
    
    // Create a temp file
    var tmp_file = try tmpfile.tmpFile(&threaded, .{});
    defer tmp_file.deinit();
    
    // Write to file (Zig 0.16 uses positional I/O)
    try tmp_file.f.writePositionalAll(threaded.io(), "hello, world!", 0);
    
    // Read from file
    var buf: [4096]u8 = undefined;
    const read_count = try tmp_file.f.readPositionalAll(threaded.io(), &buf, 0);
    try std.testing.expectEqual(read_count, "hello, world!".len);
    try std.testing.expectEqualSlices(u8, buf[0..read_count], "hello, world!");
}
```

### Advanced Usage

```zig
const std = @import("std");
const Io = std.Io;
const tmpfile = @import("tmpfile").tmpfile;

pub fn main() !void {
    var threaded = Io.Threaded.init(std.heap.page_allocator, .{});
    defer threaded.deinit();
    const io = threaded.io();
    
    // Create a temp directory
    var tmp_dir = try tmpfile.tmpDirOwned(&threaded, .{});
    defer {
        tmp_dir.deinit();
        tmp_dir.allocator.destroy(tmp_dir);
    }
    
    // Create a temp file in the directory
    var tmp_file = try tmpfile.tmpFile(&threaded, .{ .tmp_dir = tmp_dir });
    defer tmp_file.deinit();
    
    try tmp_file.f.writePositionalAll(io, "hello, world!", 0);
    
    var buf: [4096]u8 = undefined;
    const read_count = try tmp_file.f.readPositionalAll(io, &buf, 0);
    try std.testing.expectEqual(read_count, "hello, world!".len);
    try std.testing.expectEqualSlices(u8, buf[0..read_count], "hello, world!");
    
    // Create another file in the same directory
    var tmp_file2 = try tmpfile.tmpFile(&threaded, .{ .tmp_dir = tmp_dir });
    defer tmp_file2.deinit();
    
    try tmp_file2.f.writePositionalAll(io, "hello, world!2", 0);
    const read_count2 = try tmp_file2.f.readPositionalAll(io, &buf, 0);
    try std.testing.expectEqual(read_count2, "hello, world!2".len);
    try std.testing.expectEqualSlices(u8, buf[0..read_count2], "hello, world!2");
}
```

## useage

use zig packager

```bash
zig fetch --save https://github.com/liyu1981/tmpfile.zig/archive/refs/heads/main.tar.gz
```

(or lock on any commit as)
```bash
zig fetch --save https://github.com/liyu1981/tmpfile.zig/archive/<commit hash>.tar.gz
```

this lib is also provided for `build.zig`, use like

```zig
// in build.zig
const tmpfile = @import("tmpfile").tmpfile;
```

## license

MIT
