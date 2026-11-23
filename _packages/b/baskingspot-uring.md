---
title: uring
description: "An io_uring completion loop for Zig: one ring, one tick, and a user_data type you define."
license: MIT
author: baskingspot
author_github: baskingspot
repository: https://github.com/baskingspot/uring
keywords:
  - event-loop
  - io-uring
date: 2026-11-18
category: systems
updated_at: 2026-11-18T02:31:05+00:00
last_sync: 2026-11-18T02:31:05Z
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
permalink: /packages/baskingspot/uring/
---

<h1>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/static/logo-dark.svg">
    <img src="docs/static/logo.svg" alt="uring" height="48">
  </picture>
</h1>

An io_uring completion loop for Zig: one ring, one tick, and a user_data type you define.

Zig's standard library already encodes every io_uring operation. What it does not have is the loop around them: when to submit, when to enter, and what runs when. `uring` is that loop, and nothing else.

It is parameterized by your tag, the value `user_data` carries home, so a completion means whatever you say it means. The handler is known at comptime, which makes every completion a direct call. Nothing allocates after `init`, and the loop never closes a descriptor, never frees a byte, and never rearms an operation.

```zig
const std = @import("std");
const uring = @import("uring");

const Tag = packed struct(u64) { op: u8, slot: u16, gen: u16, spare: u24 };

var cqes: [64]std.os.linux.io_uring_cqe = undefined;
var loop: uring.Loop(Tag) = try .init(.{
    .cqes = &cqes,
    .setup = .{ .single_issuer = true, .defer_taskrun = true },
});
defer loop.deinit();

_ = try loop.recv(.{ .op = 1, .slot = 7, .gen = 1 }, fd, .{ .buffer = buf }, 0);

// One pass per call. The deadline is the caller's, computed from the loop's
// clock every tick, because a moving deadline is application state.
while (!loop.stopped) {
    const next = server.nextDeadline(loop.now());
    try loop.tick(&server, Server.onCompletion, .{ .until = next });
}
```

A program with no deadlines of its own calls `run` instead, which ticks until
`stop`.

Deadlines ride the enter, not an operation: `io_uring_enter` takes a timeout
through `IORING_ENTER_EXT_ARG`, so moving a deadline costs no submission and no
cancel.

## What is in it

- [The loop](https://baskingspot.dev/uring/#the-loop): `Loop(Tag).tick`, `run`, `post`, `stop`, and `now`. One pass publishes, reaps, enters, dispatches, and submits, in that order.
- [The tag](https://baskingspot.dev/uring/#the-tag): any 64-bit type. `ping`, a packed struct, a pointer. `Cqe` decodes it once and hands it to a comptime handler.
- [Waiting](https://baskingspot.dev/uring/#waiting): `Wait.poll`, `no_wait`, `once`, and `until`, and what each costs.
- [Deadlines](https://baskingspot.dev/uring/#deadlines): a deadline through the enter with no submitted operation, and `timeout` when you want the kernel to own the clock.
- [Operations](https://baskingspot.dev/uring/#operations): every opcode the standard library encodes, each taking your tag and returning the SQE.
- [Registered resources](https://baskingspot.dev/uring/#registered-resources): files, buffers, eventfds, NAPI, and the probe.
- [Provided buffers](https://baskingspot.dev/uring/#provided-buffers): `BufferGroup` with a multishot receive that fills ring buffers the kernel picks.
- [The ring](https://baskingspot.dev/uring/#the-ring): `Ring`, its setup struct, and the submit discipline that keeps the queue from filling.
- [Performance](https://baskingspot.dev/uring/#performance): the loop against the equivalent hand-written loop, measured: about 3 ns per completion and two clock reads per idle pass.

Not implemented:

- `msg_ring`, futex operations, `tee`, `madvise`, `openat2`, `timeout_update`, and a generic `URING_CMD` for non-socket commands: the standard library does not encode them. Build the SQE through `Loop.sqe` if you need one.
- Registration for personalities, restrictions, io-wq worker limits, `sync_cancel`, `clamp`, `pbuf_status`, and `files_update2`: same reason.

## Install

```sh
zig fetch --save https://baskingspot.dev/uring/v0.4.0.tar.gz
```

Add the module to your build:

```zig
const uring = b.dependency("uring", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("uring", uring.module("uring"));
```

`uring` builds with Zig 0.17, on Linux only, because io_uring is Linux.

## Documentation

- The [guide](https://baskingspot.dev/uring/) says which piece to use for a task, with examples that compile.
- The [API reference](https://baskingspot.dev/uring/api/) documents every symbol.

## Work on it

```sh
just ci
```

`nix develop` provides the toolchain. `just` lists the recipes, and `just ci` runs what CI runs. `just bench` compares the loop against the equivalent hand-written loop.

## License

MIT. See `LICENSE`. The logo files in `docs/static/` are baskingspot marks and are not covered by it. See `docs/static/LICENSE`.

## How it's made

Built with LLM assistance. [How, in detail](https://github.com/baskingspot/.github/blob/main/docs/AI.md).

<a href="https://github.com/baskingspot"><img src="https://raw.githubusercontent.com/baskingspot/.github/main/brand/assets/badge.svg" alt="baskingspot" height="24"></a>
