---
title: wick
description: A small, dependency-free WebAssembly interpreter for embedding plugin systems in Zig applications
license: MIT
author: ooyeku
author_github: ooyeku
repository: https://github.com/ooyeku/wick
keywords:
  - wasm
  - webassembly
date: 2026-07-20
category: systems
updated_at: 2026-07-20T05:18:07+00:00
last_sync: 2026-07-20T05:18:07Z
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
permalink: /packages/ooyeku/wick/
---

# wick

**A small, dependency-free WebAssembly interpreter for embedding
plugin systems in Zig applications.**

wick runs wasm 1.0 core modules by direct interpretation — no JIT, no
codegen, no libc. An `std.mem.Allocator` is the only thing it asks of
its host. It is built for one job: letting an application execute
third-party code where the host controls every doorway (imports are
the only way out of the sandbox) and every budget (memory ceiling,
call depth, instruction fuel).

wick is a deliberate interpreter, not a performance runtime: if you
need near-native wasm speed, use a JIT engine; if you need a few
thousand plugin calls per second, zero dependencies, and one static
binary, wick is the point on that curve.

## Features

- **wasm 1.0 core execution** — full control flow, i32/i64/f32/f64
  arithmetic and conversions (including trapping *and* saturating
  float→int truncations), linear memory with bounded growth, globals,
  funcref tables with `call_indirect` (runtime type-checked), active
  data and element segments, and the bulk-memory ops LLVM toolchains
  emit (`memory.copy`, `memory.fill`, `memory.init`, `data.drop`).
- **Typed host bindings** — declare host functions with native Zig
  signatures; comptime codegen does the argument unpacking, including
  `[]const u8` parameters resolved through guest memory with bounds
  checks:

  ```zig
  const Host = struct {
      fn log(call: wick.bindings.Ctx(Host), level: u32, msg: []const u8) void {
          std.log.info("plugin[{d}]: {s}", .{ level, msg });
      }
  };
  const imports = [_]wick.HostImport{
      .{ .module_name = "env", .field_name = "log", .func = wick.bind(Host, Host.log) },
  };
  ```
- **Resource limits** — per-instance `Limits`: instruction fuel
  (a runaway module returns `error.OutOfFuel` instead of hanging your
  host), call-depth cap, value-stack cap, and a memory ceiling the
  host imposes on top of whatever the module declares.
- **Hostile-input hardening** — decode bounds every count against the
  bytes backing it, so a forged section can't drive a multi-gigabyte
  allocation; unimplemented opcodes fail loudly with
  `error.UnsupportedOp` rather than miscomputing silently.

## Non-goals (for now)

SIMD, threads, multi-memory, reference types beyond funcref tables,
and WASI. Gaps surface as typed errors, never as wrong answers.

## Quick start

```zig
const wick = @import("wick");

var module = try wick.decode(allocator, wasm_bytes);
defer module.deinit();

var instance = try wick.instantiateWithLimits(allocator, &module, &imports, &host, .{
    .fuel = 10_000_000,        // ~instructions per invoke
    .max_memory_pages = 64,    // 4 MiB ceiling
});
defer instance.deinit();

const entry = module.findExport("activate", .func) orelse return error.NoEntry;
var results: [1]u64 = undefined;
_ = try wick.invoke(&instance, entry, &.{}, results[0..0]);
```

Values cross the boundary as `u64` bit patterns (f32 in the low 32
bits). For host functions, `wick.bind` hides that; for calling guest
exports, you widen/narrow at the call site.

## Install

```bash
zig fetch --save git+https://github.com/ooyeku/wick
```

```zig
// build.zig
const wick = b.dependency("wick", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("wick", wick.module("wick"));
```

## Testing

`zig build test` runs the suite: decoder hardening, control-flow
regressions, float semantics (NaN, saturation), `call_indirect`
dispatch and traps, fuel exhaustion, and an end-to-end test of the
full plugin-host integration pattern (host imports, `user_data`,
guest strings, export lookup and invocation).

## License

[MIT](LICENSE)
