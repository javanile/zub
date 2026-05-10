---
title: termio
description: A simple Zig library for reading from stdin, with support for secret (echo-off) input.
license: MIT
author: gokhanaltun
author_github: gokhanaltun
repository: https://github.com/gokhanaltun/termio
keywords:
date: 2026-05-06
updated_at: 2026-05-06T16:00:39+00:00
last_sync: 2026-05-06T16:00:39Z
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
permalink: /packages/gokhanaltun/termio/
---

# termio

A simple Zig library for reading from stdin, with support for secret (echo-off) input.

## Platform Support

| Feature | Linux | macOS | BSD | Windows |
|---|---|---|---|---|
| `read` | ✓ | ✓ | ✓ | ✓ |
| `readToAlloc` | ✓ | ✓ | ✓ | ✓ |
| `readLineAlloc` | ✓ | ✓ | ✓ | ✓ |
| `readSecret` | ✓ | ✓ | ✓ | ✗ |
| `readSecretToAlloc` | ✓ | ✓ | ✓ | ✗ |
| `readSecretLineAlloc` | ✓ | ✓ | ✓ | ✗ |

> `readSecret` and its variants rely on POSIX `termios` and are not supported on Windows.

## Installation

Run the following command to add the package to your project:

```bash
zig fetch --save https://github.com/gokhanaltun/termio/archive/refs/tags/v0.2.0.tar.gz
```

Then add it to your `build.zig`:

```zig
const termio_dep = b.dependency("termio", .{});
exe.root_module.addImport("termio", termio_dep.module("termio"));
```

## Usage

```zig
const std = @import("std");
const TermIo = @import("termio").TermIo;

pub fn main(init: std.process.Init) !void {
    // Static read into a fixed buffer
    var buff: [100]u8 = undefined;
    const len = try TermIo.read(init.io, &buff);
    std.debug.print("{s}\n", .{buff[0..len]});

    // Read a line into an allocated slice
    const termio = TermIo.init(init.gpa, init.io);
    const line = try termio.readLineAlloc();
    defer init.gpa.free(line);
    std.debug.print("{s}\n", .{line});

    // Read a secret (echo off) into a fixed buffer
    var secret_buff: [100]u8 = undefined;
    const secret_len = try TermIo.readSecret(init.io, &secret_buff);
    std.debug.print("{s}\n", .{secret_buff[0..secret_len]});

    // Read a secret line into an allocated slice
    const secret = try termio.readSecretLineAlloc();
    defer init.gpa.free(secret);
    std.debug.print("{s}\n", .{secret});
}
```

## API

### Static (fixed buffer)

```zig
TermIo.read(io: std.Io, buff: []u8) !usize
TermIo.readSecret(io: std.Io, buff: []u8) !usize  // POSIX only
```

### Instance (allocator-based)

```zig
TermIo.init(allocator: std.mem.Allocator, io: std.Io) TermIo
termio.readToAlloc(delimiter: u8) ![]u8
termio.readLineAlloc() ![]u8
termio.readSecretToAlloc(delimiter: u8) ![]u8      // POSIX only
termio.readSecretLineAlloc() ![]u8                  // POSIX only
```

## Minimum Zig Version

0.16.0
