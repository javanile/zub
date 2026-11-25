---
title: protoz
description: "Zero-allocation Protocol Buffers (proto3 & proto2) compiler and runtime written in pure Zig."
license: MIT
author: sahrahul181
author_github: sahrahul181
repository: https://github.com/sahrahul181/protoz
keywords:
  - proto
  - protobuf
  - protobuf3
  - protobuffer
date: 2026-11-25
category: data-formats
updated_at: 2026-11-25T07:04:31+00:00
last_sync: 2026-11-25T07:04:31Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 4
distributable_binary_count: 4
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/sahrahul181/protoz/
---

# protoz

[![CI](https://github.com/sahrahul181/protoz/actions/workflows/ci.yml/badge.svg)](https://github.com/sahrahul181/protoz/actions/workflows/ci.yml)

A high-performance, **zero-allocation** Protocol Buffers (`proto2`, `proto3`, and `edition`) compiler and runtime for **Zig 0.17.1**.

---

## Highlights

- **Zero Heap Allocations on Decode & Encode:** `Repeated`, `Map`, `Lazy`, and `UnknownFields` operate as compact **32–40 byte** zero-copy views directly over wire slices; strings and bytes borrow directly from the caller buffer.
- **Multi-GB/s Wire Throughput:** Up to **66.72 Mops/s** (14.99 ns) on small messages and **3.06 GB/s** decode / **2.76 GB/s** encode on batched payloads in `ReleaseFast` (see [Benchmarks](#benchmarks)).
- **Single-Pass Reverse Serialization (`ReverseWriter`):** `encodeSlice` writes backwards into caller-owned stack or slab buffers in a single pass—**1.76x faster** than forward streaming on batched payloads with no pre-pass size calculation for nested submessages.
- **On-Demand Decoding:** Comptime `decodeOnly(bytes, .{ .id, .role })` materializes a minimal stack struct and skips unselected fields (**4.4x–6.7x faster** than full decode); `fieldIterator(bytes)` streams fields with early exit (**9.9x faster** on `User`).
- **Full Protocol Toolkit:** Length-delimited framing (TCP/Unix/WAL), 5-byte gRPC HTTP/2 framing + comptime unary dispatch, zero-allocation ProtoJSON (`encodeJsonSlice` / `decodeJson`), Well-Known Type helpers (`Timestamp`, `Duration`, `Any`), `{f}` debug formatting, opt-in `UnknownFields` pass-through, and arena-backed `cloneOwned` / `cloneMessage`.
- **Two Compiler Frontends:** Native `zig-protoc` (pure Zig lexer/parser/resolver with `file:line:col` diagnostics, transitive `import public`, and Make `.d` depfiles) and a standard `protoc-gen-zig` plugin for `protoc` / `buf`.
- **First-Class `build.zig` Integration:** Package manifest exports `@import("protoz")` (application facade), `proto_wire` (slim runtime imported by generated `.pb.zig` files), `proto_wkt` (pre-wired Google Well-Known Types), host `zig-protoc` / `protoc-gen-zig` binaries, and `addProtoModule` / `addProtoPackage` helpers.

---

## Installation

Requires **Zig 0.17.1+**.

Add `protoz` to your project with `zig fetch`:

```sh
zig fetch --save git+https://github.com/sahrahul181/protoz#v0.1.0
```

Wire schema compilation in your `build.zig`:

```zig
const std = @import("std");
const protoz = @import("protoz");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const protoz_dep = b.dependency("protoz", .{
        .target = target,
        .optimize = optimize,
    });

    const api_pkg = protoz.addProtoPackage(b, protoz_dep, .{
        .include_dirs = &.{b.path("proto")},
        .entry_protos = &.{b.path("proto/api.proto")},
        .out_dir_name = "api_pb",
        .target = target,
        .optimize = optimize,
        // .preserve_unknown_fields = true, // opt-in proxy pass-through
    });

    const exe = b.addExecutable(.{
        .name = "my-app",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target = target,
            .optimize = optimize,
            .imports = &.{
                .{ .name = "protoz", .module = protoz_dep.module("protoz") },
                .{ .name = "api_pb", .module = api_pkg.module },
            },
        }),
    });
    b.installArtifact(exe);
}
```

For standalone single-file `.proto` schemas with no imports, use `protoz.addProtoModule`:

```zig
const user_pb = protoz.addProtoModule(b, protoz_dep, .{
    .proto = b.path("proto/user.proto"),
    .out_name = "user.pb.zig",
    .target = target,
    .optimize = optimize,
});
```

For standard Google Well-Known Types without generating your own schema, depend directly on `protoz_dep.module("proto_wkt")`:

```zig
.{ .name = "proto_wkt", .module = protoz_dep.module("proto_wkt") }
```

### Using `protoc-gen-zig` with `protoc`

```sh
zig build -Doptimize=ReleaseFast
protoc --plugin=protoc-gen-zig=./zig-out/bin/protoc-gen-zig \
  --zig_out=gen \
  --zig_opt=wire_import=proto_wire,root_file=root.zig,preserve_unknown_fields=false \
  -I proto -I include proto/api.proto
```

Standalone `zig-protoc` also supports `--out <file>`, `--out-dir <dir>`, `--root-file <name>`, `--depfile <file>`, `-I <dir>`, and `--preserve-unknown-fields`:

```sh
./zig-out/bin/zig-protoc \
  -I proto -I include \
  --out-dir generated_pb \
  --root-file root.zig \
  --depfile generated_pb/proto.d \
  proto/api.proto
```

---

## Quick API Guide

### Encode & Decode (Zero Allocations)

```zig
const pb = @import("api_pb").api;

const user = pb.UserProfile{
    .id = 42,
    .name = "alice",
    .scores = .{ .slice = &.{ 10, 20, 30 } },
    .quotas = .{ .slice = &.{.{ .key = "cpu", .value = 16 }} },
    .contact = .{ .email = "alice@acme.dev" },
};

var buf: [512]u8 = undefined;
const wire_bytes = try user.encodeSlice(&buf);

// Full zero-alloc decode (validates wire format + UTF-8, returns zero-copy views)
const view = try pb.UserProfile.decode(wire_bytes);
const cpu = try view.quotas.get("cpu"); // ?i32 = 16
```

### On-Demand Decoding (`decodeOnly` & `fieldIterator`)

```zig
// Materializes only `.id` and `.role` on the stack; skips UTF-8, maps, and submessages.
const routing = try pb.UserProfile.decodeOnly(wire_bytes, .{ .id, .role });

// Streaming cursor with early exit.
var it = pb.UserProfile.fieldIterator(wire_bytes);
while (try it.next()) |item| switch (item) {
    .id => |id| { _ = id; break; },
    else => {},
};
```

### Length-Delimited Framing & Owned Detach

```zig
const protoz = @import("protoz");

var frame_buf: [256]u8 = undefined;
const frame = try protoz.encodeDelimitedSlice(user, &frame_buf);

// Streaming-safe: returns `null` on partial TCP buffers, `error.FrameTooLarge` on oversize.
if (try protoz.tryDecodeDelimited(pb.UserProfile, frame, 64 * 1024)) |f| {
    // Outlive the network buffer with a single O(1) arena teardown:
    var owned = try protoz.cloneOwned(allocator, f.msg);
    defer owned.deinit();
}
```

### ProtoJSON & Well-Known Types

```zig
const wkt = @import("proto_wkt");

// Zero-allocation wire-to-JSON transcoding
var json_buf: [1024]u8 = undefined;
const json_text = try view.encodeJsonSlice(&json_buf, .{});

// Zero-copy fast-path decode (flat unescaped messages need 0 arena bytes)
const from_json = try pb.UserProfile.decodeJson(arena, json_text, .{
    .ignore_unknown_fields = true,
});

// Timestamp / Duration / Any helpers (0 heap allocations)
var ts_buf: [32]u8 = undefined;
const ts = try wkt.google_protobuf_timestamp.Timestamp.parseRfc3339("2026-11-25T14:41:00.500Z");
const rfc3339 = try ts.formatRfc3339Buf(&ts_buf);

var any_buf: [512]u8 = undefined;
const packed_any = try wkt.google_protobuf_any.Any.packSlice(user, &any_buf);
const unpacked = try packed_any.unpack(pb.UserProfile);
```

### gRPC Framing & Comptime Unary Dispatch

```zig
const protoz = @import("protoz");

const resp_frame = try protoz.rpc.dispatchUnaryGrpc(
    pb.Health,
    &handler,
    "/acme.v1.Health/Check",
    req_grpc_frame,
    4 * 1024 * 1024,
    &resp_buf,
);
```

---

## Benchmarks

Run the reproducible suite locally (`--filter` supported):

```sh
zig build bench -Doptimize=ReleaseFast
zig build bench -Doptimize=ReleaseFast -- --filter Batch
```

Measured with `zig build bench -Doptimize=ReleaseFast` (9 samples per workload, volatile barriers, **0 heap allocations**):

| Workload | Payload | Median (ns) | Min (ns) | Mops/s | Throughput (MB/s) |
|---|---:|---:|---:|---:|---:|
| `Small/encodedSize` | 29 B | 2.82 | 2.82 | 354.24 | 10,272.9 |
| `Small/encodeSlice (reverse)` | 29 B | 14.99 | 14.96 | 66.72 | 1,934.9 |
| `Small/encode (forward)` | 29 B | 15.50 | 15.48 | 64.53 | 1,871.5 |
| `Small/validateDepth` | 29 B | 17.87 | 17.24 | 55.96 | 1,622.8 |
| `Small/decode (validate + views)` | 29 B | 25.74 | 23.67 | 38.86 | 1,126.8 |
| `Small/encodeJsonSlice` | 87 B | 75.05 | 74.35 | 13.33 | 1,159.3 |
| `Small/wire -> JSON transcode` | 87 B | 91.96 | 91.35 | 10.87 | 946.0 |
| `Small/decodeJson (stack FBA)` | 87 B | 234.70 | 233.21 | 4.26 | 370.7 |
| `User/encodedSize` | 161 B | 42.55 | 42.40 | 23.50 | 3,783.5 |
| `User/encodeSlice (reverse)` | 161 B | 103.15 | 102.97 | 9.70 | 1,560.9 |
| `User/encode (forward)` | 161 B | 137.59 | 136.51 | 7.27 | 1,170.2 |
| `User/validateDepth` | 161 B | 121.02 | 120.50 | 8.26 | 1,330.3 |
| `User/decode (validate + views)` | 161 B | 161.61 | 160.70 | 6.19 | 996.3 |
| `User/decode + full traversal` | 161 B | 324.62 | 323.46 | 3.08 | 496.0 |
| `User/decodeOnly (id + role)` | 161 B | 36.35 | 36.11 | 27.51 | 4,428.7 |
| `User/fieldIterator (early-exit)` | 161 B | 16.37 | 15.77 | 61.08 | 9,833.4 |
| `User/encodeJsonSlice` | 348 B | 421.12 | 418.40 | 2.37 | 826.4 |
| `User/wire -> JSON transcode` | 348 B | 737.92 | 734.60 | 1.36 | 471.6 |
| `User/decodeJson (stack FBA)` | 348 B | 1,264.94 | 1,241.49 | 0.79 | 275.1 |
| `Batch/encodedSize` | 3,020 B | 251.13 | 248.92 | 3.98 | 12,025.5 |
| `Batch/encodeSlice (reverse)` | 3,020 B | 1,095.87 | 1,094.91 | 0.91 | 2,755.8 |
| `Batch/encode (forward)` | 3,020 B | 1,930.54 | 1,928.66 | 0.52 | 1,564.3 |
| `Batch/validateDepth` | 3,020 B | 957.42 | 932.97 | 1.04 | 3,154.3 |
| `Batch/decode (validate + views)` | 3,020 B | 987.02 | 959.00 | 1.01 | 3,059.7 |
| `Batch/decode + full traversal` | 3,020 B | 2,666.52 | 2,613.00 | 0.38 | 1,132.6 |
| `Batch/decodeOnly (host only)` | 3,020 B | 146.52 | 145.82 | 6.83 | 20,611.6 |
| `Batch/fieldIterator (sum deltas)` | 3,020 B | 315.42 | 314.01 | 3.17 | 9,574.4 |
| `Batch/encodeJsonSlice` | 7,112 B | 11,020.83 | 10,908.47 | 0.09 | 645.3 |
| `Batch/wire -> JSON transcode` | 7,112 B | 13,701.77 | 13,598.25 | 0.07 | 519.1 |
| `Batch/decodeJson (stack FBA)` | 7,112 B | 18,936.27 | 18,722.28 | 0.05 | 375.6 |

- **`Small` (`SmallEvent`):** Flat telemetry event (`uint64`, `int64`, `uint32`, UTF-8 `string`).
- **`User` (`UserProfile`):** Rich RPC message (`repeated uint32`, `repeated string`, `map<string, int32>`, nested message, explicit `optional bool`, `oneof`, cyclic `Lazy` message). `decodeOnly` is **4.4x faster** and early-exit `fieldIterator` is **9.9x faster** than full `decode`.
- **`Batch` (`TelemetryBatch`):** 128 packed `sint64`, 128 packed `fixed64`, 64 repeated `Point` submessages. `encodeSlice` is **1.76x faster** than forward `encode`; `decodeOnly` (`host`) is **6.7x faster** than full `decode`.

---

## Testing & Fuzzing

```sh
# Format check
zig fmt --check build.zig build_proto.zig src bench tests

# Unit, compiler, WKT, ProtoJSON, gRPC, and unknown-field tests under ReleaseSafe
zig build test -Doptimize=ReleaseSafe --summary all

# Standalone zero-allocation wire fuzzer (PRNG mutations + structured round-trips)
zig build fuzz -Doptimize=ReleaseFast -- --iters 5000000
```

---

## Repository Structure

```text
├── build.zig                    # Exports protoz, proto_wire, proto_wkt, zig-protoc, protoc-gen-zig
├── build.zig.zon                # Zig package manifest (v0.1.0)
├── build_proto.zig              # Reusable build helpers (addProtoModule, addProtoPackage, *With)
├── LICENSE                      # MIT License
├── README.md
├── bench/                       # 3-tier zero-allocation wire & JSON benchmark suite
│   ├── bench.proto
│   └── main.zig
├── include/                     # Bundled Google Well-Known Types (google/protobuf/*.proto)
│   └── google/protobuf/
├── tests/
│   └── fuzz.zig                 # Cross-platform malformed-wire + structured round-trip fuzzer
└── src/
    ├── root.zig                 # Public `@import("protoz")` facade
    ├── wire.zig                 # Zero-allocation wire runtime (Reader, ReverseWriter, containers, framing)
    ├── json.zig                 # ProtoJSON encoder/decoder (zero-copy fast path + wire transcoding)
    ├── wkt.zig                  # Timestamp, Duration, and Any zero-allocation helpers
    ├── rpc.zig                  # gRPC 5-byte framing and comptime unary dispatch
    ├── ast.zig                  # Typed AST (proto2, proto3, editions, services)
    ├── diag.zig                 # Source-located compiler diagnostics (file:line:col)
    ├── lexer.zig                # Spec-compliant tokenizer with line/column tracking
    ├── parser.zig               # Recursive-descent .proto parser
    ├── loader.zig               # Multi-file import loader & path canonicalization
    ├── resolver.zig             # Scoped type resolution, cycle detection, and schema validation
    ├── codegen.zig              # Zero-allocation Zig 0.17.1 code emitter
    ├── plugin.zig               # Google protoc CodeGeneratorRequest/Response codec
    ├── protoc_main.zig          # Entrypoint for standalone zig-protoc CLI
    └── protoc_gen_zig_main.zig  # Entrypoint for protoc-gen-zig plugin
```

---

## License

[MIT](LICENSE)
