---
title: zrx
description: Declarative push streams for Zig with type-keyed dependency injection, compiled down to the loop you would have written by hand.
license: MIT
author: aleksaelezovic
author_github: aleksaelezovic
repository: https://github.com/aleksaelezovic/zrx
keywords:
  - comptime
  - dataflow
  - dependency-injection
  - stream-processing
  - streams
date: 2026-11-23
category: tooling
updated_at: 2026-11-23T18:55:29+00:00
last_sync: 2026-11-23T18:55:29Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 3
distributable_binary_count: 3
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/aleksaelezovic/zrx/
---

# zrx

Declarative push streams for Zig with type-keyed dependency injection, compiled
down to the loop you would have written by hand.

**Experimental.** This is a ground-up rewrite; the API is small on purpose and
may still change.

## Install

Requires exactly [Zig 0.17.0](https://ziglang.org/download/).

```sh
zig fetch --save=zrx https://github.com/aleksaelezovic/zrx/archive/refs/tags/v0.2.0.tar.gz
```

Then import it in `build.zig`:

```zig
const zrx = b.dependency("zrx", .{ .target = target, .optimize = optimize }).module("zrx");
exe.root_module.addImport("zrx", zrx);
```

## Quickstart

```zig
const std = @import("std");
const zrx = @import("zrx");
const pipe = zrx.pipe;
const program = zrx.program;
const rescue = zrx.rescue;
const fromSlice = zrx.fromSlice;
const map = zrx.map;
const filter = zrx.filter;
const fold = zrx.fold;
const ge = zrx.ge;
const print = zrx.print;
const sum = zrx.ext.math.sum;
const process = zrx.ext.process;
const stdout = process.stdout;
const Stdout = process.Stdout;

const Scale = struct { by: u32 };

fn scale(factor: Scale, value: u32) u32 { // `factor` is injected by its type
    return value * factor.by;
}

pub fn main(init: std.process.Init) u8 {
    var exit: process.Exit = .{};
    const values = [_]u32{ 1, 2, 3, 4 };
    const total = pipe(.{
        map(scale),
        filter(ge(6)),
        fold(@as(u64, 0), sum),
        print(Stdout, "total: {d}\n"),
    });
    program(fromSlice(&values), total)
        .provide(.{stdout(Stdout, 64)}) // a default; it could as well be given to `run`
        .run(.{
        init.io,
        Scale{ .by = 2 },
        &exit,
        // A run returns nothing: what ends it goes to a rescue, and here
        // becomes the exit status.
        rescue(process.fail(.{ .prefix = null })),
    });
    return exit.code;
}
```

It prints `total: 14`: each value doubled, those of at least 6 added up.

## The model

| Concept | What it is |
|---|---|
| **handler** | A plain function. Its leading parameters are dependencies, found by type; the operator decides the data after them (an item for `map`, a state and an item for `fold`). |
| **operator** | A stage built from a handler or a setting: `map(f)`, `filter(p)`, `take(3)`, `queue(16)`. |
| **pipe** | Operators composed left to right. A pipe is itself an operator, so pipes nest. |
| **program** | One source feeding one pipe that ends in a terminal operator. Nothing runs until `run(.{ deps })`. |
| **system** | Several programs run together with the same dependencies. |

Mistakes are compile errors that say what to do: a missing dependency, a
handler whose parameter does not match the stream, an operator after a terminal
one, a pipe that never ends, a failure nobody takes.

Read the **[guide](docs/guide.md)** for every operator, the error and
concurrency model, and how to write operators of your own. The
[examples](examples) are small and each is run and checked by the build;
[examples/apps](examples/apps/README.md) holds complete applications.

## Zero overhead, checked

Everything is resolved at compile time: every stage is a local variable of
the run, dependencies are copied into the handlers that asked for them once,
and a push is a chain of direct calls the optimizer flattens. `zig build
zero-overhead` compiles each [fixture](tests/zero_overhead/cases.zig) twice, as
a pipeline and as a hand-written loop, and compares the optimized LLVM IR.
Every synchronous operator has one. Most compile to the same instructions; the
rest may be shaped differently but have no calls and no extra memory traffic.
The [guide](docs/guide.md#how-zero-overhead-is-checked) says exactly what is
compared and what that does not show.

`queue`, timed operators, and `concurrent` create task boundaries and carry
real storage and synchronization costs.

## Platforms

CI runs the tests natively on Linux, macOS and Windows; a few that need
POSIX file system behavior are skipped on Windows. The core also
compiles for targets without an operating system (`wasm32-freestanding`,
`thumb-freestanding-eabi`).

## Develop

The repository pins Zig in [`.zigversion`](.zigversion).

```sh
zig build test            # suites, compile-error contracts, examples, zero-overhead
zig build check           # the above plus formatting and cross compilation
zig build example         # run the examples
zig build zero-overhead   # print the code comparison
zig build benchmark       # throughput against a hand-written loop
```

## License

[MIT](LICENSE)
