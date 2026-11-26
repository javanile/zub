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
date: 2026-11-26
category: data-formats
updated_at: 2026-11-26T11:21:24+00:00
last_sync: 2026-11-26T11:21:24Z
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
- **Multi-GB/s Wire Throughput:** Up to **67.25 Mops/s** (14.87 ns) on small messages and **3.17 GB/s** decode / **2.81 GB/s** encode on batched payloads in `ReleaseFast` (see [Benchmarks](#benchmarks)).
- **Single-Pass Reverse Serialization (`ReverseWriter`):** `encodeSlice` writes backwards into caller-owned stack or slab buffers in a single pass—**1.60x faster** than forward streaming on batched payloads with no pre-pass size calculation for nested submessages.
- **On-Demand Decoding:** Comptime `decodeOnly(bytes, .{ .id, .role })` materializes a minimal stack struct and skips unselected fields (**4.6x–6.1x faster** than full decode); `fieldIterator(bytes)` streams fields with early exit (**8.6x faster** on `User`).
- **Full Protocol Toolkit:** Length-delimited framing (TCP/Unix/WAL), 5-byte gRPC HTTP/2 framing + comptime unary dispatch, zero-allocation ProtoJSON (`encodeJsonSlice` / `decodeJson`), Well-Known Type helpers (`Timestamp`, `Duration`, `Any`), `{f}` debug formatting, opt-in `UnknownFields` pass-through, and arena-backed `cloneOwned` / `cloneMessage`.
- **Two Compiler Frontends:** Native `zig-protoc` (pure Zig lexer/parser/resolver with `file:line:col` diagnostics, transitive `import public`, and Make `.d` depfiles) and a standard `protoc-gen-zig` plugin for `protoc` / `buf`.
- **First-Class `build.zig` Integration:** Package manifest exports `@import("protoz")` (application facade), `proto_wire` (slim runtime imported by generated `.pb.zig` files), `proto_wkt` (pre-wired Google Well-Known Types), host `zig-protoc` / `protoc-gen-zig` binaries, and `addProtoModule` / `addProtoPackage` helpers.

---

## Installation

Requires **Zig 0.17.1+**.

Add `protoz` to your project with `zig fetch`:

```sh
zig fetch --save git+https://github.com/sahrahul181/protoz#v0.1.1
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
        // .minimal = true,                 // omit optional JSON/iterator/helper/validate families
        // .only_roots = &.{"api.Request"}, // prune unreachable declarations
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

Standalone `zig-protoc` also supports `--out <file>`, `--out-dir <dir>`, `--root-file <name>`, `--depfile <file>`, `-I <dir>`, `--preserve-unknown-fields`, `--minimal` (plus `--no-*`/`--emit-*` toggles), and `--only`:

```sh
./zig-out/bin/zig-protoc \
  -I proto -I include \
  --out-dir generated_pb \
  --root-file root.zig \
  --depfile generated_pb/proto.d \
  --minimal \
  --only api.Request,api.Response \
  proto/api.proto
```

### Minimal Codegen & Reachability Pruning

For large schemas, you can cut generated code size and compile time without changing the core wire API (`decode`, `encodeSlice`, `encodeReverse`):

- **Minimal profile (`--minimal`):** Omits optional helper families—ProtoJSON, `fieldIterator`, `format`/`cloneInto`/`cloneOwned` helpers, `decodeOnly`, forward `encode`/`encodedSize`, and `validateDepth` (while `proto_wire` falls back cleanly with zero allocations). Individual families can still be toggled via `--no-json` / `--emit-json`, `--no-iter` (`--no-field-iterator`) / `--emit-iter` (`--emit-field-iterator`), `--no-helpers` / `--emit-helpers`, `--no-decode-only` / `--emit-decode-only`, `--no-forward-encode` / `--emit-forward-encode`, and `--no-validate` / `--emit-validate`.
- **Reachability pruning (`--only`):** Accepts comma-separated or repeated message, enum, or service roots (`pkg.Packet`, `Packet`, `MyService`) and emits only transitively referenced declarations (keeping bare namespace shells for nested types and skipping unreachable files in `--out-dir` / `root.zig`).
- **`protoc-gen-zig` `--zig_opt` parameters:** Supports `minimal=true|false`, `emit_json=...`, `emit_field_iterator=...`, `emit_helpers=...`, `emit_decode_only=...`, `emit_forward_encode=...`, `emit_validate=...`, and `only=MsgA+MsgB` (or `;`-separated / repeated `only=...`).
- **`build.zig` options (`addProtoModule` / `addProtoPackage`):** Exposes `.minimal = true`, nullable `.emit_*` overrides (`?bool`), and `.only_roots = &.{ ... }`.

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

## Scope & Intentional Boundaries

- **Protobuf coverage:** Supports `proto2` (including `group`, `extensions`, `extend`, custom `defaults`, and transitive `required` validation), `proto3` (including `proto3 optional`), and **Edition 2023** (`field_presence`, `repeated_field_encoding`, `utf8_validation`, and `message_encoding = DELIMITED` in both `zig-protoc` and `protoc-gen-zig`).
- **Not included in v0.1.1:** `import weak` (parsed and skipped), arbitrary runtime custom descriptor options, and `textproto` parsing (human-readable `{f}` debug formatting and ProtoJSON are provided instead).
- **gRPC & transport:** `protoz.rpc` handles 5-byte Length-Prefixed framing and zero-allocation comptime dispatchers (`dispatchUnaryGrpc`, `dispatchClientStreamGrpc`, `dispatchServerStreamGrpc`, `dispatchBidiStreamGrpc`, `dispatchGrpc`). Compressed gRPC payloads (`compressed = 1`) are exposed via `rpc.tryDecodeGrpcRaw` for caller-chosen decompression, and full HTTP/2 transport (HPACK, TLS, multiplexing) is left to the application's transport layer.
- **`google.protobuf.Any` in ProtoJSON:** Inline JSON expansion uses a zero-allocation comptime type tuple (`encodeMessageSliceWithTypes` / `decodeMessageWithTypes`); unregistered types fall back cleanly to `{"@type":"...","value":"<base64>"}`.

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
| `Small/encodedSize` | 29 B | 2.83 | 2.83 | 353.32 | 10,246.3 |
| `Small/encodeSlice (reverse)` | 29 B | 14.87 | 14.85 | 67.25 | 1,950.4 |
| `Small/encode (forward)` | 29 B | 15.81 | 15.77 | 63.26 | 1,834.6 |
| `Small/validateDepth` | 29 B | 17.87 | 17.64 | 55.95 | 1,622.6 |
| `Small/decode (validate + views)` | 29 B | 25.66 | 24.39 | 38.97 | 1,130.2 |
| `Small/encodeJsonSlice` | 87 B | 63.47 | 63.30 | 15.76 | 1,370.8 |
| `Small/wire -> JSON transcode` | 87 B | 83.97 | 83.35 | 11.91 | 1,036.1 |
| `Small/decodeJson (stack FBA)` | 87 B | 220.67 | 215.59 | 4.53 | 394.3 |
| `User/encodedSize` | 161 B | 40.96 | 40.72 | 24.42 | 3,931.1 |
| `User/encodeSlice (reverse)` | 161 B | 102.47 | 102.37 | 9.76 | 1,571.3 |
| `User/encode (forward)` | 161 B | 132.03 | 131.08 | 7.57 | 1,219.4 |
| `User/validateDepth` | 161 B | 130.67 | 129.74 | 7.65 | 1,232.1 |
| `User/decode (validate + views)` | 161 B | 170.72 | 166.96 | 5.86 | 943.1 |
| `User/decode + full traversal` | 161 B | 325.09 | 324.53 | 3.08 | 495.2 |
| `User/decodeOnly (id + role)` | 161 B | 36.94 | 35.96 | 27.07 | 4,358.2 |
| `User/fieldIterator (early-exit)` | 161 B | 19.93 | 19.37 | 50.19 | 8,080.1 |
| `User/encodeJsonSlice` | 348 B | 343.29 | 341.54 | 2.91 | 1,013.7 |
| `User/wire -> JSON transcode` | 348 B | 685.52 | 682.09 | 1.46 | 507.6 |
| `User/decodeJson (stack FBA)` | 348 B | 951.51 | 946.03 | 1.05 | 365.7 |
| `Batch/encodedSize` | 3,020 B | 251.25 | 248.74 | 3.98 | 12,019.9 |
| `Batch/encodeSlice (reverse)` | 3,020 B | 1,072.85 | 1,071.71 | 0.93 | 2,814.9 |
| `Batch/encode (forward)` | 3,020 B | 1,711.40 | 1,709.47 | 0.58 | 1,764.6 |
| `Batch/validateDepth` | 3,020 B | 912.53 | 857.07 | 1.10 | 3,309.5 |
| `Batch/decode (validate + views)` | 3,020 B | 953.17 | 933.31 | 1.05 | 3,168.4 |
| `Batch/decode + full traversal` | 3,020 B | 2,689.49 | 2,654.09 | 0.37 | 1,122.9 |
| `Batch/decodeOnly (host only)` | 3,020 B | 156.40 | 153.77 | 6.39 | 19,309.2 |
| `Batch/fieldIterator (sum deltas)` | 3,020 B | 314.02 | 312.16 | 3.18 | 9,617.1 |
| `Batch/encodeJsonSlice` | 7,112 B | 10,828.87 | 10,784.00 | 0.09 | 656.8 |
| `Batch/wire -> JSON transcode` | 7,112 B | 13,909.23 | 13,873.26 | 0.07 | 511.3 |
| `Batch/decodeJson (stack FBA)` | 7,112 B | 18,741.41 | 18,704.28 | 0.05 | 379.5 |

- **`Small` (`SmallEvent`):** Flat telemetry event (`uint64`, `int64`, `uint32`, UTF-8 `string`).
- **`User` (`UserProfile`):** Rich RPC message (`repeated uint32`, `repeated string`, `map<string, int32>`, nested message, explicit `optional bool`, `oneof`, cyclic `Lazy` message). `decodeOnly` is **4.6x faster** and early-exit `fieldIterator` is **8.6x faster** than full `decode`.
- **`Batch` (`TelemetryBatch`):** 128 packed `sint64`, 128 packed `fixed64`, 64 repeated `Point` submessages. `encodeSlice` is **1.60x faster** than forward `encode`; `decodeOnly` (`host`) is **6.1x faster** than full `decode`.

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
├── build.zig.zon                # Zig package manifest (v0.1.1)
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
