---
title: zeit
description: a date and time library written in zig. Timezone, DST, and leap second aware
license: MIT
author: rockorager
author_github: rockorager
repository: https://github.com/rockorager/zeit
keywords:
  - date
  - datetime
  - time
  - timezone
date: 2026-06-20
updated_at: 2026-06-20T10:55:16+00:00
last_sync: 2026-06-20T10:55:16Z
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
permalink: /packages/rockorager/zeit/
---

# zeit

A time library written in zig.

## Install

zeit's `main` branch currently tracks Zig 0.17-dev.

```
zig fetch --save git+https://github.com/rockorager/zeit#main
```

For the last Zig 0.16-compatible release, fetch `v0.9.0`:

```
zig fetch --save git+https://github.com/rockorager/zeit#v0.9.0
```

Or install another [tag](https://github.com/rockorager/zeit/tags) instead of main.

## Usage

[API Documentation](https://rockorager.github.io/zeit/)

```zig
const std = @import("std");
const zeit = @import("zeit");

pub fn main(init: std.process.Init) !void {

    // Get a "now" instant in UTC.
    const now = zeit.instant(.{ .now = init.io }, &zeit.utc);

    // Load our local timezone. This needs an allocator. Optionally pass in a
    // zeit.EnvConfig to support TZ and TZDIR environment variables
    const local = try zeit.local(init.gpa, init.io, .{});
    defer local.deinit();

    // Convert our instant to a new timezone
    const now_local = now.in(&local);

    // Generate date/time info for this instant
    const dt = now_local.time();

    // Print it out
    std.debug.print("{}\n", .{dt});

    // zeit.Time{
    //    .year = 2024,
    //    .month = zeit.Month.mar,
    //    .day = 16,
    //    .hour = 8,
    //    .minute = 38,
    //    .second = 29,
    //    .millisecond = 496,
    //    .microsecond = 706,
    //    .nanosecond = 64
    //    .offset = -18000,
    // }

    var buf: [256]u8 = undefined;
    var writer = std.Io.Writer.fixed(&buf);

    // Format using strftime specifier. Format strings are not required to be comptime
    try dt.strftime(&writer, "%Y-%m-%d %H:%M:%S %Z");
    std.debug.print("{s}\n", .{writer.buffered()});

    writer.end = 0;

    // Or...golang magic date specifiers. Format strings are not required to be comptime
    try dt.gofmt(&writer, "2006-01-02 15:04:05 MST");
    std.debug.print("{s}\n", .{writer.buffered()});

    // Load an arbitrary location using IANA location syntax. The location name
    // comes from an enum which will automatically map IANA location names to
    // Windows names, as needed. Pass an optional EnvConfig to support TZDIR
    const vienna = try zeit.loadTimeZone(init.gpa, init.io, .@"Europe/Vienna", .{});
    defer vienna.deinit();

    // Parse an Instant from an ISO8601 or RFC3339 string
    _ = try zeit.instantFromText(
        .iso8601,
        "2024-03-16T08:38:29.496-1200",
        &zeit.utc,
    );

    _ = try zeit.instantFromText(
        .rfc3339,
        "2024-03-16T08:38:29.496706064-1200",
        &zeit.utc,
    );
}
```
