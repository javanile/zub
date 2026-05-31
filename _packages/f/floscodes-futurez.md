---
title: futurez
description: A small runtime for running futures in zig.
license: MIT
author: floscodes
author_github: floscodes
repository: https://github.com/floscodes/futurez
keywords:
date: 2026-05-28
updated_at: 2026-05-28T10:22:44+00:00
last_sync: 2026-05-28T10:22:44Z
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
permalink: /packages/floscodes/futurez/
---

# futurez

[![CI](https://github.com/floscodes/futurez/actions/workflows/ci.yml/badge.svg)](https://github.com/floscodes/futurez/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

futurez is a small runtime for running asynchronous tasks using futures in Zig.


## Minimal Example

```zig
const std = @import("std");
const futurez = @import("futurez");
const Runtime = futurez.Runtime;

fn main() !void {
    const allocator = std.heap.page_allocator;
    var rt = try Runtime.init(allocator);
    defer rt.deinit();

    const task = try rt.spawn(myTaskFunction, .{});
    const result = task.join(i32);
    std.debug.print("Result: {d}\n", .{result});
}

fn myTaskFunction() i32 {
    return 42;
}
```

For a complete example showcasing advanced usage with dynamic allocations and multiple parameters, see [examples/basic.zig](./examples/basic.zig).

## Overview

futurez spawns as many worker threads as logical CPU cores available on your machine. These threads continuously pick up and run asynchronous tasks you spawn via `Runtime.spawn`. Finished tasks remain in the task queue until you call the `join()` method on the associated `*Task` to retrieve the result.

You can also control the number of worker threads by initializing the runtime with a specific core count using `initWithCores()`:

```zig
const allocator = std.heap.page_allocator;
var rt = try Runtime.initWithCores(allocator, 4);
defer rt.deinit();
```
