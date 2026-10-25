---
title: zcgltf
description: Zig bindings for cgltf — vendored upstream v1.15, complete surface enforced at compile time, std.mem.Allocator and std.Io adapters, ABI drift guarded by tests
license: MIT
author: pedronaugusto
author_github: pedronaugusto
repository: https://github.com/pedronaugusto/zcgltf
keywords:
  - zig-gamedev
date: 2026-10-25
updated_at: 2026-10-25T13:19:20+00:00
last_sync: 2026-10-25T13:19:20Z
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
permalink: /packages/pedronaugusto/zcgltf/
---

# zcgltf

Zig bindings for [cgltf](https://github.com/jkuhlmann/cgltf), a glTF 2.0
parser and writer. Parse glTF and GLB from memory or from a file, load
buffers, validate, read vertex data back through the accessor API, and write
documents out again.

## Usage

The block below is a region of [`examples/usage.zig`](examples/usage.zig),
which the tests build and run; the gate fails if this copy has drifted from
it.

<!-- BEGIN GENERATED zig build docs -- usage -->
```zig
const zcgltf = @import("zcgltf");

var options = std.mem.zeroes(zcgltf.Options);
options.memory = zcgltf.memoryOptions(&gpa);

const path = "tests/data/triangle.gltf";
const data = try zcgltf.parseFile(&options, path);
defer zcgltf.free(data);
try zcgltf.loadBuffers(&options, data, path);
try zcgltf.validate(data);

const prim = &data.meshes.?[0].primitives.?[0];
const positions = zcgltf.findAccessor(prim, .position, 0) orelse
    return error.MissingPositions;
const indices = prim.indices orelse return error.MissingIndices;

var corners: [9]f32 = undefined;
const floats = zcgltf.unpackFloats(positions, &corners);
var index_values: [3]u32 = undefined;
const idx = zcgltf.unpackIndices(indices, u32, &index_values);
```
<!-- END GENERATED -->

## Install

Requires Zig 0.17.0 and libc:

```sh
zig fetch --save git+https://github.com/pedronaugusto/zcgltf#main
```

Then in `build.zig`:

```zig
const zcgltf_dep = b.dependency("zcgltf", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("zcgltf", zcgltf_dep.module("zcgltf"));
```

Forward `optimize` as shown, or a release executable links a Debug library.
A C or C++ host links the library and includes upstream's own headers, which
the artifact installs:

```zig
exe.root_module.linkLibrary(zcgltf_dep.artifact("zcgltf"));  // then #include <cgltf.h>
```

zcgltf's one dependency is [aegis](https://github.com/pedronaugusto/aegis).

## Features

- Every function `cgltf.h` and `cgltf_write.h` declare is bound, and every
  struct, enum and union is mirrored under Zig names (`cgltf_buffer_view` is
  `BufferView`), with optionals where upstream documents a field as
  omittable. A compile-time check fails the build if a layout, signature or
  enumerator drifts from the headers, or if a header function is not bound.
- An idiomatic layer: one `Error` set for `cgltf_result`, slices in and out,
  and one `indexOf` for every object type, returning an index branded with
  its type.
- Documents are untrusted input. `parse` takes an `Input`; a buffer size a
  data URI cannot encode, an accessor index past its count, a buffer view
  running past its buffer, an accessor misaligned for its component type
  and an object the document does not hold are refused before upstream
  reads or allocates them.
- Allocation through any `std.mem.Allocator` (`memoryOptions`), file reads
  through `std.Io` with a byte limit and the reason for each refusal
  (`fileOptions`), and serialization into a Zig allocator (`writeAlloc`).
  Every hook is per document; nothing is process-wide.
- cgltf v1.15 is vendored in `libs/cgltf` with two patches:
  [`cgltf-attribute-count.patch`](libs/patches/cgltf-attribute-count.patch)
  fixes a crash in upstream's `cgltf_parse_json_attribute_list`
  (`cgltf.h:2928`) when an allocation is refused mid-parse, and
  [`cgltf-aligned-reads.patch`](libs/patches/cgltf-aligned-reads.patch)
  makes upstream's component reads (`cgltf.h:1566`, `2217`) defined at a
  misaligned address. A test proves each vendored file is upstream at the
  pinned commit with exactly its patches.

| | |
|---|---|
| Document lifecycle | `parse`, `parseFile`, `loadBuffers`, `loadBufferBase64`, `validate`, `free` |
| Strings | `decodeString`, `decodeUri` |
| Accessor reading | `findAccessor`, `readFloat`, `readUint`, `readIndex`, `unpackFloats`, `unpackIndices`, `unpackFloatsCount`, `unpackIndicesCount`, `bufferViewData` |
| Element sizing | `numComponents`, `componentSize`, `calcSize` |
| Node transforms | `nodeTransformLocal`, `nodeTransformWorld` |
| Object to index | `indexOf`, `animationIndexOf` |
| Writing | `writeFile`, `writeAlloc` |
| Adapters | `memoryOptions`, `freeThrough`, `fileOptions` |
| The raw C surface | `zcgltf.c` |

`EXT_meshopt_compression` is parsed, not decoded; the host decodes with
meshoptimizer and hands the bytes back through `BufferView.data`.
[docs/design.md](docs/design.md) has that contract, what upstream does that
zcgltf guards against, the measured cost of each binding beside the same work
in C, and how the vendored copy is checked and updated.

## Testing

```sh
bay test
```

runs the gate: formatting, structure, lint and documentation, the checks in
`ci/`, a consumer build, and the suite twice, against the C under Zig's
undefined-behaviour sanitizer and without it. The suite holds the ABI check,
the vendor check, behavioural tests per area, a sweep that refuses every
allocation and fails every I/O call of a document load once, fuzz properties
over both parsers, the C smoke test against the installed headers, the
examples, and one run of the bench. `bay dev bench` runs the bench in full.

## Licence

MIT, see [LICENSE](LICENSE). Vendored cgltf is MIT, copyright Johannes
Kuhlmann; its inlined jsmn JSON tokenizer is MIT, copyright Serge Zaitsev.
