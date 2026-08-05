---
title: zig-dll
description: A lightweight, idiomatic Zig abstraction for Windows DLL entry points. zig-dll removes the WinAPI boilerplate required to implement DllMain while keeping the DLL lifecycle explicit and compile-time validated.
license: MIT
author: kotop21
author_github: kotop21
repository: https://github.com/kotop21/zig-dll
keywords:
  - dll
  - winapi
  - windows
date: 2026-08-01
category: systems
updated_at: 2026-08-01T11:52:41+00:00
last_sync: 2026-08-01T11:52:41Z
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
permalink: /packages/kotop21/zig-dll/
---

# zig-dll

A lightweight, idiomatic Zig abstraction for Windows DLL entry points.

`zig-dll` removes the WinAPI boilerplate required to implement `DllMain` while keeping the DLL lifecycle explicit and compile-time validated.

## Features

* **No WinAPI boilerplate** — no manual `DllMain`, calling conventions, `HINSTANCE`, `LPVOID`, or raw reason codes.
* **Compile-time validation** — invalid entry point signatures fail at compile time.
* **Zero runtime overhead** — `zig-dll` only generates the `DllMain` adapter.
* **Typed API** — use `Reason` or `DllContext` instead of raw Windows values.
* **Explicit** — nothing is automatically executed or hidden from the user.

## Comparison

### Raw WinAPI

```zig
const std = @import("std");

pub export fn DllMain(
    hinst: std.os.windows.HINSTANCE,
    dwReason: u32,
    lpReserved: std.os.windows.LPVOID,
) callconv(.winapi) std.os.windows.BOOL {
    _ = hinst;
    _ = lpReserved;

    switch (dwReason) {
        1 => {
            // DLL_PROCESS_ATTACH
        },
        0 => {
            // DLL_PROCESS_DETACH
        },
        else => {},
    }

    return std.os.windows.TRUE;
}
```

### zig-dll

```zig
const dll = @import("zig-dll");

fn main(reason: dll.Reason) void {
    switch (reason) {
        .process_attach => {
            // Setup logic
        },
        .process_detach => {
            // Cleanup logic
        },
        else => {},
    }
}

comptime {
    dll.register(main);
}
```

### Need Windows metadata?

Instead of manually handling `HINSTANCE`, `LPVOID` and the raw reason:

```zig
const dll = @import("zig-dll");

fn main(ctx: dll.DllContext) void {
    if (ctx.reason == .process_attach) {
        ctx.disableThreadCalls();

        // ctx.hinst
        // ctx.raw_reason
        // ctx.reserved
    }
}

comptime {
    dll.register(main);
}
```

## Supported Signatures

The entry function must accept exactly one argument:

```text
Reason
?Reason
DllContext
```

It may return:

```text
void
bool
```

Example:

```zig
fn main(reason: dll.Reason) bool {
    switch (reason) {
        .process_attach => return initialize(),
        .process_detach => cleanup(),
        else => {},
    }

    return true;
}

comptime {
    dll.register(main);
}
```

Returning `false` makes `DllMain` return `FALSE`.

## Installation

```bash
zig fetch --save git+https://github.com/kotop21/zig-dll.git#v0.1.0
```

Then add the module to your DLL in `build.zig`:

```zig
const zig_dll = b.dependency("zig_dll", .{
    .target = target,
    .optimize = optimize,
});

lib.root_module.addImport(
    "zig-dll",
    zig_dll.module("zig-dll"),
);
```

## API

### `Reason`

```zig
pub const Reason = enum(u32) {
    process_attach = 1,
    thread_attach = 2,
    thread_detach = 3,
    process_detach = 0,
};
```

Unknown Windows reason codes are represented as `null` when using `?Reason`.

### `DllContext`

```zig
pub const DllContext = struct {
    hinst: std.os.windows.HINSTANCE,
    reason: ?Reason,
    raw_reason: u32,
    reserved: std.os.windows.LPVOID,

    pub fn disableThreadCalls(self: DllContext) void;
};
```

### `register`

```zig
comptime {
    dll.register(main);
}
```

Validates the entry point at compile time and generates the DLL entry point.
