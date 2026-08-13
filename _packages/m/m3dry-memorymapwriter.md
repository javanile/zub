---
title: MemoryMapWriter
description: "Implementation of Zig's std.Io.Writer for std.Io.File.MemoryMap"
license: MIT
author: M3dry
author_github: M3dry
repository: https://github.com/M3dry/MemoryMapWriter
keywords:
date: 2026-07-21
updated_at: 2026-07-21T20:09:53+00:00
last_sync: 2026-07-21T20:09:53Z
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
permalink: /packages/M3dry/MemoryMapWriter/
---

## Getting started

Add to build.zig.zon via `zig fetch --save git+https://github.com/m3dry/MemoryMapWriter`, then in your build.zig:
```zig
pub fn build(b: *std.Build) void {
    const exe = b.addExecutable(.{ ... });

    const mw = b.dependency("MemoryMapWriter", .{});
    exe.root_module.addImport("MemoryMapWriter", mw.module("root"));
}
```

## Usage

```zig
const MemoryMapWriter = @import("MemoryMapWriter").MemoryMapWriter;

pub fn writeExample(io: std.Io, file: std.Io.File) !void {
    var mmw = try MemoryMapWriter.init(io, file, 4096);
    defer mmw.deinit();

    try mmw.writer.print("Hello {s}! answer is {d}\n", .{"world", 42});
    try mmw.writer.writeAll("more data\n");
    try mmw.writer.writeByteNTimes('x', 80);

    // Zero-copy: inspect what's been written without a file read
    _ = mmw.written(); // "Hello world! answer is 42\nmore data\nxxx..."

    // Random-access: rewind and overwrite
    try mmw.seekTo(6);
    try mmw.writer.writeAll("there"); // "Hello there! answer is 42\n..."

    // Trim the file to written size mid-life
    try mmw.truncate();

    // Pre-allocate so the next N bytes don't trigger a grow during a hot loop
    try mmw.ensureUnusedCapacity(1024);
}

pub fn sendFileExample(io: std.Io, src_file: std.Io.File, dst_file: std.Io.File) !void {
    var mmw = try MemoryMapWriter.init(io, dst_file, 4096);
    defer mmw.deinit();

    var reader = std.Io.File.Reader.init(src_file, io, &.{});
    _ = try mmw.writer.sendFileAll(&reader, .unlimited);
}
```
