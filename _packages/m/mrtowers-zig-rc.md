---
title: zig-rc
description: Reference counting module for Zig
license: MIT
author: mrtowers
author_github: mrtowers
repository: https://github.com/mrtowers/zig-rc
keywords:
  - reference-counting
date: 2026-11-11
updated_at: 2026-11-11T07:32:20+00:00
last_sync: 2026-11-11T07:32:20Z
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
permalink: /packages/mrtowers/zig-rc/
---

# Reference Counting Smart Pointer for Zig

A simple and efficient implementation of a reference counting smart pointer for Zig. This library helps manage the lifetime of heap-allocated objects by automatically tracking references and freeing memory when no references remain.

Requires **Zig 0.17.0**.

## Features

- **Automatic Memory Management**: Simplifies memory handling by automatically freeing unused resources.
- **Thread-Safe**: Includes mutex-based reference counting for multithreaded applications via `Arc`.
- **Lightweight**: Designed to be minimal and efficient.
- **Auto deinit**: `Rc` and `Arc` support an optional `auto_deinit` mode. When enabled, the managed value is automatically deinitialized on the final destroy. If the wrapped type defines a `deinit()` method (with any return type), it will be called before the memory is released.
- **Weak Pointers** (`WeakRc` / `WeakArc`): Provide non-owning references to managed values without increasing the reference count. Weak pointers do not keep the value alive and can be safely upgraded to a strong `Rc`/`Arc` only if the value still exists. This helps prevent reference cycles and memory leaks, especially in graph-like data structures.

## Installation

### Adding to Your Project

```bash
zig fetch --save git+https://github.com/mrtowers/zig-rc
```
In `build.zig`:

```zig
const rc = b.dependency("zig-rc", .{
    .target = target,
    .optimize = optimize,
});
your_app.root_module.addImport("rc", rc.module("rc"));
```

## Usage

### Basic Example

```zig
const std = @import("std");
const rc = @import("rc");
const Allocator = std.mem.Allocator;

const User = struct {
    name: []u8,
    allocator: Allocator,

    pub fn deinit(self: *const User) u8 { //run automatically by `auto_deinit`
        self.allocator.free(self.name);
        return 0;
    }
};

pub fn main() !void {
    var gpa = std.heap.SafeAllocator.init(std.heap.page_allocator, .{});
    defer if (gpa.deinit() != 0) @panic("memory leak");
    const allocator = gpa.allocator();

    var ptr = try rc.Rc(User).init(allocator, User{
        .allocator = allocator,
        .name = try allocator.dupe(u8, "some user"),
    }, .{
        .auto_deinit = true,
    });
    var ptr2 = ptr.ref();
    _ = ptr.deref();
    _ = ptr2.deref(); // object cleaned up here

}
```

### Weak pointers with Rc

```zig
const std = @import("std");
const rc = @import("rc");
const Rc = rc.Rc;
const WeakRc = rc.WeakRc;

pub fn main() !void {
    var gpa = std.heap.SafeAllocator.init(std.heap.page_allocator, .{});
    defer if (gpa.deinit() != 0) @panic("memory leak");
    const allocator = gpa.allocator();

    const ptr = try Rc(i32).init(allocator, 5, .{});
    defer ptr.deref();

    usingWeak(ptr.weak());
}

fn usingWeak(weak: WeakRc(i32)) void {
    defer weak.deref(); //deref every instance

    if (weak.upgrade()) |number_ref| {
        defer number_ref.deref();
        std.debug.print("number is: {d}\n", .{number_ref.value.*});
    }
}
```

### Weak pointers with Arc

```zig
const std = @import("std");
const rc = @import("rc");
const Arc = rc.Arc;
const WeakArc = rc.WeakArc;

pub fn main(init: std.process.Init) !void {
    var gpa = std.heap.SafeAllocator.init(std.heap.page_allocator, .{});
    defer if (gpa.deinit() != 0) @panic("memory leak");
    const allocator = gpa.allocator();
    const io = init.io;

    const ptr = try Arc(i32).init(allocator, 5, .{});
    defer _ = ptr.deref(io) catch unreachable;

    try usingWeak(try ptr.weak(io), io);
}

fn usingWeak(weak: WeakArc(i32), io: std.Io) std.Io.Cancelable!void {
    defer weak.deref(io) catch unreachable;

    if (try weak.upgrade(io)) |number_ref| {
        defer _ = number_ref.deref(io) catch unreachable;
        std.debug.print("number is: {d}\n", .{number_ref.rc.value.*});
    }
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

Also you can donate me [here](https://buymeacoffee.com/mrtowers), this helps alot! (mainly because i drink a lot of coffee)

Happy coding! 🎉
