---
title: zphp-bindings
description: Zig bindings for the zphp C extension ABI
license: MIT
author: nexxii04
author_github: nexxii04
repository: https://github.com/nexxii04/zphp-bindings
keywords:
  - php
date: 2026-09-11
updated_at: 2026-09-11T13:55:52+00:00
last_sync: 2026-09-11T13:55:52Z
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
permalink: /packages/nexxii04/zphp-bindings/
---

# zphp-bindings

Idiomatic [Zig](https://ziglang.org) bindings for the **zphp C extension ABI**.

Write zphp native extensions in pure Zig — no C required. The bindings mirror
`include/zphp_extension.h` exactly and layer a zero-cost, allocation-free Zig
surface on top.

```zig
const zphp = @import("zphp");

fn add(ctx: zphp.Context) void {
    ctx.returnInt(ctx.intArg(0) + ctx.intArg(1));
}

comptime {
    _ = zphp.extension(.{
        .name = "myext",
        .version = "1.0.0",
        .functions = &.{.{ .name = "my_add", .handler = add }},
    });
}
```

Build it as a dynamic extension and load it:

```sh
zig build -Doptimize=ReleaseFast
zphp --extension=zig-out/lib/libmyext.so run app.php
```

## Why it works with any Zig version

A dynamic extension is a self-contained shared object. It does not link
against zphp: the only contract is the C ABI of the function table. That means
the extension may be built with a **different Zig version** than the one that
built zphp. This package targets Zig 0.16; zphp 0.9 is built with 0.15 and
loads 0.16-built extensions without issue.

The one exception is the _static_ path (`zig build -Dextension=...` in zphp),
which compiles the extension into the zphp binary and therefore needs the same
toolchain. Use the dynamic path.

## Design rules

- **No hidden allocations.** Every wrapper is `inline` and delegates straight
  to the ABI table. The only stack buffers are for `call`/`callMethod`
  argument arrays and interface method lists, both compile-time bounded.
- **No hidden state.** `Context` and `Value` are single-pointer structs.
- **Lifetime is explicit.** Value handles are owned by the current request.
  Slices (`stringArg`, `Value.slice`, `iniGet`) point into VM memory valid for
  the request. Never keep a handle past the function that obtained it.
- **Handlers are plain Zig functions.** `extension()` wraps them in
  `callconv(.c)` trampolines at comptime.

## Layout

| File                   | Purpose                                                                                                              |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `src/abi.zig`          | Raw C ABI. A field-for-field mirror of `include/zphp_extension.h`.                                                   |
| `src/zphp.zig`         | Ergonomic surface: `Context`, `Value`, `Module`, `Class`, `extension()`.                                             |
| `src/tests.zig`        | Unit tests against a mock `Api`, covering the whole surface.                                                         |
| `examples/example.zig` | A complete reference extension exercising functions, a class, an interface, constants, ini defaults, and exceptions. |

## API at a glance

### Context

```zig
ctx.argCount()            // usize
ctx.arg(i)                // ?Value
ctx.selfObject()          // ?Value  ($this)
ctx.intArg(i)             // i64
ctx.floatArg(i)           // f64
ctx.boolArg(i)            // bool
ctx.stringArg(i)          // ?[]const u8
ctx.argType(i)            // abi.Type (.int, .string, .array, ...)

ctx.makeInt(v)  ctx.makeFloat(v)  ctx.makeBool(v)
ctx.makeString(bytes)     // copied by the runtime
ctx.makeArray()           // empty array
ctx.makeObject("Class")   // ?Value
ctx.makeResource(type, ptr) / ctx.resourceAs(T, v, type)

ctx.returnInt(v) ctx.returnFloat(v) ctx.returnBool(v)
ctx.returnString(bytes)   // copied
ctx.returnValue(v) ctx.returnNull()

ctx.throwError(msg) ctx.throwTypeError(msg)
ctx.throwValueError(msg) ctx.throwArgumentCountError(msg)
ctx.throwException("My\\Exception", msg)

ctx.call("strtoupper", args)          // ?Value, null == threw
ctx.callMethod(obj, "method", args)   // ?Value, null == threw
ctx.echo(bytes)
ctx.iniGet("name")        // ?[]const u8

ctx.requestData(T)        // ?*T
ctx.setRequestData(ptr)
ctx.workerData(T)         // ?*T
ctx.setWorkerData(ptr)
```

### Value

```zig
v.typeOf() v.isNull() v.toInt() v.toFloat() v.toBool()
v.slice(ctx)              // ?[]const u8
v.className(ctx)          // ?[]const u8
v.instanceOf(ctx, "Class")
v.getProperty(ctx, "name") / v.setProperty(ctx, "name", value)

v.arrayCount() v.push(ctx, value)
v.setIntKey(ctx, k, value) / v.getIntKey(ctx, k)
v.setStringKey(ctx, k, value) / v.getStringKey(ctx, k)
v.at(ctx, index)          // ?struct { key: ?Value, value: ?Value }
```

### Declaration

The `extension()` config covers the entire registration surface:

```zig
_ = zphp.extension(.{
    .name = "myext",
    .version = "1.0.0",
    .functions = &.{ .{ .name = "fn", .handler = fnHandler } },
    .classes = &.{.{
        .name = "My\\Class",
        .parent = null,
        .interfaces = &.{"My\\Iface"},
        .methods = &.{.{ .name = "m", .handler = mHandler, .arity = 1, .is_static = false }},
        .constants = &.{.{ .name = "K", .value = .{ .int = 1 } }},
        .properties = &.{.{ .name = "p", .value = .{ .int = 0 } }},
    }},
    .interfaces = &.{.{ .name = "My\\Iface", .methods = &.{"m"} }},
    .constants = &.{.{ .name = "GLOBAL", .value = .{ .string = "x" } }},
    .inis = &.{.{ .name = "my.ini", .default = "on" }},
    .resources = &.{.{ .class_name = "MyResource", .dtor = myDtor, .type_out = &my_type }},
    .lifecycle = .{
        .module_init = onModuleInit,
        .worker_init = onWorkerInit,
        .worker_shutdown = onWorkerShutdown,
        .request_init = onRequestInit,
        .request_shutdown = onRequestShutdown,
    },
});
```

If you need finer control, `Module` and `Class` expose every `register_*` and
`class_add_*` method directly for use inside a custom `module_init`.

## Tests

```sh
zig build test
```

The suite builds a mock `abi.Api` from real `callconv(.c)` functions and
exercises the trampolines, value/array/object/resource wrappers, registration
helpers, and the declarative `extension()` path.

## Building the example

```sh
zig build example -Doptimize=ReleaseFast
zphp --extension=zig-out/lib/libexample.so run demo.php
```

## Consumers

Add it as a dependency in your extension package:

```sh
zig fetch --save git+https://nexxii04/zphp-bindings
```

then in `build.zig`:

```zig
const bindings = b.dependency("zphp_bindings", .{ .target = target });
ext.root_module.addImport("zphp", bindings.module("zphp"));
```

## Memory notes

- Value handles live in a per-VM arena reset at the end of each request. They
  are valid for the whole request but must not outlive it.
- `returnString` and `makeString` copy; your source buffer remains yours.
- Native resources registered via `.resources` are destroyed by their `dtor`
  when the PHP value is unset, goes out of scope, unwinds through an exception,
  or the request ends. The runtime zeroes the pointer after destruction, so the
  destructor never runs twice.
- `requestData`/`workerData` pointers are yours to free in the matching
  `request_shutdown`/`worker_shutdown` hook.
