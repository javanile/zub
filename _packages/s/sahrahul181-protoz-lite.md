---
title: protoz-lite
description: Compact, zero-heap-allocation Protocol Buffers compiler and comptime wire/JSON runtime for Zig 0.17+.
license: MIT
author: sahrahul181
author_github: sahrahul181
repository: https://github.com/sahrahul181/protoz-lite
keywords:
  - proto
  - protobuf
  - protocol-buffers
date: 2026-11-27
category: data-formats
updated_at: 2026-11-27T19:10:22+00:00
last_sync: 2026-11-27T19:10:22Z
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
permalink: /packages/sahrahul181/protoz-lite/
---

# protoz-lite

A compact, zero-heap-allocation Protocol Buffers code generator and comptime wire runtime for **Zig 0.17.0+**.

`protoz-lite` generates minimal Zig data structs paired with a small comptime `_pb` field descriptor table—no per-message encode/decode boilerplate, no arena/allocator required on the wire hot path, and direct zero-copy views into the incoming packet buffer.

## Features

- **Zero heap allocations**:
  - **Reverse single-pass encoding** (`encodeSlice`) writes fields backwards into a caller-supplied buffer in $O(N)$ time without pre-sizing passes.
  - **Zero-copy decoding** (`decode` / `validate`): `string` and `bytes` fields slice directly into the input buffer; `Repeated`, `Map`, and cyclic `Lazy` fields retain compact 32-byte wire views and decode lazily on iteration/lookup.
- **Fast comptime tag dispatch (`TagDispatch`)**:
  - 128-entry `O(1)` lookup table for 1-byte tags (field numbers `1..15`).
  - Comptime-sorted table (`<= 12` linear scan, `> 12` binary search) for multi-byte tags (field numbers `>= 16`).
  - `u64` known-field bitmask on the cold mismatch/skip path and an `inline` jump-table `switch`.
- **Comptime UTF-8 validation toggle**:
  - Enabled by default; disable per call via `DecodeOpts{ .validate_utf8 = false }` (`decodeOpts`, `validateOpts`) or globally at your executable/library root with `pub const pb_validate_utf8 = false;`.
- **Zero-allocation JSON serializer & `{f}` logger**:
  - `pb_rt.fmt` / `pb_rt.fmtOpts` integrate directly with `std.log`, `std.debug.print`, and `*std.Io.Writer` via `{f}`.
  - `pb_rt.stringifySlice` and `pb_rt.writeJson` support `emit_defaults`, pretty-printing (`indent`), and `.base64` / `.hex` formatting for `bytes` fields.
- **Compact `.proto` compiler (`pb_gen`)**:
  - Supports `proto2`, `proto3`, and `edition`, nested messages/enums, enum aliases, `oneof` (`union(enum)`), `map<K, V>`, packed/unpacked `repeated`, automatic cycle breaking with `Lazy(T)`, Zig keyword escaping, `--strip-enum-prefix`, and `--only` reachability pruning.

## Repository Layout

| File | Description |
| --- | --- |
| [`pb_rt.zig`](pb_rt.zig) | Zero-allocation wire runtime, comptime dispatch engine, and JSON logger |
| [`pb_gen.zig`](pb_gen.zig) | Standalone `.proto` to `.pb.zig` code generator CLI |
| [`build.zig`](build.zig) | Build script wiring `pb_gen`, `pb_rt`, and the example |
| [`build.zig.zon`](build.zig.zon) | Zig package manifest (`protoz_lite`, minimum Zig `0.17.0`) |
| [`example/telemetry.proto`](example/telemetry.proto) | Example Proto3 schema (enums, nested messages, maps, oneofs, self-cycle) |
| [`example/main.zig`](example/main.zig) | Runnable stack-only encode/decode/JSON example and round-trip test |

## Quick Start

Requires **Zig 0.17.0** (or newer).

```sh
# Build pb_gen and the example binary into zig-out/bin/
zig build

# Generate example schema, encode/decode on the stack, and print JSON output
zig build run

# Run tests
zig build test --summary all
```

## Using `pb_gen` CLI

```sh
zig build -Doptimize=ReleaseSafe
./zig-out/bin/pb_gen input.proto --out output.pb.zig --rt pb_rt.zig --strip-enum-prefix
```

If `input.proto` is omitted, `pb_gen` reads from `stdin`; if `--out` is omitted, it writes to `stdout`.

