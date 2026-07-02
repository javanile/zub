---
title: zretry
description: retry fallible functions in zig
license: MIT
author: k1ngkevin
author_github: k1ngkevin
repository: https://github.com/k1ngkevin/zretry
keywords:
  - backoff
  - fault-tolerance
  - retry
date: 2026-07-02
updated_at: 2026-07-02T10:34:18+00:00
last_sync: 2026-07-02T10:34:18Z
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
permalink: /packages/k1ngkevin/zretry/
---

# zretry

A Zig retry helper with configurable delay strategy and jitter.

## Installing

Create a project with `zig init` that has a `build.zig` and `build.zig.zon`.

Run:

```sh
zig fetch --save 'git+https://github.com/k1ngkevin/zretry#v0.3.1'
```

Add this to your `build.zig`:

```zig
const zretry = b.dependency("zretry", .{
    .target = target,
});

exe.root_module.addImport("zretry", zretry.module("zretry"));
```

then import it like this

```zig
const retry = @import("zretry");
```

Note:
Make sure you're using zig version `0.16.0` or higher

## Usage

Import the module in your code and call `zretry` with an operation that returns an error union such as `!void` or `!T`.
The retry options carry the `std.Io` value used for sleeping and randomness.
Pass `.{}` for a function with no arguments, or a tuple containing the arguments for a function that has them.

```zig
const std = @import("std");
const retry = @import("zretry");

fn doWork() !void {
    // fallible operation
}

pub fn main(init: std.process.Init) !void {
    try retry.zretry(doWork, .{}, .{
        .io = init.io,
        .max_attempts = 5,
        .initial_delay_ms = 250,
        .max_delay_ms = 5_000,
    });
}
```

For a function that takes arguments, pass those arguments as the second parameter:

```zig
const std = @import("std");
const retry = @import("zretry");

fn downloadFile(url: []const u8, output_path: []const u8) !void {
    // fallible operation using url and output_path
}

pub fn main(init: std.process.Init) !void {
    try retry.zretry(
        downloadFile,
        .{ "https://example.com/file.html", "output.html" },
        .{
            .io = init.io,
            .max_attempts = 5,
            .initial_delay_ms = 250,
            .max_delay_ms = 5_000,
        },
    );
}
```

## Options

- `io`: `std.Io` used to sleep between retries and seed jitter randomness.
- `max_attempts`: total number of attempts before returning the final error.
- `initial_delay_ms`: starting delay in milliseconds.
- `max_delay_ms`: maximum delay in milliseconds.
- `strategy`: `.fixed`, `.linear`, or `.exponential`.
- `jitter`: `.none` or `.full`.
- `random`: optional `std.Random`; if omitted, one is seeded from `std.Io`.

## Development

Run the test suite:

```sh
zig build test
```
