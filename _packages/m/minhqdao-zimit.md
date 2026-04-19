---
title: zimit
description: A rate limiter for Zig. Implements the GCRA (Generic Cell Rate Algorithm) with a Token-Bucket-like API.
license: MIT
author: minhqdao
author_github: minhqdao
repository: https://github.com/minhqdao/zimit
keywords:
  - api
  - atomics
  - backend
  - concurrency
  - gcra
  - generic-cell-rate-algorithm
  - networking
  - rate-limit
  - rate-limiter
  - rate-limiting
  - scheduler
  - server
  - throttle
  - throttling
  - token-bucket
  - zero-allocation
  - zigistry
date: 2026-04-19
category: systems
updated_at: 2026-04-19T08:50:31+00:00
last_sync: 2026-04-19T08:50:31Z
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
permalink: /packages/minhqdao/zimit/
---

# zimit

A zero-dependency GCRA-based rate limiter with a token-bucket-like API for Zig 0.16.0+.

## Features

- **Global limiting:** Use `GlobalLimiter` when you want a single shared limit across all requests (e.g. protect total server throughput). It's lock-free and thread-safe.
- **Per-key rate limiting:** Each key is tracked independently (e.g. per user ID or IP address). The `RateLimiter` is **not** thread-safe. If you share it across multiple threads, you should protect it with a `std.Io.Mutex`.
- **Blocking vs non-blocking:**
  - `allow()` → Immediate decision
  - `wait(io, key)` → Blocks until allowed (uses `std.Io.sleep`)
- **Clocks:**
  - `SystemClock` → Production (requires `std.process.Init.io`)
  - `ManualClock` → Deterministic tests

## Usage

```zig
const std = @import("std");
const zimit = @import("zimit");

pub fn main(init: std.process.Init) !void {
    const gpa = init.gpa;
    const io = init.io;

    var sys = zimit.SystemClock.init(io);

    var limiter = try zimit.RateLimiter([]const u8).init(.{
        .allocator = gpa,
        .rate = 5,
        .per = .second,
        .burst = 2,
        .clock = sys.clock(),
    });
    defer limiter.deinit();

    const key = "127.0.0.1";

    var i: usize = 0;
    while (i < 5) : (i += 1) {
        switch (try limiter.allow(key)) {
            .allowed => std.debug.print("allowed\n", .{}),
            .denied => |d| {
                std.debug.print("denied, time until allowed: {d}ms\n", .{d.retry_after_ms_ceil()});
            },
        }
    }
}

```
See [examples](examples) for more.


## Installation

Run:

```shell
zig fetch --save git+https://github.com/minhqdao/zimit.git#0.2.1
```

Then in your `build.zig`:

```zig
const zimit_dep = b.dependency("zimit", .{
    .target = target,
    .optimize = optimize,
});

const exe = b.addExecutable(.{
    .name = "yourapp",
    .root_module = b.createModule(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
        .imports = &.{
            .{ .name = "zimit", .module = zimit_dep.module("zimit") },
        },
    }),
});
```

## License
[MIT](LICENSE)