| Flag | Description |
| --- | --- |
| `--out <path>` | Output `.pb.zig` file path (default: `stdout`) |
| `--rt <import>` | `@import(...)` string emitted for `_pb_rt` (default: `"pb_rt.zig"`) |
| `--strip-enum-prefix` | Strip enum type prefix (including `PascalCase` -> `UPPER_SNAKE_CASE`) from enum members |
| `--only <syms>` | Comma-separated root message/enum names to keep; prunes unreachable declarations and emits shell-only parent structs for nested targets |

## Integrating in `build.zig`

```zig
const pb_rt = b.addModule("pb_rt", .{
    .root_source_file = b.path("pb_rt.zig"),
    .target = target,
    .optimize = optimize,
});

const pb_gen = b.addExecutable(.{
    .name = "pb_gen",
    .root_module = b.createModule(.{
        .root_source_file = b.path("pb_gen.zig"),
        .target = b.graph.host,
        .optimize = .ReleaseSafe,
    }),
});

const gen_cmd = b.addRunArtifact(pb_gen);
gen_cmd.addFileArg(b.path("schema.proto"));
gen_cmd.addArgs(&.{ "--rt", "pb_rt", "--strip-enum-prefix", "--out" });
const schema_pb_zig = gen_cmd.addOutputFileArg("schema.pb.zig");

const schema_pb = b.createModule(.{
    .root_source_file = schema_pb_zig,
    .target = target,
    .optimize = optimize,
    .imports = &.{ .{ .name = "pb_rt", .module = pb_rt } },
});
```

## Runtime API Overview (`pb_rt.zig`)

### Encode, Decode, and Validate

```zig
const pb_rt = @import("pb_rt");
const pb = @import("telemetry_pb");

var wire_buf: [512]u8 = undefined;
const wire = try pb_rt.encodeSlice(event, &wire_buf);

try pb_rt.validate(pb.Event, wire);
const decoded = try pb_rt.decode(pb.Event, wire);
```

- **UTF-8 override**:
  - Per-call: `pb_rt.decodeOpts(Msg, wire, .{ .validate_utf8 = false })`, `pb_rt.validateOpts(Msg, wire, .{ .validate_utf8 = false })` (plus `nextOpts`, `getOpts`, and `Lazy.decodeOpts`).
  - Global default: add `pub const pb_validate_utf8 = false;` to your executable or library root file.
- **Recursion limit**: `decodeDepth`, `decodeDepthOpts`, `validateDepth`, and `validateDepthOpts` enforce bounded nesting (`max_recursion_depth = 100` by default).

### Zero-Allocation Views

- **`Repeated(Codec)`**: Set `.{ .slice = &items }` when encoding; read decoded wire elements lazily with `var it = msg.items.iterator(); while (try it.next()) |item| { ... }`.
- **`Map(KCodec, VCodec)`**: Set `.{ .slice = &entries }` when encoding; look up keys in wire order (last duplicate wins) via `try msg.tags.get("key")`, or iterate with `msg.tags.iterator()`.
- **`Lazy(MsgT)`**: Used automatically for cyclic message fields; set `.{ .ptr = &child }` or `.{ .raw = bytes }` when encoding, and call `try msg.parent.?.decode()` when reading.

### Zero-Allocation JSON & Logging

```zig
// Compact single-line JSON directly in std.log / std.debug.print / std.Io.Writer
std.debug.print("{f}\n", .{pb_rt.fmt(decoded)});

// Pretty-printed JSON with hex-encoded bytes into a stack buffer
var json_buf: [1024]u8 = undefined;
const pretty = try pb_rt.stringifySlice(decoded, &json_buf, .{
    .indent = 2,
    .bytes_format = .hex,
    .emit_defaults = true,
});
```

## Notes & Scope

- Because decoded views point into the original wire buffer without heap allocation, the wire slice must outlive the decoded struct, and merging two separate disjoint buffers onto an already-populated `Repeated`, `Map`, or `Lazy` field returns `error.DisjointMergeUnsupported`.
- `pb_gen` parses and skips `service`, `extend`, `extensions`, `reserved`, `option`, and proto2 `group` declarations without generating bindings for them, and ignores proto2 `[default = ...]` values (using zero defaults / optional `?T = null`).
- Unknown fields are validated/skipped during `decode` and `validate`, and are not retained when re-encoding a decoded message.
