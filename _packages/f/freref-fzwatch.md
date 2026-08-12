---
title: fzwatch
description: A lightweight and cross-platform file watcher for your Zig projects
license: MIT
author: freref
author_github: freref
repository: https://github.com/freref/fzwatch
keywords:
date: 2026-07-22
updated_at: 2026-07-22T22:54:17+00:00
last_sync: 2026-07-22T22:54:17Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 2
distributable_binary_count: 2
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/freref/fzwatch/
---

# fzwatch

A lightweight and cross-platform file watcher for your Zig projects.

> [!NOTE]
> This project exists to support [fancy-cat](https://github.com/freref/fancy-cat) and has limited features.

## Instructions

### Run example

You can run the [examples](./examples/) like so:

```sh
zig build run-<example-filename> -- <file-to-watch>
```

### Usage

A basic example can be found under [examples](./examples/basic.zig). The API is defined as follows:

```zig
pub const Event = enum { modified };
pub const Callback = fn (context: *anyopaque, event: Event) void;
pub const Opts = struct { latency: f16 = 1.0 };

pub fn init(allocator: std.mem.Allocator) !Watcher;
pub fn deinit(self: *Watcher) void;
pub fn addFile(self: *Watcher, path: []const u8) !void;
pub fn removeFile(self: *Watcher, path: []const u8) !void;
pub fn setCallback(self: *Watcher, callback: Callback) void;
pub fn start(self: *Watcher, opts: Opts) !void;
pub fn stop(self: *Watcher) !void;
```

### Testing

Run the test suite:

```sh
zig build test
```
